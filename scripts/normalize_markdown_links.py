from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_HEADINGS = {"参考来源", "一手资料", "references", "sources", "primary sources"}

SOURCE_WITH_PUBLISHER = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>[-*+]\s+)?"
    r"(?P<publisher>[^,\n]+),\s*"
    r"(?P<title>[^:\n]+):\s*"
    r"(?P<url>https?://\S+)\s*$"
)

SOURCE_SIMPLE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>[-*+]\s+)?"
    r"(?P<title>[^:\n]+):\s*"
    r"(?P<url>https?://\S+)\s*$"
)

HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")
FENCE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})")


def _is_reference_heading(title: str) -> bool:
    normalized = title.strip().lower()
    return any(key in normalized for key in REFERENCE_HEADINGS)


def normalize_text(text: str) -> tuple[str, int]:
    changed = 0
    out: list[str] = []
    in_fence = False
    fence_char: str | None = None
    in_reference_section = False
    reference_level: int | None = None

    for line in text.splitlines(keepends=True):
        newline = "\n" if line.endswith("\n") else ""
        body = line[:-1] if newline else line

        fence_match = FENCE.match(body)
        if fence_match:
            marker = fence_match.group("fence")
            marker_char = marker[0]
            if not in_fence:
                in_fence = True
                fence_char = marker_char
            elif marker_char == fence_char:
                in_fence = False
                fence_char = None
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        heading_match = HEADING.match(body)
        if heading_match:
            level = len(heading_match.group("hashes"))
            title = heading_match.group("title")
            if _is_reference_heading(title):
                in_reference_section = True
                reference_level = level
            elif in_reference_section and reference_level is not None and level <= reference_level:
                in_reference_section = False
                reference_level = None
            out.append(line)
            continue

        if not in_reference_section:
            out.append(line)
            continue

        match = SOURCE_WITH_PUBLISHER.match(body)
        if match:
            publisher = match.group("publisher").strip()
            title = match.group("title").strip()
            url = match.group("url").strip()
            indent = match.group("indent")
            if "[" not in title and "](" not in title:
                out.append(f"{indent}- {publisher}, [{title}]({url}){newline}")
                changed += 1
                continue

        match = SOURCE_SIMPLE.match(body)
        if match:
            title = match.group("title").strip()
            url = match.group("url").strip()
            indent = match.group("indent")
            if "[" not in title and "](" not in title:
                out.append(f"{indent}- [{title}]({url}){newline}")
                changed += 1
                continue

        out.append(line)

    return "".join(out), changed


def markdown_files() -> list[Path]:
    files = [ROOT / "README.md"]
    docs = ROOT / "docs"
    if docs.exists():
        files.extend(sorted(docs.rglob("*.md")))
    return [path for path in files if path.exists()]


def main() -> None:
    total = 0
    touched: list[str] = []

    for path in markdown_files():
        original = path.read_text(encoding="utf-8")
        normalized, count = normalize_text(original)
        if count:
            path.write_text(normalized, encoding="utf-8")
            total += count
            touched.append(str(path.relative_to(ROOT)))

    if touched:
        print(f"Normalized {total} source link(s) in {len(touched)} file(s):")
        for path in touched:
            print(f"- {path}")
    else:
        print("No naked source-list URLs found in reference sections.")


if __name__ == "__main__":
    main()
