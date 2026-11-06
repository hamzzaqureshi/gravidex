#!/usr/bin/env python3
"""Lemo-Opuscar Film Style and Director Rule Lookup Utility.

Pure Python standard library CLI tool for querying Lemo-Opuscar film styles,
director rules, pipeline commands, and style categories offline.

Zero external dependencies (Python 3 standard library only).
Strict zero-emoji compliance.
"""

import argparse
import os
import sys
from pathlib import Path

STYLES_DATA = [
    # Edit & Documentary
    {
        "name": "caption-news",
        "display": "Caption News",
        "zh": "字幕新闻",
        "category": "edit-documentary",
        "demo": "The Bee Ledger",
        "description": "Fast-paced news short designed to work with sound off, using animated caption straps and evidence data.",
        "tags": ["news", "caption", "documentary", "text", "fast"]
    },
    {
        "name": "newsreel",
        "display": "1920s Newsreel",
        "zh": "1920s 新闻影片",
        "category": "edit-documentary",
        "demo": "Knock-Knee Alert",
        "description": "Authentic vintage newsreel look with flicker, sepia tone, intertitles, and period musical rhythm.",
        "tags": ["vintage", "newsreel", "1920s", "history", "film"]
    },
    {
        "name": "countdown",
        "display": "Live Countdown Split-screen",
        "zh": "实时倒计时分屏",
        "category": "edit-documentary",
        "demo": "Counting Itself Down",
        "description": "High-tension split-screen launch sequence where 9 cells merge into 1 at ignition.",
        "tags": ["countdown", "split-screen", "launch", "space", "tension"]
    },
    {
        "name": "city-symphony",
        "display": "Time-lapse Symphony",
        "zh": "延时交响",
        "category": "edit-documentary",
        "demo": "One Day in New York",
        "description": "Urban time-lapse rhythm combining historical archive photos with modern city light streams.",
        "tags": ["timelapse", "city", "urban", "symphony", "architecture"]
    },
    {
        "name": "visual-investigation",
        "display": "Visual Investigation",
        "zh": "视觉调查",
        "category": "edit-documentary",
        "demo": "The Hindenburg: Four Minutes, 32 Seconds",
        "description": "Forensic journalistic reconstruction synchronizing multiple eyewitness photos, newsreels, and clocks.",
        "tags": ["investigation", "forensic", "journalism", "archive", "clock"]
    },
    {
        "name": "kino-montage",
        "display": "Constructivist Montage",
        "zh": "构成主义蒙太奇",
        "category": "edit-documentary",
        "demo": "410 Days",
        "description": "Aggressive Soviet-style geometric montage celebrating industrial construction and human labor.",
        "tags": ["constructivist", "montage", "industrial", "geometric", "bold"]
    },
    {
        "name": "telestrator",
        "display": "Sports Telestrator",
        "zh": "体育战术板",
        "category": "edit-documentary",
        "demo": "Freeze Frame",
        "description": "Tactical broadcast breakdown with player freezing, geometric trajectory vectors, and pitch maps.",
        "tags": ["sports", "tactics", "freeze-frame", "vectors", "analysis"]
    },
    {
        "name": "news-package",
        "display": "Broadcast News Package",
        "zh": "电视新闻包装",
        "category": "edit-documentary",
        "demo": "The Week in AI",
        "description": "Complete broadcast television package: rundown, ticker strap, price boards, and spec cards.",
        "tags": ["broadcast", "news", "tv", "rundown", "strap"]
    },

    # Evidence Films
    {
        "name": "satellite-briefing",
        "display": "Satellite Briefing",
        "zh": "卫星简报",
        "category": "evidence",
        "demo": "The Map Still Says Sea",
        "description": "Geospatial satellite survey tracking environmental change, multi-spectral false color, and land recovery.",
        "tags": ["satellite", "geospatial", "earth", "climate", "survey"]
    },
    {
        "name": "briefing-board",
        "display": "Engineering Briefing Board",
        "zh": "工程简报板",
        "category": "evidence",
        "demo": "The Ship Decides",
        "description": "Wall-mounted technical briefing testing infrastructure variants against physical shipping constraints.",
        "tags": ["engineering", "briefing", "infrastructure", "technical", "blueprints"]
    },
    {
        "name": "lidar-survey",
        "display": "LiDAR Survey",
        "zh": "点云测绘",
        "category": "evidence",
        "demo": "The Fields Under the Forest",
        "description": "Laser-scan 3D point cloud stripping tree canopies to uncover ancient stone foundations.",
        "tags": ["lidar", "point-cloud", "survey", "3d", "archaeology"]
    },
    {
        "name": "white-model",
        "display": "Projection on White Model",
        "zh": "白模投影",
        "category": "evidence",
        "demo": "How a Flattened City Grew Back",
        "description": "Architectural white massing model illuminated by projection-mapped urban reconstruction phases.",
        "tags": ["white-model", "architectural", "projection", "city", "reconstruction"]
    },
    {
        "name": "data-physical",
        "display": "Data Physicalization",
        "zh": "数据实物化",
        "category": "evidence",
        "demo": "Two Spirals",
        "description": "Tangible physical data plates stacked into walnut circular dials charting energy shifts.",
        "tags": ["data", "physicalization", "wood", "sculpture", "charts"]
    },
    {
        "name": "teardown",
        "display": "Exploded Teardown",
        "zh": "产品拆解",
        "category": "evidence",
        "demo": "21 Keys, Opened",
        "description": "Technical CAD hardware teardown exploding components in orbiting 3D space with dimension callouts.",
        "tags": ["teardown", "cad", "hardware", "exploded-view", "3d"]
    },
    {
        "name": "microscope",
        "display": "Microscope Story",
        "zh": "显微叙事",
        "category": "evidence",
        "demo": "Measured Blue",
        "description": "Seamless zoom descent from biological slide specimen down into nuclear cell structures.",
        "tags": ["microscope", "biology", "science", "zoom", "cells"]
    },
    {
        "name": "archive-lighttable",
        "display": "Archive Light Table",
        "zh": "档案灯台",
        "category": "evidence",
        "demo": "Two Seconds Short",
        "description": "Forensic examination of historical glass plate negatives under magnifying loupe inspection.",
        "tags": ["archive", "light-table", "loupe", "negatives", "photography"]
    },

    # Hand-drawn & Painting
    {
        "name": "crayon-book",
        "display": "Crayon Picture Book",
        "zh": "蜡笔儿童绘本",
        "category": "hand-drawn",
        "demo": "The Moon Can't Sleep",
        "description": "Soft textured wax crayon children's book aesthetic with warm, rhythmic nursery pacing.",
        "tags": ["crayon", "children", "book", "storybook", "gentle"]
    },
    {
        "name": "watercolor",
        "display": "Watercolor Brush",
        "zh": "水彩笔刷",
        "category": "hand-drawn",
        "demo": "Follow the Rain",
        "description": "Flowing fluid pigment washes that blend, bleed, and dry organically on textured paper.",
        "tags": ["watercolor", "brush", "fluid", "painting", "nature"]
    },
    {
        "name": "ink-wash",
        "display": "Chinese Ink Wash",
        "zh": "中国水墨",
        "category": "hand-drawn",
        "demo": "The Swordsman and the River",
        "description": "Traditional East Asian brushwork with flying white dry-brush strokes and mountain mists.",
        "tags": ["ink", "ink-wash", "chinese", "brush", "martial-arts"]
    },
    {
        "name": "impasto",
        "display": "Impasto Oil Painting",
        "zh": "油画厚涂",
        "category": "hand-drawn",
        "demo": "The Colour of Rain",
        "description": "Richly textured palette knife oil strokes catching directional specular light.",
        "tags": ["impasto", "oil-painting", "texture", "knife", "rich"]
    },
    {
        "name": "one-line",
        "display": "One-line Drawing",
        "zh": "一笔画",
        "category": "hand-drawn",
        "demo": "The Line That Never Lifted",
        "description": "Continuous single unbroken vector line drawing transforming from one scene into another.",
        "tags": ["one-line", "continuous", "vector", "minimalist", "fluid"]
    },
    {
        "name": "whiteboard",
        "display": "Whiteboard Explainer",
        "zh": "白板讲解",
        "category": "hand-drawn",
        "demo": "Einstein in Your Pocket",
        "description": "Scientific whiteboard lecture with dry-erase markers, equation derivations, and hand-drawn graphs.",
        "tags": ["whiteboard", "explainer", "lecture", "diagram", "education"]
    },
    {
        "name": "urban-sketch",
        "display": "Urban Sketch",
        "zh": "钢笔淡彩",
        "category": "hand-drawn",
        "demo": "Where the Wind Went",
        "description": "Crisp fountain pen linework infused with light loose watercolor splashes of urban architecture.",
        "tags": ["urban-sketch", "pen", "fountain-pen", "watercolor", "city"]
    },
    {
        "name": "chalkboard",
        "display": "Chalkboard",
        "zh": "黑板粉笔",
        "category": "hand-drawn",
        "demo": "The Story of Chinese Characters",
        "description": "Textured classroom chalkboard where chalk dust writes, erases, and redraws historical etymologies.",
        "tags": ["chalk", "chalkboard", "classroom", "etymology", "education"]
    },

    # Graphic & Type
    {
        "name": "swiss-motion",
        "display": "Swiss Motion Graphics",
        "zh": "瑞士动态排版",
        "category": "graphic-type",
        "demo": "Five Rules for a Poster",
        "description": "International Typographic Style animated on a strict 12-column grid with extreme scale contrast.",
        "tags": ["swiss", "typography", "grid", "minimal", "beat-synced"]
    },
    {
        "name": "spy-titles",
        "display": "60s Spy Title Sequence",
        "zh": "60s 间谍片头",
        "category": "graphic-type",
        "demo": "The Velvet Cipher",
        "description": "Hard-edged Saul Bass-inspired cutout shapes and jazz brass kinetic typography.",
        "tags": ["spy", "title-sequence", "1960s", "cutout", "kinetic"]
    },
    {
        "name": "art-deco",
        "display": "Art Deco",
        "zh": "装饰艺术",
        "category": "graphic-type",
        "demo": "Midnight at the Starlight Hotel",
        "description": "Geometric gold-leaf filigree, stepped chevrons, and opulent 1930s architectural symmetry.",
        "tags": ["art-deco", "gold", "geometric", "1930s", "luxury"]
    },
    {
        "name": "blueprint",
        "display": "Blueprint",
        "zh": "蓝图 / 工程制图",
        "category": "graphic-type",
        "demo": "Patent Pending: The Cloud Catcher",
        "description": "Cyan engineering paper with white drafting pen vectors, dimension tolerances, and patent stamps.",
        "tags": ["blueprint", "patent", "engineering", "cyan", "drafting"]
    },
    {
        "name": "stained-glass",
        "display": "Stained Glass",
        "zh": "彩色玻璃窗",
        "category": "graphic-type",
        "demo": "The Dragon of the East Window",
        "description": "Cathedral leaded glass windows backlit by moving sunlight projecting stained color shafts.",
        "tags": ["stained-glass", "cathedral", "light", "glass", "gothic"]
    },
    {
        "name": "pictogram-motion",
        "display": "Pictogram Motion",
        "zh": "象形运动图形",
        "category": "graphic-type",
        "demo": "Left Behind",
        "description": "Precise Otto Neurath Isotype-inspired pictograms animating smoothly on musical rhythm.",
        "tags": ["pictogram", "isotype", "icons", "rhythm", "clean"]
    },
    {
        "name": "ascii-crt",
        "display": "ASCII / CRT Terminal",
        "zh": "ASCII / CRT 终端",
        "category": "graphic-type",
        "demo": "Tranquility.log",
        "description": "Amber phosphor monochrome CRT monitor with scanlines, barrel distortion, and ASCII character art.",
        "tags": ["ascii", "crt", "terminal", "retro", "phosphor"]
    },

    # East Asian Traditions
    {
        "name": "shadow-puppet",
        "display": "Shadow Puppetry",
        "zh": "皮影戏",
        "category": "asian-traditions",
        "demo": "Hou Yi Shoots the Suns",
        "description": "Translucent carved leather puppets with articulated joints performing against an illuminated backlit parchment.",
        "tags": ["shadow-puppet", "leather", "chinese", "traditional", "folklore"]
    },
    {
        "name": "ukiyoe",
        "display": "Ukiyo-e",
        "zh": "浮世绘",
        "category": "asian-traditions",
        "demo": "Toward the Mountain",
        "description": "Woodblock printing aesthetic with graduated bokashi ink shading and traditional Japanese perspective.",
        "tags": ["ukiyoe", "woodblock", "japanese", "print", "wave"]
    },
    {
        "name": "papercut-red",
        "display": "Red Paper-cut",
        "zh": "红色窗花剪纸",
        "category": "asian-traditions",
        "demo": "Nian Comes to Town",
        "description": "Traditional Chinese crimson paper folk art with intricate positive/negative silhouette cutting.",
        "tags": ["paper-cut", "red", "chinese", "festival", "silhouette"]
    },
    {
        "name": "paper-lantern",
        "display": "Paper-cut Lightbox",
        "zh": "纸雕灯影",
        "category": "asian-traditions",
        "demo": "The Last Night Train",
        "description": "Layered multi-depth white paper card silhouettes backlit by warm glowing miniature LED stages.",
        "tags": ["lightbox", "paper-cut", "depth", "layers", "shadow"]
    },

    # Materials & 3D
    {
        "name": "brick-toy",
        "display": "Brick Toy",
        "zh": "积木玩具",
        "category": "materials-3d",
        "demo": "Rocket from Spare Parts",
        "description": "Modular plastic construction bricks and mini-figures with stop-motion charm.",
        "tags": ["brick", "lego", "toy", "stop-motion", "plastic"]
    },
    {
        "name": "paper-popup",
        "display": "Paper Pop-up Book",
        "zh": "纸片立体书",
        "category": "materials-3d",
        "demo": "Pip's Paper Adventure",
        "description": "Mechanical pop-up book pages opening, folding, and rotating multi-layered cardstock sets.",
        "tags": ["pop-up", "book", "folding", "papercraft", "3d"]
    },
    {
        "name": "tilt-shift",
        "display": "Tilt-Shift Miniature",
        "zh": "移轴微缩",
        "category": "materials-3d",
        "demo": "Toy Town Rush Hour",
        "description": "Selective shallow depth of field transforming real-scale traffic and urban scenes into miniatures.",
        "tags": ["tilt-shift", "miniature", "dof", "diorama", "bokeh"]
    },
    {
        "name": "lowpoly-island",
        "display": "Low-poly Isometric Island",
        "zh": "低多边形等距",
        "category": "materials-3d",
        "demo": "The Island That Grew",
        "description": "Faceted flat-shaded 3D polygon landscape building itself block by block out of an azure sea.",
        "tags": ["lowpoly", "isometric", "island", "polygonal", "stylized"]
    },
    {
        "name": "glass-product",
        "display": "Glass Product Render",
        "zh": "玻璃质感产品",
        "category": "materials-3d",
        "demo": "Aura — Hear the Light",
        "description": "Studio lighting caustics, dispersion, and refractions sweeping across translucent glass tech hardware.",
        "tags": ["glass", "3d", "product-render", "caustics", "hardware"]
    },
    {
        "name": "memphis-diorama",
        "display": "Memphis Diorama",
        "zh": "孟菲斯微缩景观",
        "category": "materials-3d",
        "demo": "Four Seasons in Pomelo Town",
        "description": "Playful 1980s Memphis Milano geometric patterns, squiggles, pastel volumes, and kinetic dioramas.",
        "tags": ["memphis", "diorama", "geometry", "playful", "pastel"]
    }
]

