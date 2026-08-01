#!/usr/bin/env python3
"""Validate the mechanical structure of courseware outline and script Markdown."""

from __future__ import annotations

import argparse
import glob
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence


PAGE_HEADING_RE = re.compile(
    r"^###\s+第\s*(\d+)\s*页(?:\s*[｜|]\s*(.+?))?\s*$", re.MULTILINE
)
FIELD_RE = re.compile(r"^-\s*([^:：\n]+?)\s*[:：]\s*(.*)$")
BATCH_RE = re.compile(r"当前批次\s*[:：]\s*第\s*(\d+)\s*[–—-]\s*(\d+)\s*页")
PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|XXX|PLACEHOLDER)\b|\{\{.+?\}\}|[\[【]\s*(?:待补|待定|待确认|占位)[^\]】]*[\]】]|(?:待补充|待完善)",
    re.IGNORECASE,
)

REQUIRED_FIELDS = (
    "页码",
    "页面类型",
    "核心问题",
    "教学目标",
    "固定母版文字",
    "本页文字",
    "公式与符号",
    "预期可见公式",
    "视觉方案",
    "本页结论",
    "内容来源",
    "禁止添加",
    "核验点",
)
OUTLINE_FIELDS = ("页码", "页面类型", "核心问题", "来源材料")


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("`", "")).strip()


