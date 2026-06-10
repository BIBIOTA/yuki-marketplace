#!/usr/bin/env python3
"""
PostToolUse hook: validate gh pr create output.

Checks:
  1. PR title is ASCII-only (English)
  2. PR has at least one assignee

Triggered on every Bash PostToolUse; exits 0 immediately if the command
is not a `gh pr create` call, so there is no performance impact on other
Bash commands.

Exit codes:
  0 — validation passed (or not a pr create command)
  1 — validation failed; stdout message is surfaced to Claude as feedback
"""

import json
import re
import subprocess
import sys


def is_ascii(text: str) -> bool:
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    command: str = data.get("tool_input", {}).get("command", "")

    if "gh pr create" not in command:
        sys.exit(0)

    output: str = data.get("tool_response", {}).get("output", "")

    # Extract PR URL from gh pr create output (last non-empty line is the URL)
    pr_url: str | None = None
    for line in reversed(output.strip().splitlines()):
        line = line.strip()
        if re.match(r"https://github\.com/.+/pull/\d+", line):
            pr_url = line
            break

    if not pr_url:
        sys.exit(0)

    try:
        result = subprocess.run(
            ["gh", "pr", "view", pr_url, "--json", "title,assignees"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            sys.exit(0)
        pr_data = json.loads(result.stdout)
    except Exception:
        sys.exit(0)

    issues: list[str] = []

    title: str = pr_data.get("title", "")
    if not is_ascii(title):
        issues.append(
            f'PR title contains non-English characters: "{title}"\n'
            f'  Fix: gh pr edit {pr_url} --title "<English title>"'
        )

    assignees: list = pr_data.get("assignees", [])
    if not assignees:
        issues.append(
            f"PR has no assignee.\n"
            f"  Fix: gh pr edit {pr_url} --add-assignee @me"
        )

    if issues:
        print("⚠️  PR convention check failed:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