CATEGORIES = {
    "edit-documentary": "Edit & Documentary (Archival newsreels, split screens, forensic investigations)",
    "evidence": "Evidence Films (Satellite imagery, LiDAR point clouds, white mass models, CAD teardowns)",
    "hand-drawn": "Hand-drawn & Painting (Watercolor, crayon, ink wash, impasto, one-line, chalkboard)",
    "graphic-type": "Graphic & Typography (Swiss motion graphics, 60s spy titles, art deco, blueprints, ASCII CRT)",
    "asian-traditions": "East Asian Traditions (Shadow puppetry, Ukiyo-e, red paper-cut, layered paper lightboxes)",
    "materials-3d": "Materials & 3D (Brick toys, pop-up books, tilt-shift dioramas, glass renders, low-poly)"
}


def list_styles(category=None):
    styles = STYLES_DATA
    if category:
        styles = [s for s in styles if s["category"].lower() == category.lower()]
    print("=" * 72)
    print("                     LEMO-OPUSCAR FILM STYLES")
    print("=" * 72)
    print(f"{'Folder Name':<22} | {'English Display':<26} | {'Chinese':<12}")
    print("-" * 72)
    for s in styles:
        print(f"{s['name']:<22} | {s['display']:<26} | {s['zh']:<12}")
    print("=" * 72)
    print(f"Total Styles Displayed: {len(styles)} (out of 66 available)")


