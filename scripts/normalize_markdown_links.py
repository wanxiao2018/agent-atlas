from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Normalize source-list lines such as:
# Anthropic, Building Effective Agents: https://example.com/article
# - OpenAI, New tools for building agents: https://example.com/post
# into:
# - Anthropic, [Building Effective Agents](https://example.com/article)
SOURCE_LINE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>[-*+]\s+)?"
    r"(?P<publisher>[^,\n]+),\s*"
    r"(?P<title>[^:\n]+):\s*"
    r"(?P<url>https?://\S+)\s*$"
)


def normalize_text(text: str) -> tuple[str, int]:
    changed = 0
    out: list[str] = []

    for line in text.splitlines(keepends=True):
        newline = "\n" if line.endswith("\n") else ""
        body = line[:-1] if newline else line
        match = SOURCE_LINE.match(body)

        if not match:
            out.append(line)
            continue

        publisher = match.group("publisher").strip()
        title = match.group("title").strip()
        url = match.group("url").strip()
        indent = match.group("indent")

        # Already-normalized Markdown links are intentionally ignored.
        if "[" in title or "](" in title:
            out.append(line)
            continue

        out.append(f"{indent}- {publisher}, [{title}]({url}){newline}")
        changed += 1

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
        print("No naked source-list URLs found.")


if __name__ == "__main__":
    main()
