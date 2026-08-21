from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECIPES_DIR = ROOT / "recipes"
TEMPLATE_PATH = ROOT / "templates" / "index.html"
OUTPUT_PATH = ROOT / "index.html"

TITLE_RE = re.compile(r"^#\s+(.+?)\s*$")
STEP_RE = re.compile(r"^\d+\.\s+(.+?)\s*$")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def render_inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    return BOLD_RE.sub(r"<strong>\1</strong>", escaped)


def parse_recipe(path: Path) -> tuple[str, list[str]]:
    title: str | None = None
    steps: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if title is None:
            match = TITLE_RE.match(line)
            if not match:
                raise ValueError(f"{path.name}: 第一条非空行必须是 '# 菜名'")
            title = match.group(1).strip()
            continue

        match = STEP_RE.match(line)
        if match:
            steps.append(match.group(1).strip())
        else:
            raise ValueError(
                f"{path.name}: 仅支持有序步骤，例如 '1. **煸**：...'；当前行为：{line}"
            )

    if title is None:
        raise ValueError(f"{path.name}: 文件为空")
    if not steps:
        raise ValueError(f"{path.name}: 至少需要一个步骤")

    return title, steps


def render_card(title: str, steps: list[str]) -> str:
    items = "\n".join(
        f"        <li>{render_inline(step)}</li>" for step in steps
    )
    return (
        '      <article class="card">\n'
        f"        <h2>{html.escape(title)}</h2>\n"
        "        <ol>\n"
        f"{items}\n"
        "        </ol>\n"
        "      </article>"
    )


def build() -> None:
    recipe_files = sorted(RECIPES_DIR.glob("*.md"), key=lambda p: p.name.casefold())
    if not recipe_files:
        raise SystemExit("recipes/ 中没有 .md 菜谱")

    cards = []
    for path in recipe_files:
        title, steps = parse_recipe(path)
        cards.append(render_card(title, steps))

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    output = template.replace("{{CARDS}}", "\n".join(cards))
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Built {len(cards)} recipe card(s) -> {OUTPUT_PATH.name}")


if __name__ == "__main__":
    build()