def search_styles(query):
    q = query.lower()
    matches = []
    for s in STYLES_DATA:
        if (q in s["name"].lower() or 
            q in s["display"].lower() or 
            q in s["zh"] or 
            q in s["demo"].lower() or 
            q in s["description"].lower() or 
            any(q in t for t in s["tags"])):
            matches.append(s)
    print("=" * 72)
    print(f"LEMO-OPUSCAR STYLE SEARCH RESULTS FOR: '{query}' ({len(matches)} matches)")
    print("=" * 72)
    for s in matches:
        print(f"Style:       {s['display']} ({s['zh']})")
        print(f"Folder:      styles/{s['name']}/")
        print(f"Category:    {s['category']}")
        print(f"Demo Title:  {s['demo']}")
        print(f"Description: {s['description']}")
        print(f"Tags:        {', '.join(s['tags'])}")
        print("-" * 72)


def show_style(name):
    target = name.lower().strip()
    for s in STYLES_DATA:
        if s["name"] == target or s["display"].lower() == target or target in s["zh"]:
            print("=" * 72)
            print(f"Style:       {s['display']}")
            print(f"Chinese:     {s['zh']}")
            print(f"Folder:      styles/{s['name']}/")
            print(f"Prompt File: $LIB/styles/{s['name']}/STYLE.md")
            print(f"Category:    {s['category']}")
            print(f"Demo Title:  {s['demo']}")
            print(f"Description: {s['description']}")
            print(f"Tags:        {', '.join(s['tags'])}")
            print("=" * 72)
            return True
    print(f"Style '{name}' not found. Use --list to see all available styles.")
    return False


