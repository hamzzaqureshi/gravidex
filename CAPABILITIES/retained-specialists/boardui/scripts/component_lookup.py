#!/usr/bin/env python3
"""BoardUI Component, Semantic Token, and Agent Rule Lookup Utility.

Pure Python standard library tool for querying BoardUI components,
design tokens, layout conventions, and installation commands offline.

Zero external dependencies (Python 3 standard library only).
Strict zero-emoji compliance.
"""

import argparse
import json
import os
import sys

COMPONENTS_DATA = [
    # Application Blocks
    {
        "name": "agent-chat",
        "category": "application",
        "display": "Agent Chat",
        "description": "Full chat application with app sidebar, streaming message stream, thinking indicator, composer pill with stop control, and local thread history rail.",
        "install": "npx boardui@latest add agent-chat",
        "tags": ["chat", "agent", "streaming", "threads", "ai"]
    },
    {
        "name": "agent-log",
        "category": "application",
        "display": "Agent Log",
        "description": "Streaming execution logger with ticker reveal, blur-in transitions, and self-drawing hierarchical guide trees. Used for task execution and web research.",
        "install": "npx boardui@latest add agent-log",
        "tags": ["log", "agent", "streaming", "tree", "tasks"]
    },
    {
        "name": "agent-thinking",
        "category": "application",
        "display": "Agent Thinking",
        "description": "Thinking indicator for chat composers with dot wave, dot spin, star shimmer, and infinity variants, elapsed timer, and label shimmer.",
        "install": "npx boardui@latest add agent-thinking",
        "tags": ["thinking", "indicator", "spinner", "agent", "composer"]
    },
    {
        "name": "app-shell",
        "category": "application",
        "display": "App Shell",
        "description": "Adaptive application page frame with collapsible sidebar, mobile phone drawer, responsive topbar, and card container.",
        "install": "npx boardui@latest add app-shell",
        "tags": ["layout", "shell", "sidebar", "responsive", "frame"]
    },
    {
        "name": "auth-card",
        "category": "application",
        "display": "Auth Card",
        "description": "Sign-in and sign-up cards with 24 social authentication providers (stacked or icon row), email validation, and submit actions.",
        "install": "npx boardui@latest add auth-card",
        "tags": ["auth", "login", "signup", "oauth", "card"]
    },
    {
        "name": "composer-loader",
        "category": "application",
        "display": "Composer Loader",
        "description": "Iridescent orbital light rim animation with soft inward bloom that wraps the chat composer during agent execution.",
        "install": "npx boardui@latest add composer-loader",
        "tags": ["composer", "loader", "animation", "agent", "glow"]
    },
    {
        "name": "data-grid",
        "category": "application",
        "display": "Data Grid",
        "description": "Virtualized spreadsheet with editable cells, range selections, multi-column filters, column resizing, undo/redo history, and CSV export.",
        "install": "npx boardui@latest add data-grid",
        "tags": ["grid", "spreadsheet", "virtualized", "table", "editing"]
    },
    {
        "name": "data-table",
        "category": "application",
        "display": "Data Table",
        "description": "TanStack Table integration featuring multi-column sorting, row selection checkboxes, pagination, and filter drawers.",
        "install": "npx boardui@latest add data-table",
        "tags": ["table", "tanstack", "pagination", "sorting", "filtering"]
    },
    {
        "name": "important-alerts-card",
        "category": "application",
        "display": "Important Alerts Card",
        "description": "Scrollable alert feed with status circles, timestamps, and dismissal actions.",
        "install": "npx boardui@latest add important-alerts-card",
        "tags": ["alerts", "notifications", "feed", "card"]
    },
    {
        "name": "notification-center",
        "category": "application",
        "display": "Notification Center",
        "description": "Tabbed notification drawer with read/unread statuses, category tabs, user avatars, and inline trigger actions.",
        "install": "npx boardui@latest add notification-center",
        "tags": ["notifications", "drawer", "inbox", "activity"]
    },
    {
        "name": "orders-chart-card",
        "category": "application",
        "display": "Orders Chart Card",
        "description": "Bar chart card displaying 12-month order volumes against prior year with count-up headline and delta chip.",
        "install": "npx boardui@latest add orders-chart-card",
        "tags": ["chart", "bar-chart", "kpi", "card", "orders"]
    },
    {
        "name": "patient-info-card",
        "category": "application",
        "display": "Patient Info Card",
        "description": "Structured profile metadata card featuring avatar, demographic metrics, and key-value rows.",
        "install": "npx boardui@latest add patient-info-card",
        "tags": ["profile", "medical", "card", "metadata"]
    },
    {
        "name": "revenue-chart-card",
        "category": "application",
        "display": "Revenue Chart Card",
        "description": "Interactive area chart comparing annual revenue trends against prior year with monthly hover inspection and delta badges.",
        "install": "npx boardui@latest add revenue-chart-card",
        "tags": ["chart", "area-chart", "revenue", "card", "finance"]
    },
    {
        "name": "settings-modal",
        "category": "application",
        "display": "Settings Modal",
        "description": "Multi-tab settings dialog containing General, Profile, Agent Tools, and Storage configuration sections.",
        "install": "npx boardui@latest add settings-modal",
        "tags": ["settings", "modal", "dialog", "tabs", "preferences"]
    },
    {
        "name": "sidebar",
        "category": "application",
        "display": "Sidebar",
        "description": "Floating dashboard navigation bar with organization switcher, nav items, announcement slot, and user profile menu.",
        "install": "npx boardui@latest add sidebar",
        "tags": ["navigation", "sidebar", "menu", "dashboard"]
    },
    {
        "name": "stat-cards",
        "category": "application",
        "display": "Stat Cards",
        "description": "Metric KPI card row with trend indicators, delta percentages, and sparkline references.",
        "install": "npx boardui@latest add stat-cards",
        "tags": ["kpi", "stats", "cards", "metrics", "delta"]
    },
    {
        "name": "theme-toggle",
        "category": "application",
        "display": "Theme Toggle",
        "description": "Manual light/dark mode control with circular clip-path reveal animation and local persistence.",
        "install": "npx boardui@latest add theme-toggle",
        "tags": ["theme", "dark-mode", "toggle", "switch"]
    },

    # Base Components
    {
        "name": "button",
        "category": "base",
        "display": "Button",
        "description": "Primary, secondary, ghost, and danger buttons in sm/md/lg sizes with leading and trailing icon slots.",
        "install": "npx boardui@latest add button",
        "tags": ["button", "action", "input"]
    },
    {
        "name": "button-group",
        "category": "base",
        "display": "Button Group",
        "description": "Row of secondary buttons fused into one bordered control with hairline dividers and selectable items.",
        "install": "npx boardui@latest add button-group",
        "tags": ["button", "group", "segmented"]
    },
    {
        "name": "checkbox",
        "category": "base",
        "display": "Checkbox",
        "description": "Accessible checkbox with animated checkmark, indeterminate state, and focus ring.",
        "install": "npx boardui@latest add checkbox",
        "tags": ["checkbox", "input", "selection"]
    },
    {
        "name": "checkbox-card",
        "category": "base",
        "display": "Checkbox Card",
        "description": "Bordered selectable card driven by an integrated checkbox control.",
        "install": "npx boardui@latest add checkbox-card",
        "tags": ["checkbox", "card", "selection"]
    },
    {
        "name": "dialog",
        "category": "base",
        "display": "Dialog / Modal",
        "description": "Accessible modal dialog built on React Aria with focus trap, backdrop blur, and escape key handling.",
        "install": "npx boardui@latest add dialog",
        "tags": ["modal", "dialog", "overlay", "popup"]
    },
    {
        "name": "dropdown-menu",
        "category": "base",
        "display": "Dropdown Menu",
        "description": "Action menu with submenus, keyboard navigation, and checkable items.",
        "install": "npx boardui@latest add dropdown-menu",
        "tags": ["dropdown", "menu", "context-menu"]
    },
    {
        "name": "dropdown-select",
        "category": "base",
        "display": "Dropdown Select",
        "description": "Form select menu with custom trigger, item search filtering, and icon support.",
        "install": "npx boardui@latest add dropdown-select",
        "tags": ["select", "form", "dropdown", "picker"]
    },
    {
        "name": "input",
        "category": "base",
        "display": "Input",
        "description": "Single-line text input with label, leading/trailing icons, error text, and clear button.",
        "install": "npx boardui@latest add input",
        "tags": ["input", "text", "form", "field"]
    },
    {
        "name": "popover",
        "category": "base",
        "display": "Popover",
        "description": "Floating anchored card with smart viewport edge detection and outside dismiss.",
        "install": "npx boardui@latest add popover",
        "tags": ["popover", "floating", "overlay"]
    },
    {
        "name": "segmented-control",
        "category": "base",
        "display": "Segmented Control",
        "description": "Pill-style segmented switcher with sliding highlight pill animation.",
        "install": "npx boardui@latest add segmented-control",
        "tags": ["segmented", "toggle", "tabs", "pills"]
    },
    {
        "name": "switch",
        "category": "base",
        "display": "Switch",
        "description": "Smooth toggle switch with skeuomorphic thumb styling in two sizes.",
        "install": "npx boardui@latest add switch",
        "tags": ["switch", "toggle", "boolean"]
    },
    {
        "name": "tabs",
        "category": "base",
        "display": "Tabs",
        "description": "Underline and pill tab variants built on React Aria with keyboard navigation.",
        "install": "npx boardui@latest add tabs",
        "tags": ["tabs", "navigation", "sections"]
    },
    {
        "name": "textarea",
        "category": "base",
        "display": "Textarea",
        "description": "Auto-growing multiline input with character counter and validation states.",
        "install": "npx boardui@latest add textarea",
        "tags": ["textarea", "multiline", "input"]
    },
    {
        "name": "tooltip",
        "category": "base",
        "display": "Tooltip",
        "description": "Light-surface tooltip built on React Aria with arrow pointer.",
        "install": "npx boardui@latest add tooltip",
        "tags": ["tooltip", "hint", "hover"]
    },
    {
        "name": "tree-view",
        "category": "base",
        "display": "Tree View",
        "description": "Hierarchical folder tree with expand/collapse, active node styling, and guides.",
        "install": "npx boardui@latest add tree-view",
        "tags": ["tree", "folders", "hierarchy", "navigation"]
    },

    # Foundations
    {
        "name": "direction",
        "category": "foundations",
        "display": "Direction Provider",
        "description": "React context provider delivering layout direction, locale, and RTL coordination for React Aria interactions.",
        "install": "npx boardui@latest add direction",
        "tags": ["rtl", "direction", "locale", "bidi", "arabic", "hebrew"]
    },
    {
        "name": "directional-icon",
        "category": "foundations",
        "display": "Directional Icons",
        "description": "Dynamic icon wrapper that mirrors directional arrows in RTL while preserving symmetric icons.",
        "install": "npx boardui@latest add directional-icon",
        "tags": ["icons", "rtl", "mirror", "arrows"]
    },
    {
        "name": "cx",
        "category": "foundations",
        "display": "cx Utility",
        "description": "Tailwind-merge wrapper aware of BoardUI composite text styles and conflict resolution.",
        "install": "npx boardui@latest add cx",
        "tags": ["utility", "classnames", "tailwind", "cx"]
    },
    {
        "name": "theme",
        "category": "foundations",
        "display": "Theme Tokens",
        "description": "400+ semantic tokens covering light/dark surfaces, borders, text, charts, accents, and shadows.",
        "install": "npx boardui@latest add theme",
        "tags": ["theme", "tokens", "colors", "dark-mode"]
    },
    {
        "name": "typography",
        "category": "foundations",
        "display": "Typography Tokens",
        "description": "Composite font utilities combining size, weight, leading, and tracking into single Tailwind classes.",
        "install": "npx boardui@latest add typography",
        "tags": ["typography", "type-scale", "fonts", "composite"]
    },
    {
        "name": "rules",
        "category": "foundations",
        "display": "Agent Rules",
        "description": "Always-on design rules for AI coding agents installed as AGENTS.md or .cursor/rules/boardui.mdc.",
        "install": "npx boardui@latest add rules",
        "tags": ["rules", "agents", "prompts", "conventions"]
    }
]

