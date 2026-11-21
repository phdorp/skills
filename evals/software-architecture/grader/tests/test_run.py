import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GRADER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GRADER))

import run  # noqa: E402

DATA = Path(__file__).resolve().parent / "data"
REPO_ROOT = GRADER.parents[2]


def _git_subjects(ws):
    out = subprocess.run(["git", "log", "--format=%s"], cwd=ws, capture_output=True,
                         text=True, check=True).stdout
    return out.split()


class LoadScenarios(unittest.TestCase):
    def _write(self, text):
        d = Path(tempfile.mkdtemp())
        p = d / "TASKS.md"
        p.write_text(text)
        return p

    def test_load_scenarios_reads_fixture_and_prompt(self):
        p = self._write("# Tasks\n\nIntro.\n\n## S99 thing: a test\n\nFixture: plain\n\n"
                        "```text\nDo the thing.\n```\n\n## S98 other\n\nFixture: x\n\n"
                        "```text\nOther.\n```\n")
        scenarios = run.load_scenarios(p)
        s = scenarios["S99"]
        self.assertEqual((s.id, s.fixture, s.prompt), ("S99", "plain", "Do the thing.\n"))
        self.assertEqual(set(scenarios), {"S99", "S98"})

    def test_load_scenarios_reads_optional_overlay(self):
        p = self._write("## S97 x\n\nFixture: setup\nOverlay: s97\n\n```text\nGo.\n```\n\n"
                        "## S96 y\n\nFixture: setup\n\n```text\nGo.\n```\n")
        scenarios = run.load_scenarios(p)
        self.assertEqual((scenarios["S97"].overlay, scenarios["S96"].overlay), ("s97", None))

    def test_load_scenarios_reads_optional_invoke(self):
        p = self._write("## S95 x\n\nFixture: setup\nInvoke: add-requirements\n\n```text\nGo.\n```\n\n"
                        "## S94 y\n\nFixture: setup\n\n```text\nGo.\n```\n")
        scenarios = run.load_scenarios(p)
        self.assertEqual((scenarios["S95"].invoke, scenarios["S94"].invoke),
                         ("add-requirements", None))

    def test_load_scenarios_rejects_section_without_fixture(self):
        p = self._write("## S99 thing\n\n```text\nDo it.\n```\n")
        with self.assertRaises(ValueError):
            run.load_scenarios(p)

    def test_load_scenarios_rejects_section_with_two_prompts(self):
        p = self._write("## S99 thing\n\nFixture: plain\n\n```text\nA\n```\n\n```text\nB\n```\n")
        with self.assertRaises(ValueError):
            run.load_scenarios(p)


class BuildPrompt(unittest.TestCase):
    def setUp(self):
        self.plugin_dir = Path(tempfile.mkdtemp()) / "sa"
        (self.plugin_dir / "skills" / "add-requirements").mkdir(parents=True)
        (self.plugin_dir / "skills" / "add-requirements" / "SKILL.md").write_text("x\n")

    def test_build_prompt_prefixes_slash_when_arm_has_skill(self):
        s = run.Scenario("S95", "setup", "Integrate these.\n", invoke="add-requirements")
        self.assertEqual(run.build_prompt(s, self.plugin_dir),
                         "/sa:add-requirements Integrate these.\n")

    def test_build_prompt_plain_when_arm_lacks_skill(self):
        s = run.Scenario("S95", "setup", "Integrate these.\n", invoke="quality-requirements")
        self.assertEqual(run.build_prompt(s, self.plugin_dir), "Integrate these.\n")