def print_director_rules():
    print("=" * 72)
    print("                    LEMO-OPUSCAR DIRECTOR RULES")
    print("=" * 72)
    print("1. Take the Brief: Decide length (30-60s), language, and must-have shots. Ask once.")
    print("2. Find a Benchmark: Pick 1-2 real reference works for tone and camera grammar.")
    print("3. Shape the Story: One subject, one goal, one turn. Hook in the first 3 seconds.")
    print("4. Native Medium Move: Identify the signature transition only this style can do.")
    print("5. Sound First: Build the audio track before drawing final animation frames.")
    print("6. Frame Function: Implement deterministic window.render = (t) => { ... }.")
    print("7. Empirical Mix: Duck music under narration, normalize with loudnorm -14 LUFS.")
    print("=" * 72)


def list_categories():
    print("=" * 72)
    print("                    LEMO-OPUSCAR STYLE CATEGORIES")
    print("=" * 72)
    for k, v in CATEGORIES.items():
        print(f"[{k:<18}] {v}")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="Lemo-Opuscar Style & Director Lookup Utility")
    parser.add_argument("--list", "-l", type=str, nargs="?", const="all", help="List styles by category")
    parser.add_argument("--search", "-s", type=str, help="Search styles by keyword, name, or tag")
    parser.add_argument("--style", "-c", type=str, help="Show details for a specific style")
    parser.add_argument("--categories", action="store_true", help="List available style categories")
    parser.add_argument("--rules", "-r", action="store_true", help="Print director guidelines summary")

    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args()

    if args.list:
        cat = None if args.list == "all" else args.list
        list_styles(cat)
    elif args.search:
        search_styles(args.search)
    elif args.style:
        show_style(args.style)
    elif args.categories:
        list_categories()
    elif args.rules:
        print_director_rules()

    return 0


if __name__ == "__main__":
    sys.exit(main())

