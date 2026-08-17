from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
GRAPH = DOCS / "data" / "concept-graph.json"

FORBIDDEN_LITERAL = (
    "这个页面目前是 Agent Atlas",
    "后续会继续补充生活类比",
    "当前阶段：v0.",
)
FORBIDDEN_VERSION = re.compile(r"\bv0\.\d+(?:\.\d+)?\b", re.IGNORECASE)
ALLOWED_STATUS = {"planned", "stub", "developing", "atlas-quality"}
ALLOWED_MATURITY = {"green", "yellow", "red"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_public_markdown(errors: list[str]) -> None:
    files = [ROOT / "README.md", *sorted(DOCS.rglob("*.md"))]
    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for marker in FORBIDDEN_LITERAL:
            if marker in text:
                fail(errors, f"{relative}: forbidden placeholder text: {marker!r}")
        if FORBIDDEN_VERSION.search(text):
            fail(errors, f"{relative}: temporary v0.x version label is not allowed in public Markdown")


def validate_graph(errors: list[str]) -> None:
    data = json.loads(GRAPH.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail(errors, "concept-graph.json: schema_version must be integer 1")

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    ids: set[str] = set()

    for node in nodes:
        node_id = node.get("id")
        if not node_id:
            fail(errors, "concept-graph.json: node without id")
            continue
        if node_id in ids:
            fail(errors, f"concept-graph.json: duplicate node id {node_id!r}")
        ids.add(node_id)

        if node.get("status") not in ALLOWED_STATUS:
            fail(errors, f"concept-graph.json: invalid status for {node_id!r}")
        if node.get("maturity") not in ALLOWED_MATURITY:
            fail(errors, f"concept-graph.json: invalid maturity for {node_id!r}")

        path = node.get("path")
        if path is not None and not (DOCS / path).is_file():
            fail(errors, f"concept-graph.json: missing page for {node_id!r}: {path}")

    for edge in edges:
        source = edge.get("from")
        target = edge.get("to")
        if source not in ids:
            fail(errors, f"concept-graph.json: edge source does not exist: {source!r}")
        if target not in ids:
            fail(errors, f"concept-graph.json: edge target does not exist: {target!r}")
        if not edge.get("type"):
            fail(errors, f"concept-graph.json: edge {source!r}->{target!r} has no type")


def main() -> None:
    errors: list[str] = []
    validate_public_markdown(errors)
    validate_graph(errors)

    if errors:
        print("Project validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("Project validation passed.")


if __name__ == "__main__":
    main()