TOKENS_DATA = {
    "text": [
        ("text-text-primary", "Headings, hero copy, primary labels, table values"),
        ("text-text-secondary", "Secondary descriptions, subheadings, unselected tabs"),
        ("text-text-tertiary", "Timestamps, metadata, footnotes, breadcrumb segments"),
        ("text-text-placeholder", "Input placeholder text, disabled copy"),
        ("text-text-error-primary", "Validation errors, destructive action confirmation")
    ],
    "surface": [
        ("bg-background-full", "Root canvas and page ground surface behind all cards"),
        ("bg-background-primary-default", "Primary elevated surface (cards, modals, dropdowns, sidebars)"),
        ("bg-background-secondary-default", "Secondary container surface, table headers, inner wells"),
        ("bg-background-secondary-hover", "Hover state for interactive secondary surfaces"),
        ("bg-background-tertiary-default", "Subtle inner wells, code snippets, search input grounds")
    ],
    "border": [
        ("border-border-button-default", "Default border for cards, buttons, inputs, and container outlines"),
        ("border-border-button-hover", "Elevated border on control hover"),
        ("border-separator-border", "Subtle hairline dividers between list rows and nav groups"),
        ("border-border-table", "Table grid lines and header boundaries"),
        ("border-border-error-default", "Error state outline for failed inputs or alerts"),
        ("ring-border-focus-ring", "Focus ring outline for keyboard accessibility")
    ],
    "typography": [
        ("text-title-1-medium", "Page titles, hero headlines"),
        ("text-title-2-medium", "Modal titles, major section headers"),
        ("text-title-3-semibold", "Card headers, panel titles"),
        ("text-headline-medium", "Emphasized feature labels, stat numbers"),
        ("text-body-medium", "Default interactive elements (buttons, primary form inputs)"),
        ("text-body-regular", "Long-form reading paragraphs, conversational chat text"),
        ("text-body-2-medium", "Secondary action triggers, table cells"),
        ("text-body-2-regular", "Supporting descriptions, notification body copy"),
        ("text-caption-1-semibold", "Badge labels, stat delta chips"),
        ("text-caption-1-regular", "Timestamps, character counters, helper captions")
    ]
}