def _parse_pages(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    matches = list(PAGE_HEADING_RE.finditer(text))
    pages = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        fields: dict[str, str] = {}
        current_field = None
        for line in block.splitlines():
            field_match = FIELD_RE.match(line)
            if field_match:
                current_field = field_match.group(1).strip()
                fields[current_field] = field_match.group(2).strip()
            elif current_field and line.strip():
                fields[current_field] += "\n" + line.strip()
        pages.append(
            {
                "number": int(match.group(1)),
                "title": _clean(match.group(2) or ""),
                "fields": fields,
                "block": block,
                "path": path,
            }
        )
    return pages


def _duplicates(values: Iterable[int]) -> list[int]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _page_number(value: str) -> int | None:
    match = re.search(r"\d+", _clean(value))
    return int(match.group()) if match else None


def validate_courseware(
    outline_path: Path | str,
    script_paths: Sequence[Path | str],
    batch_size: int = 5,
    allow_partial: bool = False,
) -> list[str]:
    """Return deterministic validation errors; an empty list means pass."""
    errors: list[str] = []
    outline_path = Path(outline_path)
    script_paths = [Path(path) for path in script_paths]

    if batch_size < 1:
        return ["批次大小必须大于 0。"]
    if not outline_path.is_file():
        return [f"目录文件不存在：{outline_path}"]
    missing_files = [str(path) for path in script_paths if not path.is_file()]
    if missing_files:
        return [f"脚本文件不存在：{path}" for path in missing_files]
    if not script_paths:
        return ["未提供详细脚本文件。"]

    outline_pages = _parse_pages(outline_path)
    if not outline_pages:
        return ["目录中未找到「### 第 N 页｜标题」页面记录。"]

    outline_numbers = [page["number"] for page in outline_pages]
    for duplicate in _duplicates(outline_numbers):
        errors.append(f"目录存在重复页码：{duplicate}。")
    outline_unique = sorted(set(outline_numbers))
    expected_outline = list(range(1, max(outline_unique) + 1))
    missing_outline = sorted(set(expected_outline) - set(outline_unique))
    if missing_outline:
        errors.append(f"目录页码不连续，缺少：{missing_outline}。")

    outline_by_number = {}
    for page in outline_pages:
        outline_by_number.setdefault(page["number"], page)
        for field in OUTLINE_FIELDS:
            if not page["fields"].get(field, "").strip():
                errors.append(f"目录第 {page['number']} 页缺少字段「{field}」。")
        page_value = page["fields"].get("页码", "")
        if page_value and _page_number(page_value) != page["number"]:
            errors.append(f"目录第 {page['number']} 页的「页码」字段不一致。")

    pages_by_file: dict[Path, list[dict]] = {}
    all_script_pages: list[dict] = []
    for path in script_paths:
        pages = _parse_pages(path)
        pages_by_file[path] = pages
        all_script_pages.extend(pages)
        if not pages:
            errors.append(f"脚本文件未包含页面记录：{path}。")

    script_numbers = [page["number"] for page in all_script_pages]
    for duplicate in _duplicates(script_numbers):
        errors.append(f"详细脚本存在重复页码：{duplicate}。")

    script_unique = sorted(set(script_numbers))
    outline_set = set(outline_unique)
    script_set = set(script_unique)
    extras = sorted(script_set - outline_set)
    if extras:
        errors.append(f"详细脚本包含目录外页码：{extras}。")
    if script_unique:
        expected_scripts = (
            [number for number in expected_outline if number <= max(script_unique)]
            if allow_partial
            else expected_outline
        )
        missing_scripts = sorted(set(expected_scripts) - script_set)
        if missing_scripts:
            errors.append(f"缺少详细脚本页：{missing_scripts}。")
        if allow_partial and min(script_unique) != 1:
            errors.append("分批检查必须从第 1 页开始，不能跳过前缀页。")
    elif not errors:
        errors.append("详细脚本中未找到页面记录。")

    total_pages = max(outline_unique)
    for path, pages in pages_by_file.items():
        if not pages:
            continue
        text = path.read_text(encoding="utf-8-sig")
        declaration = BATCH_RE.search(text)
        actual_numbers = sorted(set(page["number"] for page in pages))
        actual_start, actual_end = actual_numbers[0], actual_numbers[-1]
        if not declaration:
            errors.append(f"脚本文件缺少「当前批次」声明：{path}。")
        else:
            declared = (int(declaration.group(1)), int(declaration.group(2)))
            if declared != (actual_start, actual_end):
                errors.append(
                    f"脚本文件的批次声明 {declared[0]}-{declared[1]} "
                    f"与实际页 {actual_start}-{actual_end} 不一致：{path}。"
                )
        expected_start = ((actual_start - 1) // batch_size) * batch_size + 1
        expected_end = min(expected_start + batch_size - 1, total_pages)
        expected_batch = set(range(expected_start, expected_end + 1))
        if actual_start != expected_start or set(actual_numbers) != expected_batch:
            errors.append(
                f"脚本文件批次范围错误：应为 {expected_start}-{expected_end}，"
                f"实际为 {actual_numbers}；文件 {path}。"
            )

    for page in all_script_pages:
        number = page["number"]
        fields = page["fields"]
        for field in REQUIRED_FIELDS:
            if not fields.get(field, "").strip():
                errors.append(f"详细脚本第 {number} 页缺少字段「{field}」。")
        page_value = fields.get("页码", "")
        if page_value and _page_number(page_value) != number:
            errors.append(f"详细脚本第 {number} 页的「页码」字段不一致。")
        placeholder = PLACEHOLDER_RE.search(page["block"])
        if placeholder:
            errors.append(
                f"详细脚本第 {number} 页存在未解决占位符：{placeholder.group(0)}。"
            )

        outline_page = outline_by_number.get(number)
        if not outline_page:
            continue
        if page["title"] != outline_page["title"]:
            errors.append(
                f"第 {number} 页的目录标题不一致："
                f"目录「{outline_page['title']}」，脚本「{page['title']}」。"
            )
        for field in ("页面类型", "核心问题"):
            outline_value = _clean(outline_page["fields"].get(field, ""))
            script_value = _clean(fields.get(field, ""))
            if outline_value and script_value and outline_value != script_value:
                errors.append(f"第 {number} 页的「{field}」与目录不一致。")

    return errors


def _expand_paths(patterns: Sequence[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            paths.extend(Path(match) for match in matches)
        else:
            paths.append(Path(pattern))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate courseware outline and detailed-script Markdown files."
    )
    parser.add_argument("--outline", required=True, help="Path to the complete outline Markdown")
    parser.add_argument("--scripts", required=True, nargs="+", help="Script files or glob patterns")
    parser.add_argument("--batch-size", type=int, default=5, help="Pages per batch (default: 5)")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Allow a complete, contiguous prefix of the outline during batch checks",
    )
    args = parser.parse_args()

    errors = validate_courseware(
        Path(args.outline),
        _expand_paths(args.scripts),
        batch_size=args.batch_size,
        allow_partial=args.allow_partial,
    )
    if errors:
        print(f"[FAIL] {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("[PASS] Courseware Markdown structure is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
