#!/usr/bin/env python3
"""Wrap a verified article HTML fragment in the bundled print layout.

The agent converts Markdown to semantic HTML and checks fidelity. This script
does not rewrite prose or parse Markdown. It escapes metadata, validates the
fragment, resolves local image paths, and assembles the calibrated template.
Uses Python 3 standard library only.
"""

import argparse
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote, unquote, urlsplit


ASSETS = Path(__file__).resolve().parent.parent / "assets"
VOID = {"img", "br", "hr", "col"}
ALLOWED = VOID | {
    "p", "h2", "h3", "h4", "h5", "h6", "strong", "em", "b", "i", "s",
    "a", "span", "div", "section", "figure", "figcaption", "blockquote",
    "ul", "ol", "li", "pre", "code", "table", "thead", "tbody", "tfoot",
    "tr", "th", "td", "caption", "colgroup", "sup", "sub", "small",
    "math", "mrow", "mi", "mn", "mo", "mtext", "mspace", "mfrac",
    "msup", "msub", "msubsup", "msqrt", "mroot", "mover", "munder",
    "munderover", "mtable", "mtr", "mtd", "mfenced", "semantics", "annotation",
}


class Fragment(HTMLParser):
    def __init__(self, source_dir, output_dir):
        super().__init__(convert_charrefs=False)
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.parts = []
        self.stack = []
        self.has_text = False
        self.image_count = 0

    def local_url(self, value, image=False):
        url = urlsplit(value)
        if url.scheme or url.netloc:
            if not image and url.scheme in {"https", "http", "mailto"}:
                return value
            raise ValueError("图片使用本地实体文件；链接仅支持 http、https、mailto 或本地路径")
        if not url.path:
            if image:
                raise ValueError("图片 src 不能为空")
            return value
        path = (self.source_dir / unquote(url.path)).resolve()
        if image:
            if not path.is_file():
                raise ValueError(f"图片不存在：{path}")
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}:
                raise ValueError(f"不是支持的实体图片：{path.name}")
        relative = quote(Path(os.path.relpath(path, self.output_dir)).as_posix(), safe="/")
        if url.query:
            relative += "?" + url.query
        if url.fragment:
            relative += "#" + url.fragment
        return relative

    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED:
            raise ValueError(f"正文片段不支持 <{tag}>；仅提供正文语义标签，页面骨架由模板生成")
        seen = set()
        values = {}
        for key, value in attrs:
            if key in seen:
                raise ValueError(f"重复属性：{tag}.{key}")
            seen.add(key)
            if key.startswith("on") or key in {"style", "srcset", "srcdoc", "background"}:
                raise ValueError(f"正文不支持属性 {key}；样式由 print.css 提供")
            value = value or ""
            if key == "src":
                if tag != "img":
                    raise ValueError("src 只用于实体图片")
                value = self.local_url(value, image=True)
            elif key == "href":
                if tag != "a":
                    raise ValueError("href 只用于链接")
                value = self.local_url(value)
            values[key] = value
        if tag == "img":
            if not values.get("src") or not values.get("alt", "").strip():
                raise ValueError("图片须有真实 src 和说明内容的 alt")
            self.image_count += 1
        attrs_text = "".join(f' {key}="{html.escape(value, quote=True)}"' for key, value in values.items())
        self.parts.append(f"<{tag}{attrs_text}>")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            raise ValueError(f"正文标签未正确闭合：{tag}")
        self.stack.pop()
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            self.has_text = True
        self.parts.append(html.escape(data, quote=False))

    def handle_entityref(self, name):
        self.has_text = True
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.has_text = True
        self.parts.append(f"&#{name};")

    def finish(self):
        self.close()
        if self.stack:
            raise ValueError("正文存在未闭合标签：" + ", ".join(self.stack))
        if not self.has_text:
            raise ValueError("正文没有文字内容")
        return "".join(self.parts)


def assemble(content, metadata, source_dir, output, overwrite=False):
    content = content.resolve(strict=True)
    metadata = metadata.resolve(strict=True)
    source_dir = source_dir.resolve(strict=True)
    output = output.resolve()
    if not source_dir.is_dir():
        raise ValueError("source-dir 必须是正文来源目录")
    if output.suffix.lower() != ".html":
        raise ValueError("output 必须是 .html 文件")
    if output in {content, metadata, ASSETS / "print.html", ASSETS / "print.css"}:
        raise ValueError("输出不能覆盖输入或 Skill 模板")
    if output.exists() and not overwrite:
        raise ValueError("目标已存在；明确更新目标时使用 --overwrite")
    meta = json.loads(metadata.read_text(encoding="utf-8-sig"))
    if not isinstance(meta, dict) or set(meta) != {"title", "category", "intro"}:
        raise ValueError("metadata 须包含且只包含 title、category、intro")
    if any(not isinstance(v, str) or not v.strip() for v in meta.values()):
        raise ValueError("标题、分类和引言须为非空字符串")
    fragment = Fragment(source_dir, output.parent)
    fragment.feed(content.read_text(encoding="utf-8-sig"))
    body = fragment.finish()
    fields = {key.upper(): html.escape(value, quote=True) for key, value in meta.items()}
    fields["BODY"] = body
    fields["STYLE"] = (ASSETS / "print.css").read_text(encoding="utf-8")
    template = (ASSETS / "print.html").read_text(encoding="utf-8")
    tokens = re.findall(r"\{\{([A-Z]+)\}\}", template)
    if set(tokens) != set(fields):
        raise ValueError("模板字段与脚本不一致")
    result = re.sub(r"\{\{([A-Z]+)\}\}", lambda match: fields[match[1]], template)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent,
                                     prefix=".essay-html-", suffix=".tmp", delete=False) as f:
        temp = Path(f.name)
        f.write(result)
    try:
        os.replace(temp, output)
    finally:
        temp.unlink(missing_ok=True)
    return fragment.image_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", required=True, type=Path, help="核对过的正文 HTML 片段")
    parser.add_argument("--metadata", required=True, type=Path, help="title/category/intro 的 JSON 文件")
    parser.add_argument("--source-dir", required=True, type=Path, help="原 Markdown 所在目录，片段图片从这里解析")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        count = assemble(args.content, args.metadata, args.source_dir, args.output, args.overwrite)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"HTML 未生成：{exc}\n")
    print(f"HTML 已生成：{args.output.resolve()}（实体图片 {count} 张；仍需核对正文和打印效果）")


if __name__ == "__main__":
    main()