class Isolation(unittest.TestCase):
    def setUp(self):
        self.plugin_dir = Path(tempfile.mkdtemp()) / "sa"
        for name in ("alpha", "beta"):
            (self.plugin_dir / "skills" / name).mkdir(parents=True)
        self.user = {"codebase-design", "code-review"}

    def _init(self, name, **override):
        text = (DATA / name).read_text().replace("{plugin_dir}", str(self.plugin_dir))
        init = json.loads(text)
        init.update(override)
        return init

    def test_isolation_ok(self):
        self.assertEqual(run.check_isolation(self._init("init-ok.json"), self.plugin_dir,
                                             self.user), [])

    def test_isolation_flags_user_skill_leak(self):
        errors = run.check_isolation(self._init("init-leak.json"), self.plugin_dir, self.user)
        self.assertTrue(any("codebase-design" in e for e in errors), errors)

    def test_isolation_flags_foreign_plugin(self):
        init = self._init("init-ok.json")
        init["plugins"].append({"name": "x", "path": "/root/elsewhere", "source": "x@inline"})
        errors = run.check_isolation(init, self.plugin_dir, self.user)
        self.assertTrue(any("/root/elsewhere" in e for e in errors), errors)

    def test_isolation_flags_missing_arm_plugin(self):
        init = self._init("init-ok.json")
        init["plugins"] = [p for p in init["plugins"] if p["path"] == "builtin"]
        self.assertNotEqual(run.check_isolation(init, self.plugin_dir, self.user), [])

    def test_isolation_flags_missing_arm_skill(self):
        (self.plugin_dir / "skills" / "gamma").mkdir()
        errors = run.check_isolation(self._init("init-ok.json"), self.plugin_dir, self.user)
        self.assertTrue(any("gamma" in e for e in errors), errors)


class Transcript(unittest.TestCase):
    def test_render_transcript_has_prompt_text_and_tool_calls(self):
        md = run.render_transcript(DATA / "stream-sample.jsonl", "Run ls, then say done.")
        self.assertIn("### user\n\nRun ls, then say done.", md)
        self.assertIn("### tool_use Bash", md)
        self.assertIn('"command": "ls"', md)
        self.assertIn("### tool_result", md)
        self.assertIn("a.txt", md)
        self.assertIn("### assistant", md)
        self.assertIn("Done.", md)

    def test_render_transcript_survives_truncated_stream(self):
        d = Path(tempfile.mkdtemp())
        p = d / "t.jsonl"
        p.write_text((DATA / "stream-sample.jsonl").read_text()[:-40])
        md = run.render_transcript(p, "x")
        self.assertIn("### user", md)


class Workspace(unittest.TestCase):
    def test_prepare_workspace_is_outside_repo_and_committed(self):
        fixture = Path(tempfile.mkdtemp()) / "plain"
        fixture.mkdir()
        (fixture / "README.md").write_text("hi\n")
        ws = run.prepare_workspace(fixture)
        self.assertFalse(ws.resolve().is_relative_to(REPO_ROOT))
        self.assertEqual(_git_subjects(ws), ["fixture"])
        self.assertTrue((ws / "README.md").exists())

    def test_prepare_workspace_applies_overlay(self):
        root = Path(tempfile.mkdtemp())
        (root / "fx" / "docs").mkdir(parents=True)
        (root / "fx" / "docs" / "a.md").write_text("fixture\n")
        (root / "ov" / "docs").mkdir(parents=True)
        (root / "ov" / "docs" / "a.md").write_text("overlay\n")
        (root / "ov" / "docs" / "b.md").write_text("new\n")
        ws = run.prepare_workspace(root / "fx", root / "ov")
        self.assertEqual((ws / "docs" / "a.md").read_text(), "overlay\n")
        self.assertTrue((ws / "docs" / "b.md").exists())
        self.assertEqual(_git_subjects(ws), ["fixture"])
        status = subprocess.run(["git", "status", "--porcelain"], cwd=ws, capture_output=True,
                                text=True).stdout
        self.assertEqual(status, "")

    def test_run_dir_refuses_existing(self):
        suite = Path(tempfile.mkdtemp())
        (suite / "runs" / "baseline" / "S01-r1").mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            run.new_run_dir(suite, "baseline", "S01", 1)


if __name__ == "__main__":
    unittest.main()
