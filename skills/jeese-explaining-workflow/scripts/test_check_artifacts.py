"""CLI regression tests; all generated artifacts stay in temporary directories."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check_artifacts.py")
FACT = "本次从 ReadState 读取缓存；仅在缓存失效时进入远端读取。"


def block(stage, body=FACT, run="read-1", mode="standard", branch="learning", diagram=False):
    meta = dict(run=run, mode=mode, branch=branch, stage=stage, diagram=diagram)
    return "<!-- workflow:" + json.dumps(meta) + " -->\n" + body + "\n<!-- /workflow -->\n"


class ArtifactChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.task = self.root / "中文任务 带空格"
        self.task.mkdir()

    def invoke(self, text, through=1, mode="standard", branch="learning", run="read-1", file="work.md",
               read_stages=None):
        path = self.task / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        result = self.command(through, mode, branch, run, file, read_stages)
        self.assertEqual(path.read_text(encoding="utf-8"), text, "validator must not write artifacts")
        return result

    def command(self, through=1, mode="standard", branch="learning", run="read-1", file="work.md",
                read_stages=None):
        action = (["--read-stages"] + [str(stage) for stage in read_stages]
                  if read_stages is not None else ["--through", str(through)])
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--task-dir", str(self.task), "--file", file,
             "--run", run, "--mode", mode, "--branch", branch] + action,
            text=True, capture_output=True, check=False,
        )

    def assert_status(self, code, result):
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)

    def test_each_mode_accepts_only_completed_prefix(self):
        for mode, count in (("standard", 4), ("quick", 3), ("source", 4)):
            for through in range(1, count + 1):
                with self.subTest(mode=mode, through=through):
                    text = "任务：为当前修改理解读取路径。\n" + "".join(
                        block(i, mode=mode) for i in range(1, through + 1))
                    self.assert_status(0, self.invoke(text, through, mode))

    def test_missing_predecessor_fails(self):
        self.assert_status(1, self.invoke(block(2), through=2))

    def test_future_empty_stage_not_required_yet(self):
        self.assert_status(0, self.invoke(block(1) + block(2, "## 尚未开始")))

    def test_headings_comments_separators_and_empty_fences_do_not_count(self):
        for body in ("", " \n\t", "# 概念\n## 关系", "概念\n===\n关系\n---",
                     "<!-- 待补 -->", "```text\n\n```", "---\n***\n___",
                     "## 概念\n<!-- 注释 -->\n~~~python\n~~~"):
            with self.subTest(body=body):
                self.assert_status(1, self.invoke(block(1, body)))

    def test_free_prose_lists_tables_and_code_are_allowed(self):
        for body in (FACT, "- 缓存失效才查远端", "| 对象 | 作用 |\n|---|---|\n| 缓存 | 避免重复读取 |",
                     "```python\n# code comment is still code content\n```", "说明\n\n---\n\n其后仍有内容"):
            with self.subTest(body=body):
                self.assert_status(0, self.invoke(block(1, body)))

    def test_diagrams_stay_inline_and_do_not_require_files(self):
        for language, body in (("plantuml", "@startuml\nA -> B: 读取\n@enduml"),
                               ("mermaid", "flowchart LR\nA-->B"),
                               ("text", "请求 ──> 缓存"), ("ascii", "A -> B")):
            with self.subTest(language=language):
                text = block(1) + block(2, f"~~~{language}\n{body}\n~~~", diagram=True)
                self.assert_status(0, self.invoke(text, through=2))
        self.assertEqual(["work.md"], sorted(p.name for p in self.task.iterdir()))

    def test_missing_empty_or_wrong_kind_diagrams_fail(self):
        for body in ("稍后画图", "[图](graph.puml)", "```mermaid\n```", "```python\nx = 1\n```",
                     "```text\nA -> B\n```\n```mermaid\n```"):
            with self.subTest(body=body):
                self.assert_status(1, self.invoke(block(1, body, diagram=True)))

    def test_no_diagram_declared_does_not_require_one(self):
        self.assert_status(0, self.invoke(block(1)))

    def test_old_source_segment_cannot_fill_new_segment(self):
        old = "".join(block(i, mode="source", run="part-1") for i in range(1, 5))
        new = block(1, "沿用已核实的目标；本段从 ReadState 接到 ApplyState。", mode="source", run="part-2")
        self.assert_status(0, self.invoke(old + new, mode="source", run="part-2"))
        self.assert_status(1, self.invoke(old + new, through=2, mode="source", run="part-2"))
        self.assert_status(0, self.invoke(old + new + block(2, mode="source", run="part-2"),
                                         through=2, mode="source", run="part-2"))

    def test_mode_switch_and_bug_identity(self):
        text = block(1) + block(1, mode="quick", branch="bug", run="bug-1")
        self.assert_status(0, self.invoke(text, mode="quick", branch="bug", run="bug-1"))
        self.assert_status(1, self.invoke(text, mode="quick", run="bug-1"))
        self.assert_status(1, self.invoke(text, mode="quick", run="read-1"))

    def test_duplicates_malformed_metadata_and_unclosed_blocks_fail(self):
        valid = block(1)
        for text in (valid + valid, valid.replace('"stage": 1', '"stage": true'),
                     valid.replace('"diagram": false', '"diagram": "false"'),
                     valid.replace('"stage": 1', '"stage": 1, "stage": 2'),
                     valid.replace('"mode": "standard"', '"mode": []'),
                     valid.replace('"stage": 1', '"stage": 9'),
                     valid.replace('"run": "read-1", ', ''),
                     valid.replace("<!-- /workflow -->", ""),
                     "<!-- /workflow -->", valid.replace("<!-- /workflow -->", valid),
                     valid.replace(FACT, "```mermaid\nA --> B")):
            with self.subTest(text=text):
                self.assert_status(1, self.invoke(text))

    def test_marker_examples_inside_fences_and_comments_are_ignored(self):
        sample = "````markdown\n" + block(2) + "````\n"
        comment = '<!--\nworkflow:{"stage":2}\n这是普通注释，不是阶段。\n-->\n'
        self.assert_status(1, self.invoke(sample + comment + block(1), through=2))
        self.assert_status(0, self.invoke(sample + comment + block(1)))

    def test_custom_filename_and_utf8_bom(self):
        self.assert_status(0, self.invoke("\ufeff" + block(1), file="notes/阶段记录.md"))

    def test_bad_path_missing_file_and_invalid_cli_are_errors(self):
        self.assert_status(2, self.command())
        outside = self.root / "outside.md"
        outside.write_text(block(1), encoding="utf-8")
        self.assert_status(2, self.command(file="../outside.md"))
        (self.task / "linked.md").symlink_to(outside)
        self.assert_status(2, self.command(file="linked.md"))
        self.assert_status(2, self.command(file=str(outside)))
        self.assert_status(2, self.command(mode="source", branch="bug"))
        self.assert_status(2, self.command(mode="quick", through=4))

    def test_non_utf8_is_reported_without_traceback(self):
        (self.task / "work.md").write_bytes(b"\xff\xfe")
        result = self.command()
        self.assert_status(2, result)
        self.assertNotIn("Traceback", result.stderr)

    def test_nonempty_is_not_semantic_approval(self):
        result = self.invoke(block(1, "已检查"))
        self.assert_status(0, result)
        self.assertIn("不证明内容正确", result.stdout)

    def test_read_only_selected_run_and_stages_with_complete_diagram(self):
        diagram = "先说明触发条件。\n\n```plantuml\n@startuml\nA -> B: 读取\n@enduml\n```\n保留完整配套说明。"
        text = ("区块外材料不应被读取。\n" + block(1, "旧轮次内容", run="old") +
                block(1, "本轮无需重读的事实") + block(2, "应读取的完整概念解释") +
                block(3, diagram, diagram=True) + block(4, "不需要的结束记录"))
        result = self.invoke(text, read_stages=[2, 3])
        self.assert_status(0, result)
        self.assertIn("应读取的完整概念解释", result.stdout)
        self.assertIn(diagram, result.stdout)
        for unwanted in ("区块外材料", "旧轮次内容", "无需重读的事实", "不需要的结束记录", "结构检查通过"):
            self.assertNotIn(unwanted, result.stdout)

    def test_read_does_not_require_predecessors_or_replace_validation(self):
        text = block(2, "## 只有标题")
        read = self.invoke(text, read_stages=[2])
        self.assert_status(0, read)
        self.assertIn("## 只有标题", read.stdout)
        self.assertNotIn("检查通过", read.stdout)
        self.assert_status(1, self.command(through=2))

    def test_read_missing_conflicting_or_duplicate_targets_emits_no_partial_content(self):
        for text in (block(1), block(1) + block(2, mode="quick"),
                     block(1) + block(1) + block(2), block(1) + block(2, run="old")):
            with self.subTest(text=text):
                result = self.invoke(text, read_stages=[1, 2])
                self.assert_status(1, result)
                self.assertEqual("", result.stdout)

    def test_read_reflects_disk_revision_and_deduplicates_stage_selection(self):
        self.invoke(block(1) + block(2, "旧说明"))
        result = self.invoke(block(1) + block(2, "修正后的解释"), read_stages=[2, 1, 2])
        self.assert_status(0, result)
        self.assertNotIn("旧说明", result.stdout)
        self.assertEqual(1, result.stdout.count("修正后的解释"))
        self.assertLess(result.stdout.index(FACT), result.stdout.index("修正后的解释"))

    def test_invalid_read_arguments(self):
        for stages in ([], [0], [5]):
            with self.subTest(stages=stages):
                self.assert_status(2, self.command(read_stages=stages))
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--task-dir", str(self.task), "--run", "read-1",
             "--mode", "standard", "--branch", "learning", "--through", "1", "--read-stages", "1"],
            text=True, capture_output=True, check=False,
        )
        self.assert_status(2, result)


if __name__ == "__main__":
    unittest.main()
