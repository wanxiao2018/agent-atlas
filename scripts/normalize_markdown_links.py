from __future__ import annotations

import argparse
import re
import sys
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
            marker_char = fence_match.group("fence")[0]
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
        if match and "[" not in match.group("title"):
            out.append(
                f"{match.group('indent')}- {match.group('publisher').strip()}, "
                f"[{match.group('title').strip()}]({match.group('url').strip()}){newline}"
            )
            changed += 1
            continue

        match = SOURCE_SIMPLE.match(body)
        if match and "[" not in match.group("title"):
            out.append(
                f"{match.group('indent')}- [{match.group('title').strip()}]"
                f"({match.group('url').strip()}){newline}"
            )
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if normalization would change files")
    args = parser.parse_args()

    total = 0
    touched: list[str] = []

    for path in markdown_files():
        original = path.read_text(encoding="utf-8")
        normalized, count = normalize_text(original)
        if not count:
            continue
        total += count
        touched.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.write_text(normalized, encoding="utf-8")

    if not touched:
        print("Markdown source links are normalized.")
        return

    if args.check:
        print(f"Found {total} non-normalized source link(s) in {len(touched)} file(s):")
        for path in touched:
            print(f"- {path}")
        sys.exit(1)

    print(f"Normalized {total} source link(s) in {len(touched)} file(s):")
    for path in touched:
        print(f"- {path}")


if __name__ == "__main__":
    main()
