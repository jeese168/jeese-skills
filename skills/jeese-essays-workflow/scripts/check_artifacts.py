#!/usr/bin/env python3
"""Read-only structural checks and scoped reads of Markdown stage artifacts.

No semantic scoring, Markdown rendering, network access, or file writes.
See references/workflow.md for the marker contract.
"""

import argparse
import json
import re
import sys
from pathlib import Path


STAGE_COUNT = 3
FIELDS = {"run", "stage"}
START = re.compile(r"^<!-- essay:(\{.*\}) -->$")
END = "<!-- /essay -->"
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


class InvalidArtifact(ValueError):
    pass


def opening_fence(line):
    match = FENCE.match(line)
    if not match or (match[1][0] == "`" and "`" in match[2]):
        return None
    info = match[2].strip().split()
    return match[1], info[0].lower() if info else ""


def closing_fence(line, fence):
    return re.fullmatch(r" {0,3}" + re.escape(fence[0]) +
                        "{" + str(len(fence)) + r",}[ \t]*", line) is not None


def validate_metadata(meta, line):
    prefix = f"第 {line} 行"
    if not isinstance(meta, dict) or set(meta) != FIELDS:
        raise InvalidArtifact(f"{prefix}：标记须且只包含 {', '.join(sorted(FIELDS))}")
    if not isinstance(meta["run"], str) or not meta["run"].strip():
        raise InvalidArtifact(f"{prefix}：run 必须是非空字符串")
    stage = meta["stage"]
    if type(stage) is not int or not 1 <= stage <= STAGE_COUNT:
        raise InvalidArtifact(f"{prefix}：stage 超出本路径范围")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复字段 {key}")
        result[key] = value
    return result


def parse_blocks(text):
    blocks = []
    active = None
    body = []
    fence = None
    comment = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if fence:
            if active is not None:
                body.append(line)
            if closing_fence(line, fence):
                fence = None
            continue
        if comment:
            if active is not None:
                body.append(line)
            if "-->" in line:
                comment = False
            continue
        opened = opening_fence(line)
        if opened:
            fence = opened[0]
            if active is not None:
                body.append(line)
            continue
        match = START.fullmatch(stripped)
        if match:
            if active is not None:
                raise InvalidArtifact(f"第 {number} 行：阶段标记不能嵌套")
            try:
                meta = json.loads(match[1], object_pairs_hook=unique_keys)
            except ValueError as exc:
                raise InvalidArtifact(f"第 {number} 行：标记 JSON 无效（{exc}）") from exc
            validate_metadata(meta, number)
            active = (meta, number)
            body = []
        elif stripped == END:
            if active is None:
                raise InvalidArtifact(f"第 {number} 行：结束标记没有对应的阶段")
            blocks.append((active[0], "\n".join(body), active[1]))
            active = None
        elif stripped.startswith(("<!-- essay:", "<!-- /essay")):
            raise InvalidArtifact(f"第 {number} 行：阶段标记格式无效")
        else:
            if active is not None:
                body.append(line)
            if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:
                comment = True
    if active is not None:
        raise InvalidArtifact(f"第 {active[1]} 行：阶段未闭合，请检查代码块和结束标记")
    return blocks


def has_content(body):
    """Exclude headings/comments/empty fences; leave prose and table style free."""
    prose = []
    code_blocks = []
    fence = None
    code = []
    language = ""
    for line in body.splitlines():
        if fence:
            if closing_fence(line, fence):
                code_blocks.append((language, "\n".join(code).strip()))
                fence = None
            else:
                code.append(line)
        else:
            opened = opening_fence(line)
            if opened:
                fence, language = opened
                code = []
            else:
                prose.append(line)
    prose = re.sub(r"<!--.*?-->", "", "\n".join(prose), flags=re.S).splitlines()
    has_prose = False
    for i, line in enumerate(prose):
        value = line.strip()
        if not value or re.match(r"^#{1,6}(?:\s|$)", value):
            continue
        # Setext headings and thematic breaks are not stage content.
        if i + 1 < len(prose) and re.fullmatch(r" {0,3}(?:=+|-+)\s*", prose[i + 1]):
            continue
        if re.fullmatch(r"[\s*_=|:\-]+", value):
            continue
        has_prose = True
    return has_prose or any(code for _, code in code_blocks)


def select_blocks(text, run, stages):
    selected = {}
    errors = []
    for meta, body, line in parse_blocks(text):
        if meta["run"] != run:
            continue
        stage = meta["stage"]
        if stage in selected:
            errors.append(f"第 {line} 行：run={run} 的阶段 {stage} 重复")
        selected[stage] = (meta, body, line)
    for stage in stages:
        if stage not in selected:
            errors.append(f"run={run} 缺少阶段 {stage}")
    return selected, errors


def check(text, run, through):
    stages = range(1, through + 1)
    selected, errors = select_blocks(text, run, stages)
    for stage in stages:
        if stage not in selected:
            continue
        meta, body, line = selected[stage]
        if not has_content(body):
            errors.append(f"第 {line} 行：阶段 {stage} 只有标题、注释、空白或空代码块")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-dir", required=True, type=Path)
    parser.add_argument("--file", default="work.md", help="任务目录内的 Markdown 相对路径")
    parser.add_argument("--run", required=True, help="本轮文章写作的唯一标识")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--through", type=int, help="结构检查到第几阶段（包含前置阶段）")
    action.add_argument("--read-stages", type=int, nargs="+", help="只读取指定阶段正文，不替代结构检查")
    args = parser.parse_args()
    stages = args.read_stages if args.read_stages is not None else [args.through]
    if not args.run.strip() or any(not 1 <= stage <= STAGE_COUNT for stage in stages):
        parser.error("run 不能为空，阶段号必须在本路径阶段范围内")
    try:
        task_dir = args.task_dir.resolve(strict=True)
        if not task_dir.is_dir():
            raise ValueError("task-dir 不是目录")
        if Path(args.file).is_absolute():
            raise ValueError("file 必须是任务目录内的相对路径")
        path = (task_dir / args.file).resolve(strict=True)
        path.relative_to(task_dir)
        if not path.is_file() or path.suffix.lower() != ".md":
            raise ValueError("file 必须指向 Markdown 文件")
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"无法检查：{exc}", file=sys.stderr)
        return 2
    try:
        if args.read_stages is not None:
            stages = sorted(set(args.read_stages))
            selected, errors = select_blocks(text, args.run, stages)
        else:
            errors = check(text, args.run, args.through)
    except InvalidArtifact as exc:
        errors = [str(exc)]
    if errors:
        print("区块读取未完成：" if args.read_stages is not None else "结构检查未通过：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.read_stages is not None:
        # Output exact body text, not a generated summary. Never emit unrelated stages.
        for stage in stages:
            meta, body, _ = selected[stage]
            print("<!-- essay:" + json.dumps(meta, ensure_ascii=False) + " -->")
            print(body)
            print(END)
        return 0
    print(f"结构检查通过：{args.run}，阶段 1–{args.through}。")
    print("仅确认标记和非空区块；不证明内容正确、表达充分或实际执行顺序。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
