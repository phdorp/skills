import json
import shutil
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

    def test_load_scenarios_reads_replies(self):
        p = self._write("## S93 x\n\nFixture: fresh\n\n```text\nGo.\n```\n\n```reply\nYes.\n```\n\n"
                        "```reply\nMore.\n```\n\n## S92 y\n\nFixture: fresh\n\n```text\nGo.\n```\n")
        scenarios = run.load_scenarios(p)
        self.assertEqual(scenarios["S93"].prompt, "Go.\n")
        self.assertEqual((scenarios["S93"].replies, scenarios["S92"].replies),
                         (["Yes.\n", "More.\n"], []))

    def test_load_scenarios_reads_prompt_from(self):
        p = self._write("## S91 x\n\nFixture: setup\nPrompt-from: skills/a/b.md\n\n```text\nk: v\n```\n\n"
                        "## S90 y\n\nFixture: setup\n\n```text\nGo.\n```\n")
        scenarios = run.load_scenarios(p)
        self.assertEqual((scenarios["S91"].prompt_from, scenarios["S90"].prompt_from),
                         ("skills/a/b.md", None))

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

    def test_build_prompt_fills_arm_template(self):
        (self.plugin_dir / "skills" / "x").mkdir()
        (self.plugin_dir / "skills" / "x" / "p.md").write_text(TEMPLATE)
        s = run.Scenario("S91", "setup", "[directory]: here\n", prompt_from="skills/x/p.md")
        self.assertIn("Work from: here\n", run.build_prompt(s, self.plugin_dir))
        self.assertNotIn("Subagent (general-purpose)", run.build_prompt(s, self.plugin_dir))

    def test_build_prompt_plain_when_arm_lacks_skill(self):
        s = run.Scenario("S95", "setup", "Integrate these.\n", invoke="quality-requirements")
        self.assertEqual(run.build_prompt(s, self.plugin_dir), "Integrate these.\n")


TEMPLATE = """# Template

Use it.

```
Subagent (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name]

    Read your brief: [BRIEF_FILE]

    [Scene-setting: where this fits,
    the rulings.]

    Work from: [directory]
```

**Placeholders:** `[BRIEF_FILE]`
"""


class FillTemplate(unittest.TestCase):
    def test_fill_template_fills_bracketed_and_literal_keys(self):
        fills = ("Task N: Task 2\n[task name]: Tags\n[BRIEF_FILE]: b.md\n"
                 "[Scene-setting]: Task 1 is separate.\n[directory]: here\n")
        self.assertEqual(run.fill_template(TEMPLATE, fills),
                         "You are implementing Task 2: Tags\n\nRead your brief: b.md\n\n"
                         "Task 1 is separate.\n\nWork from: here\n")

    def test_fill_template_rejects_unknown_key(self):
        with self.assertRaises(ValueError):
            run.fill_template(TEMPLATE, "[REPORT_FILE]: r.md\n")

    def test_fill_template_rejects_template_without_prompt(self):
        with self.assertRaises(ValueError):
            run.fill_template("# no block\n", "Task N: Task 2\n")


class Turns(unittest.TestCase):
    def test_turn_summary_keeps_every_exit_code(self):
        s = run.turn_summary(["timeout", 0], [None, 0.02], expected=2)
        self.assertEqual((s["exit_codes"], s["exit_code"], s["cost_usd"]), (["timeout", 0], "timeout", None))
        self.assertTrue(any("turn 1" in e for e in s["errors"]), s["errors"])

    def test_turn_summary_clean_run(self):
        s = run.turn_summary([0, 0], [0.01, 0.02], expected=2)
        self.assertEqual((s["exit_code"], s["cost_usd"], s["errors"]), (0, 0.03, []))

    def test_turn_summary_flags_missing_turns(self):
        s = run.turn_summary([0], [0.01], expected=2)
        self.assertTrue(any("1 of 2" in e for e in s["errors"]), s["errors"])

    def test_turn_summary_single_turn_keeps_old_meaning(self):
        s = run.turn_summary([1], [0.01], expected=1)
        self.assertEqual((s["exit_code"], s["errors"]), (1, []))


class ClaudeCmd(unittest.TestCase):
    def test_claude_cmd_adds_resume(self):
        cmd = run.claude_cmd("hi", Path("/p/sa"), resume="abc-123")
        self.assertEqual(cmd[cmd.index("--resume") + 1], "abc-123")
        self.assertEqual(cmd[cmd.index("-p") + 1], "hi")
        self.assertNotIn("--resume", run.claude_cmd("hi", Path("/p/sa")))


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

    def test_isolation_flags_mcp_server(self):
        init = self._init("init-ok.json")
        init["mcp_servers"] = [{"name": "claude.ai Claude Docs", "status": "pending", "source": "claudeai"}]
        errors = run.check_isolation(init, self.plugin_dir, self.user)
        self.assertTrue(any("Claude Docs" in e for e in errors), errors)

    def test_child_runs_without_claudeai_connectors(self):
        self.assertEqual(run._child_env()["ENABLE_CLAUDEAI_MCP_SERVERS"], "false")
        self.assertIn("--strict-mcp-config", run.claude_cmd("hi", Path("/p/sa")))

    def test_session_mismatch_fails_isolation(self):
        first, second = self._init("init-ok.json"), self._init("init-ok.json")
        second["session_id"] = "another-session"
        self.assertEqual(run.turn_errors([first, dict(first)], self.plugin_dir, self.user), [])
        errors = run.turn_errors([first, second], self.plugin_dir, self.user)
        self.assertTrue(any("session" in e for e in errors), errors)

    def test_turn_without_init_fails_isolation(self):
        errors = run.turn_errors([self._init("init-ok.json"), {}], self.plugin_dir, self.user)
        self.assertTrue(any("turn 2" in e for e in errors), errors)

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

    def test_render_turns_in_order(self):
        md = run.render_turns([(DATA / "stream-sample.jsonl", "First turn."),
                               (DATA / "stream-sample.jsonl", "Second turn.")])
        self.assertLess(md.index("### user\n\nFirst turn."), md.index("### user\n\nSecond turn."))
        self.assertEqual(md.count("Done."), 2)

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


class RecordGit(unittest.TestCase):
    def test_record_writes_git_status(self):
        fixture = Path(tempfile.mkdtemp(prefix="sa-test-"))
        out = Path(tempfile.mkdtemp(prefix="sa-test-"))
        self.addCleanup(shutil.rmtree, fixture, ignore_errors=True)
        self.addCleanup(shutil.rmtree, out, ignore_errors=True)
        (fixture / "kept.txt").write_text("committed\n")
        ws = run.prepare_workspace(fixture)
        self.addCleanup(shutil.rmtree, ws.parent, ignore_errors=True)
        (ws / "docs").mkdir()
        (ws / "docs" / "new.md").write_text("untracked\n")
        run.record_git(ws, out)
        self.assertEqual((out / "git-status.txt").read_text(), "?? docs/new.md\n")
        self.assertIn(" fixture", (out / "git-log.txt").read_text())


if __name__ == "__main__":
    unittest.main()
