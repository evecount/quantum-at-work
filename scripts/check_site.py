"""Verify that all built HTML pages exist and execute every Python code block in docs/."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

sys.path.insert(0, str(ROOT))


def main() -> None:
    if not SITE.exists():
        raise SystemExit("site/ directory does not exist. Run `mkdocs build --strict` first.")

    md_files = sorted(DOCS.glob("*.md"))
    if len(md_files) < 10:
        raise SystemExit(f"Expected at least 10 markdown chapters in docs/, found {len(md_files)}.")

    code_pattern = re.compile(r"```python
(.*?)```", re.DOTALL)
    executed_blocks = 0

    for md in md_files:
        text = md.read_text(encoding="utf-8")
        for match in code_pattern.finditer(text):
            snippet = match.group(1)
            ns: dict = {}
            try:
                exec(snippet, ns, ns)
                executed_blocks += 1
            except Exception as exc:
                raise SystemExit(f"Python snippet failed in {md.name}:
{snippet}
Error: {exc}") from exc

    print(f"Verified {len(md_files)} markdown chapters and executed {executed_blocks} runnable Python snippets.")


if __name__ == "__main__":
    main()
