import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "openspec" / "changes" / "add-codex-plugin-compatibility"


def read_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path):
    return path.read_text(encoding="utf-8")


class CodexPluginCompatibilityTests(unittest.TestCase):
    def test_codex_marketplace_lists_both_plugins(self):
        """Codex marketplace lists both plugins."""
        marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        plugins = {plugin["name"]: plugin for plugin in marketplace["plugins"]}

        self.assertEqual(
            {
                "yuki-toolkit": "./plugins/yuki-toolkit",
                "spec-driven-dev": "./plugins/spec-driven-dev",
            },
            {
                name: plugin["source"]["path"]
                for name, plugin in plugins.items()
                if name in {"yuki-toolkit", "spec-driven-dev"}
            },
        )

    def test_claude_marketplace_remains_present(self):
        """Claude marketplace remains present."""
        marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
        sources = {plugin["name"]: plugin["source"] for plugin in marketplace["plugins"]}

        self.assertEqual("./plugins/yuki-toolkit", sources["yuki-toolkit"])
        self.assertEqual("./plugins/spec-driven-dev", sources["spec-driven-dev"])

    def test_yuki_toolkit_has_codex_metadata(self):
        """yuki-toolkit has Codex metadata."""
        manifest = read_json(
            ROOT / "plugins" / "yuki-toolkit" / ".codex-plugin" / "plugin.json"
        )

        self.assertEqual("yuki-toolkit", manifest["name"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertIn("interface", manifest)
        self.assertLess(
            (ROOT / "plugins" / "yuki-toolkit" / ".codex-plugin" / "plugin.json").stat().st_size,
            5000,
        )

    def test_spec_driven_dev_has_codex_metadata(self):
        """spec-driven-dev has Codex metadata."""
        manifest = read_json(
            ROOT / "plugins" / "spec-driven-dev" / ".codex-plugin" / "plugin.json"
        )

        self.assertEqual("spec-driven-dev", manifest["name"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertIn("interface", manifest)
        self.assertLess(
            (
                ROOT
                / "plugins"
                / "spec-driven-dev"
                / ".codex-plugin"
                / "plugin.json"
            ).stat().st_size,
            5000,
        )

    def test_claude_plugin_manifests_remain_compatible(self):
        """Claude plugin manifests remain compatible."""
        yuki = read_json(
            ROOT / "plugins" / "yuki-toolkit" / ".claude-plugin" / "plugin.json"
        )
        spec = read_json(
            ROOT / "plugins" / "spec-driven-dev" / ".claude-plugin" / "plugin.json"
        )

        self.assertIn("./agents/running-coach-zh-tw.md", yuki["agents"])
        self.assertTrue(any("gws-reference" in skill for skill in yuki["skills"]))
        self.assertTrue(any("brainstorming" in skill for skill in spec["skills"]))

    def test_existing_skills_remain_shared(self):
        """Existing skills remain shared."""
        self.assertTrue((ROOT / "plugins" / "yuki-toolkit" / "skills").is_dir())
        self.assertTrue((ROOT / "plugins" / "spec-driven-dev" / "skills").is_dir())
        self.assertEqual(
            "./skills/",
            read_json(
                ROOT / "plugins" / "yuki-toolkit" / ".codex-plugin" / "plugin.json"
            )["skills"],
        )
        self.assertEqual(
            "./skills/",
            read_json(
                ROOT
                / "plugins"
                / "spec-driven-dev"
                / ".codex-plugin"
                / "plugin.json"
            )["skills"],
        )

    def test_running_coach_remains_agent_first(self):
        """Running coach remains agent-first."""
        agent_path = ROOT / "plugins" / "yuki-toolkit" / "agents" / "running-coach-zh-tw.md"
        wrapper_path = (
            ROOT / "plugins" / "yuki-toolkit" / "skills" / "running-coach-zh-tw" / "SKILL.md"
        )

        self.assertTrue(agent_path.is_file())
        self.assertFalse(wrapper_path.exists())

    def test_thin_wrapper_is_added_only_when_required(self):
        """Thin wrapper is added only when required."""
        evidence = read_text(CHANGE_DIR / "running-coach-codex-agent-verification.md")

        self.assertIn("Task 2.3 is not needed for now", evidence)
        self.assertIn("No install-time or discovery-time failure", evidence)

    def test_readme_includes_codex_installation(self):
        """README includes Codex installation."""
        readme = read_text(ROOT / "README.md")

        self.assertIn("/plugin install yuki-toolkit@yuki-marketplace", readme)
        self.assertIn("codex plugin marketplace add", readme)
        self.assertIn("codex plugin add yuki-toolkit@yuki-marketplace", readme)
        self.assertIn("codex plugin add spec-driven-dev@yuki-marketplace", readme)

    def test_readme_explains_one_content_source_maintenance(self):
        """README explains one-content-source maintenance."""
        readme = read_text(ROOT / "README.md")

        self.assertIn("Claude 與 Codex 使用各自的包裝 metadata", readme)
        self.assertIn("source of truth", readme)
        self.assertIn("不要為 Codex 複製第二份長篇 skill 或 agent 內容", readme)

    def test_readme_or_repo_guidance_explains_version_alignment(self):
        """README or repo guidance explains version alignment."""
        readme = read_text(ROOT / "README.md")
        claude = read_text(ROOT / "CLAUDE.md")

        self.assertIn("Codex manifest version 應與對應 Claude plugin version 保持一致", readme)
        self.assertIn("Codex `.codex-plugin/plugin.json` version 要與對應 Claude plugin version 保持一致", claude)

    def test_manifest_json_parses_successfully(self):
        """Manifest JSON parses successfully."""
        for path in [
            ROOT / ".claude-plugin" / "marketplace.json",
            ROOT / ".agents" / "plugins" / "marketplace.json",
            ROOT / "plugins" / "yuki-toolkit" / ".claude-plugin" / "plugin.json",
            ROOT / "plugins" / "yuki-toolkit" / ".codex-plugin" / "plugin.json",
            ROOT / "plugins" / "spec-driven-dev" / ".claude-plugin" / "plugin.json",
            ROOT / "plugins" / "spec-driven-dev" / ".codex-plugin" / "plugin.json",
        ]:
            self.assertIsInstance(read_json(path), dict)

    def test_codex_manifests_reference_existing_shared_paths(self):
        """Codex manifests reference existing shared paths."""
        for plugin in ["yuki-toolkit", "spec-driven-dev"]:
            manifest = read_json(ROOT / "plugins" / plugin / ".codex-plugin" / "plugin.json")
            self.assertEqual("./skills/", manifest["skills"])
            self.assertTrue((ROOT / "plugins" / plugin / "skills").is_dir())

    def test_codex_marketplace_smoke_behavior_is_recorded(self):
        """Codex marketplace smoke behavior is recorded."""
        evidence = read_text(CHANGE_DIR / "running-coach-codex-agent-verification.md")

        self.assertIn("codex plugin marketplace add", evidence)
        self.assertIn("codex plugin add yuki-toolkit@yuki-marketplace", evidence)
        self.assertIn("codex plugin list --available --json", evidence)

    def test_running_coach_codex_behavior_is_recorded(self):
        """Running coach Codex behavior is recorded."""
        evidence = read_text(CHANGE_DIR / "running-coach-codex-agent-verification.md")
        normalized = " ".join(evidence.split())

        self.assertIn("agents/running-coach-zh-tw.md", evidence)
        self.assertIn("cache", evidence)
        self.assertIn("runtime dispatch", normalized)


if __name__ == "__main__":
    unittest.main()
