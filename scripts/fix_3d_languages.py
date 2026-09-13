#!/usr/bin/env python3
"""Replace the 3D graph language pie (commit-primary-language) with repo language bytes."""

from __future__ import annotations

import json
import math
import os
import pathlib
import re
import ssl
import urllib.request

USER = os.environ.get("GITHUB_USER", "vrelay")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HIDE = {"HTML", "CSS"}
TOP_N = 5
SIZE_WEIGHT = 0.5
COUNT_WEIGHT = 0.5
PIE_START = re.compile(r'<g transform="translate\(\s*40\s*,\s*520\s*\)">')

LANG_COLORS = {
    "TypeScript": "#3178c6",
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "Go": "#00ADD8",
    "Jupyter Notebook": "#DA5B0B",
    "Shell": "#89e051",
    "Dockerfile": "#384d54",
    "C++": "#f34b7d",
    "C": "#555555",
    "Rust": "#dea584",
    "other": "#444444",
}


def api(path: str) -> object:
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "vrelay-profile",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30) as resp:
        return json.load(resp)


def language_shares() -> list[tuple[str, float, str]]:
    repos = api(f"/users/{USER}/repos?per_page=100&type=owner")
    assert isinstance(repos, list)
    sizes: dict[str, int] = {}
    counts: dict[str, int] = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        langs = api(f"/repos/{USER}/{repo['name']}/languages")
        assert isinstance(langs, dict)
        langs = {k: int(v) for k, v in langs.items() if k not in HIDE}
        if not langs:
            continue
        for name, size in langs.items():
            sizes[name] = sizes.get(name, 0) + size
        primary = max(langs, key=langs.get)
        counts[primary] = counts.get(primary, 0) + 1

    names = set(sizes) | set(counts)
    if not names:
        raise SystemExit("no languages found")
    max_size = max(sizes.values()) if sizes else 1
    max_count = max(counts.values()) if counts else 1
    scored = []
    for name in names:
        score = (
            SIZE_WEIGHT * (sizes.get(name, 0) / max_size)
            + COUNT_WEIGHT * (counts.get(name, 0) / max_count)
        )
        scored.append((name, score, LANG_COLORS.get(name, "#888888")))
    scored.sort(key=lambda item: -item[1])
    top = scored[:TOP_N]
    rest = sum(item[1] for item in scored[TOP_N:])
    if rest > 0:
        top.append(("other", rest, LANG_COLORS["other"]))
    return top


def polar(cx: float, cy: float, r: float, angle: float) -> tuple[float, float]:
    return cx + r * math.sin(angle), cy - r * math.cos(angle)


def donut_slice(start: float, end: float, outer: float, inner: float) -> str:
    large = 1 if end - start > math.pi else 0
    ox1, oy1 = polar(0, 0, outer, start)
    ox2, oy2 = polar(0, 0, outer, end)
    ix1, iy1 = polar(0, 0, inner, start)
    ix2, iy2 = polar(0, 0, inner, end)
    return (
        f"M{ox1:.3f},{oy1:.3f}"
        f"A{outer:.3f},{outer:.3f},0,{large},1,{ox2:.3f},{oy2:.3f}"
        f"L{ix2:.3f},{iy2:.3f}"
        f"A{inner:.3f},{inner:.3f},0,{large},0,{ix1:.3f},{iy1:.3f}"
        "Z"
    )


def pie_group(langs: list[tuple[str, float, str]]) -> str:
    height = 260.0
    radius = height / 2
    margin = radius / 10
    outer = radius - margin
    inner = radius / 2
    row = 8
    font = height / row / 1.5
    offset = (row - len(langs)) / 2 + 0.5
    total = sum(score for _, score, _ in langs) or 1
    parts = ['<g transform="translate(40, 520)">', '<g transform="translate(273, 0)">']
    for i, (name, score, color) in enumerate(langs):
        y = (i + offset) * (height / row)
        parts.append(
            f'<rect x="0" y="{y - font / 2:.4f}" width="{font:.4f}" height="{font:.4f}" '
            f'fill="{color}" class="stroke-bg" stroke-width="1px"></rect>'
        )
        parts.append(
            f'<text dominant-baseline="middle" x="{font * 1.2:.4f}" y="{y:.4f}" '
            f'class="fill-fg" font-size="{font}px">{name}</text>'
        )
    parts.append("</g>")
    parts.append('<g transform="translate(130, 130)">')
    angle = 0.0
    for name, score, color in langs:
        sweep = (score / total) * 2 * math.pi
        end = angle + sweep
        if sweep >= 2 * math.pi - 1e-6:
            path = (
                f"M0,{-outer:.3f}A{outer:.3f},{outer:.3f},0,1,1,0,{outer:.3f}"
                f"A{outer:.3f},{outer:.3f},0,1,1,0,{-outer:.3f}"
                f"M0,{-inner:.3f}A{inner:.3f},{inner:.3f},0,1,0,0,{inner:.3f}"
                f"A{inner:.3f},{inner:.3f},0,1,0,0,{-inner:.3f}Z"
            )
        else:
            path = donut_slice(angle, end, outer, inner)
        parts.append(
            f'<path d="{path}" style="fill: {color};" class="stroke-bg" stroke-width="2px">'
            f"<title>{name}</title></path>"
        )
        angle = end
    parts.append("</g></g>")
    return "".join(parts)


def replace_pie(svg: str, pie: str) -> str:
    match = PIE_START.search(svg)
    if not match:
        raise SystemExit("pie group not found")
    start = match.start()
    depth = 0
    k = start
    while k < len(svg):
        if svg.startswith("<g ", k) or svg.startswith("<g>", k):
            depth += 1
            k += 2
            continue
        if svg.startswith("</g>", k):
            depth -= 1
            if depth == 0:
                return svg[:start] + pie + svg[k + 4 :]
            k += 4
            continue
        k += 1
    raise SystemExit("unclosed pie group")


def main() -> None:
    langs = language_shares()
    print("languages:", ", ".join(f"{n} {s:.3f}" for n, s, _ in langs))
    pie = pie_group(langs)
    root = pathlib.Path("profile-3d-contrib")
    updated = 0
    for path in sorted(root.glob("*.svg")):
        text = path.read_text()
        if not PIE_START.search(text):
            print(f"skip {path.name}")
            continue
        path.write_text(replace_pie(text, pie))
        print(f"updated {path.name}")
        updated += 1
    if updated == 0:
        raise SystemExit("no 3D SVGs had a language pie to replace")


if __name__ == "__main__":
    main()