def list_components(category=None):
    comps = COMPONENTS_DATA
    if category:
        comps = [c for c in comps if c["category"].lower() == category.lower()]
    print("=" * 72)
    print("                      BOARDUI COMPONENT CATALOGUE")
    print("=" * 72)
    print(f"{'Name':<24} | {'Category':<14} | {'Description'}")
    print("-" * 72)
    for c in comps:
        desc = c["description"]
        if len(desc) > 30:
            desc = desc[:27] + "..."
        print(f"{c['name']:<24} | {c['category']:<14} | {desc}")
    print("=" * 72)
    print(f"Total Components Shown: {len(comps)}")


def search_components(query):
    q = query.lower()
    matches = []
    for c in COMPONENTS_DATA:
        if q in c["name"].lower() or q in c["description"].lower() or any(q in t for t in c["tags"]):
            matches.append(c)
    print("=" * 72)
    print(f"BOARDUI SEARCH RESULTS FOR: '{query}' ({len(matches)} matches)")
    print("=" * 72)
    for c in matches:
        print(f"Component:   {c['display']} ({c['name']})")
        print(f"Category:    {c['category']}")
        print(f"Description: {c['description']}")
        print(f"Install:     {c['install']}")
        print("-" * 72)


def show_component(name):
    target = name.lower().strip()
    for c in COMPONENTS_DATA:
        if c["name"] == target or c["display"].lower() == target:
            print("=" * 72)
            print(f"Component:   {c['display']}")
            print(f"Identifier:  {c['name']}")
            print(f"Category:    {c['category']}")
            print(f"Description: {c['description']}")
            print(f"Install:     {c['install']}")
            print(f"Tags:        {', '.join(c['tags'])}")
            print("=" * 72)
            return True
    print(f"Component '{name}' not found. Use --list to see available components.")
    return False


