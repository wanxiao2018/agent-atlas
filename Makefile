.PHONY: serve build check format

serve:
	mkdocs serve

build:
	mkdocs build --strict

format:
	python scripts/normalize_markdown_links.py

check:
	python scripts/normalize_markdown_links.py --check
	python scripts/validate_project.py
	mkdocs build --strict
