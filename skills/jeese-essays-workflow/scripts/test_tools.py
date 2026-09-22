"""Behavior checks for stage artifacts and portable print tools; temporary files only."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import assemble_html
import export_pdf


SCRIPTS = Path(__file__).parent


def block(stage, body="作者把完成与理解区分开，沿一次具体观察推进认识。", run="essay-1"):
    return '<!-- essay:' + json.dumps(dict(run=run, stage=stage)) + ' -->\n' + body + '\n<!-- /essay -->\n'


class StageChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / "work.md"

    def command(self, action, run="essay-1", file="work.md"):
        return subprocess.run([sys.executable, str(SCRIPTS / "check_artifacts.py"),
                               "--task-dir", str(self.root), "--run", run, "--file", file] + action,
                              text=True, capture_output=True)

    def invoke(self, text, through=1):
        self.work.write_text(text)
        result = self.command(["--through", str(through)])
        self.assertEqual(text, self.work.read_text())
        return result

    def test_sequential_checkpoints_and_missing_predecessor(self):
        for stage in range(1, 4):
            text = ''.join(block(n) for n in range(1, stage + 1))
            self.assertEqual(0, self.invoke(text, stage).returncode)
        self.assertEqual(1, self.invoke(block(2), 2).returncode)

    def test_empty_and_malformed_artifacts(self):
        for body in ["", "# 标题\n## 小节", "<!-- 已检查 -->", "---\n***", "```text\n```", "标题\n==="]:
            with self.subTest(body=body):
                self.assertEqual(1, self.invoke(block(1, body)).returncode)
        valid = block(1)
        for text in [valid + valid, valid.replace('"stage": 1', '"stage": true'),
                     valid.replace('"stage": 1', '"stage": 4'),
                     valid.replace('"stage": 1', '"stage": 1, "stage": 2'),
                     valid.replace('"stage": 1', '"stage": 1, "extra": 2'),
                     valid.replace('<!-- /essay -->', ''), '<!-- /essay -->',
                     valid.replace('<!-- /essay -->', valid)]:
            with self.subTest(text=text):
                self.assertEqual(1, self.invoke(text).returncode)

    def test_markers_in_examples_are_not_executed(self):
        text = '````markdown\n' + block(2) + '````\n' + block(1)
        self.assertEqual(0, self.invoke(text).returncode)
        self.assertEqual(1, self.invoke(text, 2).returncode)

    def test_read_exact_selected_content_and_disk_revision(self):
        text = block(1, "第一阶段") + block(2, "完整论述\n\n```text\n一个实际例子\n```") + block(3, "交付结果")
        self.work.write_text(block(1, "旧轮次", run="old") + text)
        result = self.command(["--read-stages", "2"])
        self.assertEqual(0, result.returncode)
        self.assertIn("完整论述\n\n```text\n一个实际例子\n```", result.stdout)
        self.assertNotIn("第一阶段", result.stdout)
        self.assertNotIn("旧轮次", result.stdout)
        self.assertNotIn("结构检查通过", result.stdout)
        self.work.write_text(block(2, "已修正的实际论述"))
        self.assertIn("已修正的实际论述", self.command(["--read-stages", "2"]).stdout)
        self.assertEqual(1, self.command(["--through", "2"]).returncode)

    def test_new_round_requires_own_blocks(self):
        self.work.write_text(''.join(block(n) for n in range(1, 4)) + block(1, run="new"))
        self.assertEqual(0, self.command(["--through", "1"], run="new").returncode)
        self.assertEqual(1, self.command(["--through", "2"], run="new").returncode)

    def test_read_failure_has_no_partial_output(self):
        self.work.write_text(block(1))
        result = self.command(["--read-stages", "1", "2"])
        self.assertEqual(1, result.returncode)
        self.assertEqual("", result.stdout)

    def test_paths_and_cli_errors(self):
        self.assertEqual(2, self.command(["--through", "1"]).returncode)
        for action in [["--through", "4"], ["--read-stages", "0"],
                       ["--through", "1", "--read-stages", "1"]]:
            self.assertEqual(2, self.command(action).returncode)
        with tempfile.TemporaryDirectory() as outside:
            p = Path(outside) / 'outside.md'
            p.write_text(block(1))
            (self.root / 'linked.md').symlink_to(p)
            self.assertEqual(2, self.command(["--through", "1"], file='linked.md').returncode)
            self.assertEqual(2, self.command(["--through", "1"], file=str(p)).returncode)
        self.work.write_bytes(b'\xff\xfe')
        result = self.command(["--through", "1"])
        self.assertEqual(2, result.returncode)
        self.assertNotIn('Traceback', result.stderr)

    def test_nonempty_does_not_prove_style(self):
        result = self.invoke(block(1, "已检查"))
        self.assertEqual(0, result.returncode)
        self.assertIn("不证明内容正确", result.stdout)


class HtmlChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.content = self.root / 'body.html'
        self.content.write_text('<h2>观察</h2><p>普通叙述，<strong>具体判断。</strong></p>')
        self.metadata = self.root / 'meta.json'
        self.metadata.write_text(json.dumps(dict(title='观察 <与> 判断', category='随笔 · 日常', intro='由一件事开始。'), ensure_ascii=False))
        self.output = self.root / 'HTML' / '文章.html'

    def build(self, overwrite=False):
        return assemble_html.assemble(self.content, self.metadata, self.root, self.output, overwrite)

    def test_template_preserves_prose_and_escapes_metadata(self):
        self.assertEqual(0, self.build())
        text = self.output.read_text()
        self.assertIn('观察 &lt;与&gt; 判断', text)
        self.assertIn('<strong>具体判断。</strong>', text)
        self.assertIn('<table class="print-shell">', text)
        self.assertIn('margin-top: 9mm', text)
        self.assertIn('普通叙述，', text)

    def test_local_image_paths_across_directories(self):
        picture = self.root / '文档图片' / '图 1.png'
        picture.parent.mkdir()
        picture.write_bytes(b'fixture-image')
        self.content.write_text('<figure class="figure"><img src="文档图片/图 1.png" alt="桌面的书本"><figcaption><span class="fig-label">FIG.</span>文字保持完整。</figcaption></figure>')
        self.assertEqual(1, self.build())
        self.assertIn('../%E6%96%87%E6%A1%A3%E5%9B%BE%E7%89%87/%E5%9B%BE%201.png', self.output.read_text())
        self.assertIn('文字保持完整。', self.output.read_text())
        self.output = self.root / '同目录.html'
        self.build()
        self.assertNotIn('src="../', self.output.read_text())

    def test_failed_build_preserves_existing_output(self):
        self.build()
        before = self.output.read_bytes()
        self.content.write_text('<p>新内容</p>')
        with self.assertRaises(ValueError):
            self.build()
        for body in ['<p>未闭合', '<script>alert(1)</script>', '<p onclick="x()">内容</p>',
                     '<img src="missing.png" alt="内容">', '<p><a href="javascript:alert(1)">内容</a></p>',
                     '<img src="https://example.com/image.png" alt="内容">']:
            self.content.write_text(body)
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.build(overwrite=True)
            self.assertEqual(before, self.output.read_bytes())
        self.content.write_text('<p>新内容</p>')
        self.build(overwrite=True)
        self.assertIn('新内容', self.output.read_text())

    def test_metadata_tokens_are_not_reexpanded(self):
        self.metadata.write_text(json.dumps(dict(title='{{BODY}}', category='随笔', intro='真实引言')))
        self.build()
        self.assertIn('<h1>{{BODY}}</h1>', self.output.read_text())

    def test_math_and_source_files_are_preserved(self):
        body = '<p>公式：<math display="inline"><msup><mi>x</mi><mn>2</mn></msup></math>。</p>'
        self.content.write_text(body)
        self.build()
        self.assertIn(body, self.output.read_text())
        self.assertEqual(body, self.content.read_text())
        self.output = self.content
        with self.assertRaises(ValueError):
            self.build(overwrite=True)


class PdfChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / '文章 含空格.html'
        self.source.write_text('<p>示例</p>')
        self.output = self.root / '文章.pdf'

    def test_print_command_and_atomic_replacement(self):
        def browser(command, **kwargs):
            self.assertIn('--no-pdf-header-footer', command)
            self.assertIn('--allow-file-access-from-files', command)
            self.assertIn('--virtual-time-budget=20000', command)
            self.assertEqual(self.source.resolve().as_uri(), command[-1])
            self.assertTrue(any(x.startswith('--user-data-dir=') for x in command))
            target = Path(next(x.split('=', 1)[1] for x in command if x.startswith('--print-to-pdf=')))
            self.assertNotEqual(target, self.output)
            target.write_bytes(b'%PDF-1.7\n' + b'fixture ' * 30 + b'\n%%EOF\n')
            return subprocess.CompletedProcess(command, 0, '', '')
        with patch.object(export_pdf, 'find_browser', return_value='browser'), patch.object(export_pdf.subprocess, 'run', side_effect=browser):
            export_pdf.export(self.source, self.output)
            with self.assertRaises(ValueError):
                export_pdf.export(self.source, self.output)
            export_pdf.export(self.source, self.output, overwrite=True)
        self.assertTrue(self.output.read_bytes().startswith(b'%PDF-'))
        self.assertFalse(list(self.root.glob('.essay-print-*')))

    def test_failure_preserves_old_pdf(self):
        self.output.write_bytes(b'previous pdf')
        for result in [subprocess.CompletedProcess([], 1, '', 'failure'), subprocess.CompletedProcess([], 0, '', '')]:
            with patch.object(export_pdf, 'find_browser', return_value='browser'), patch.object(export_pdf.subprocess, 'run', return_value=result):
                with self.assertRaises(ValueError):
                    export_pdf.export(self.source, self.output, overwrite=True)
            self.assertEqual(b'previous pdf', self.output.read_bytes())

    def test_missing_browser_is_actionable(self):
        with patch.object(export_pdf.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(ValueError, '--browser'):
                export_pdf.find_browser()

    def test_timeout_preserves_only_finished_print_result(self):
        def browser(command, **kwargs):
            target = Path(next(x.split('=', 1)[1] for x in command if x.startswith('--print-to-pdf=')))
            target.write_bytes(b'%PDF-1.7\n' + b'fixture ' * 30 + ending)
            raise subprocess.TimeoutExpired(command, 60)
        for ending in [b'', b'\n%%EOF\n']:
            self.output.write_bytes(b'previous pdf')
            with patch.object(export_pdf, 'find_browser', return_value='browser'), patch.object(export_pdf.subprocess, 'run', side_effect=browser):
                if ending:
                    export_pdf.export(self.source, self.output, overwrite=True)
                    self.assertTrue(self.output.read_bytes().endswith(ending))
                else:
                    with self.assertRaises(ValueError):
                        export_pdf.export(self.source, self.output, overwrite=True)
                    self.assertEqual(b'previous pdf', self.output.read_bytes())


if __name__ == '__main__':
    unittest.main()