def list_tokens(category=None):
    print("=" * 72)
    print("                   BOARDUI SEMANTIC TOKEN REGISTRY")
    print("=" * 72)
    cats = [category] if category and category in TOKENS_DATA else TOKENS_DATA.keys()
    for cat in cats:
        print(f"\n[Category: {cat.upper()}]")
        print(f"{'Token Class':<32} | {'Description'}")
        print("-" * 72)
        for token, desc in TOKENS_DATA[cat]:
            print(f"{token:<32} | {desc}")
    print("=" * 72)


def print_rules():
    print("=" * 72)
    print("                    BOARDUI AGENT DESIGN RULES")
    print("=" * 72)
    print("1. Components First: Check components/base and components/application first.")
    print("2. Semantic Tokens Only: Never use raw colors or hex. Tokens flip light/dark.")
    print("3. Composite Typography: Use text-title-*, text-body-*, text-caption-* utilities.")
    print("4. Spacing & Shapes: rounded-3xl for cards, rounded-md/xl for inputs, rounded-full for pills.")
    print("5. RTL & Layout Direction: Use DirectionProvider and logical properties (ms/me, ps/pe).")
    print("6. Progressive Scroll Blur: Soften top edge of scroll areas with masked blur gradient.")
    print("7. Class Merging: Always merge classes with cx() from @/utils/cx.")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="BoardUI Component, Token & Rules Lookup Utility")
    parser.add_argument("--list", "-l", choices=["all", "application", "base", "foundations"], nargs="?", const="all", help="List components")
    parser.add_argument("--search", "-s", type=str, help="Search components by keyword or tag")
    parser.add_argument("--component", "-c", type=str, help="Show details for a specific component")
    parser.add_argument("--tokens", "-t", choices=["all", "text", "surface", "border", "typography"], nargs="?", const="all", help="List semantic tokens")
    parser.add_argument("--rules", "-r", action="store_true", help="Print agent design rules summary")

    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args()

    if args.list:
        cat = None if args.list == "all" else args.list
        list_components(cat)
    elif args.search:
        search_components(args.search)
    elif args.component:
        show_component(args.component)
    elif args.tokens:
        cat = None if args.tokens == "all" else args.tokens
        list_tokens(cat)
    elif args.rules:
        print_rules()

    return 0


if __name__ == "__main__":
    sys.exit(main())

