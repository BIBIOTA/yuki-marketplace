import sys
from pathlib import Path

REQUIRED = {"name", "description"}

def _parse_simple_yaml(text: str) -> dict[str, str] | None:
    """Parse the constrained YAML subset used in SKILL.md frontmatter.
    Returns None if input contains unsupported constructs."""
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return None
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not key or value == "":
            return None
        out[key] = value
    return out

def validate(path: Path) -> list[str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return [f"{path}: missing opening '---' frontmatter delimiter"]
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return [f"{path}: missing closing '---' frontmatter delimiter"]
    fm = _parse_simple_yaml(parts[1])
    if fm is None:
        return [f"{path}: frontmatter uses unsupported YAML (only flat 'key: value' pairs allowed)"]
    missing = REQUIRED - fm.keys()
    if missing:
        return [f"{path}: missing required keys: {sorted(missing)}"]
    expected_name = path.parent.name
    if fm["name"] != expected_name:
        return [f"{path}: frontmatter name '{fm['name']}' != directory name '{expected_name}'"]
    return []

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate-skill-frontmatter.py <SKILL.md> [<SKILL.md>...]")
        return 2
    errors = []
    for arg in sys.argv[1:]:
        errors.extend(validate(Path(arg)))
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print(f"OK: {len(sys.argv) - 1} skill file(s) validated")
    return 0

if __name__ == "__main__":
    sys.exit(main())
