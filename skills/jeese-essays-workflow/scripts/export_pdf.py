#!/usr/bin/env python3
"""Print prepared local HTML with an available Edge/Chrome/Chromium browser.

Uses an isolated temporary browser profile and an atomic PDF replacement.
The calling agent must hold permission to launch the browser and write output.
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def find_browser(explicit=None):
    candidates = [explicit] if explicit else [
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "msedge", "google-chrome", "chromium", "chromium-browser",
    ]
    if not explicit:
        for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"),
                     os.environ.get("LOCALAPPDATA")):
            if base:
                candidates.extend(str(Path(base) / rel) for rel in (
                    "Microsoft/Edge/Application/msedge.exe", "Google/Chrome/Application/chrome.exe"))
    for candidate in candidates:
        located = shutil.which(str(candidate))
        if located:
            return located
    raise ValueError("未找到可用的 Edge、Chrome 或 Chromium；用 --browser 指定现有可执行文件")


def complete_pdf(path):
    if not path.is_file() or path.stat().st_size < 100:
        return False
    with path.open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            return False
        stream.seek(max(0, path.stat().st_size - 1024))
        return b"%%EOF" in stream.read()


def export(source, output, browser=None, overwrite=False, timeout=60):
    source = source.resolve(strict=True)
    output = output.resolve()
    if not source.is_file() or source.suffix.lower() not in {".html", ".htm"}:
        raise ValueError("html 必须是已核对的本地 HTML 文件")
    if output.suffix.lower() != ".pdf":
        raise ValueError("output 必须是 .pdf 文件")
    if output.exists() and not overwrite:
        raise ValueError("目标已存在；明确更新目标时使用 --overwrite")
    executable = find_browser(browser)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".essay-print-", dir=output.parent) as folder:
        work = Path(folder)
        pdf = work / "printed.pdf"
        command = [
            executable, "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-default-browser-check", "--allow-file-access-from-files",
            "--no-pdf-header-footer", "--virtual-time-budget=20000",
            f"--user-data-dir={work / 'profile'}", f"--print-to-pdf={pdf}", source.as_uri(),
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=timeout)
        except subprocess.TimeoutExpired:
            # run() has terminated the launched process. Some Edge builds finish
            # printing but keep running; accept only a completed local PDF.
            if not complete_pdf(pdf):
                raise ValueError("浏览器超时且没有完整 PDF，原目标保持不变") from None
            print("浏览器未及时退出；已结束本次进程并保留带完整结束标记的打印结果。请继续核对页面。", file=sys.stderr)
        else:
            if result.returncode != 0:
                raise ValueError(f"浏览器打印失败（{result.returncode}）：{result.stderr[-1800:]}")
        if not complete_pdf(pdf):
            raise ValueError("浏览器未生成完整 PDF；检查访问权限及 HTML")
        os.replace(pdf, output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--browser", help="现有浏览器可执行文件；不下载或安装浏览器")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        output = export(args.html, args.output, args.browser, args.overwrite)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"PDF 未生成：{exc}\n")
    print(f"PDF 已生成：{output}（需渲染页面后核对版面）")


if __name__ == "__main__":
    main()
