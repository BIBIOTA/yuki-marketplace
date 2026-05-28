# scripts/validate-skill-frontmatter.py
import sys
import yaml
from pathlib import Path

REQUIRED = {"name", "description"}

def validate(path: Path) -> list[str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return [f"{path}: missing opening '---' frontmatter delimiter"]
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return [f"{path}: missing closing '---' frontmatter delimiter"]
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [f"{path}: invalid YAML: {e}"]
    if not isinstance(fm, dict):
        return [f"{path}: frontmatter is not a mapping"]
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
