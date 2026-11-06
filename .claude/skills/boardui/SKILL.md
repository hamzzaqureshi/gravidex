---
name: boardui
description: React design system for agentic interfaces. Build dashboards and AI products with 69 source components, 400+ semantic tokens, React Aria accessibility, Tailwind CSS v4, RTL/direction support, and agent design rules.
---

# BoardUI

BoardUI is a specialized React design system engineered for agentic interfaces and dashboards. It provides 69 free source components, 400+ semantic tokens, React Aria accessibility, Tailwind CSS v4 compatibility, direction/RTL support, and dedicated agent rules.

Components are source-owned: files live directly in your project under `components/`, giving complete flexibility without library lock-in.

## Workflow

### 1. Component First Selection
Before hand-building any UI element, check for an installed BoardUI component in your project:
- Base components: `components/base/` (buttons, checkboxes, inputs, modals, popovers, tabs, switches).
- Application blocks: `components/application/` (agent-chat, agent-log, agent-thinking, app-shell, data-grid, data-table, stat-cards).
- Foundations: `components/foundations/` (direction, brand, theme, typography, template-copy).

If a component is missing, install it via the CLI:
```bash
npx boardui@latest add <component-name>
```
To install all free items at once:
```bash
npx boardui@latest add --all
```

For the complete catalogue of 69 free components, inspect [components reference](references/components.md).

### 2. Apply Semantic Color Tokens Only
Never use raw palette classes (e.g. `text-gray-500`, `bg-white`, `border-neutral-200`) or hex/oklch literals. Every color rides a BoardUI semantic token, enabling automatic light and dark mode switching via the `.dark` class on `<html>`:
- **Text:** `text-text-primary`, `text-text-secondary`, `text-text-tertiary`, `text-text-placeholder`, `text-text-error-primary`.
- **Surfaces:** `bg-background-primary-default` (cards/panels), `bg-background-secondary-default` (inner containers), `bg-background-tertiary-default` (wells), `bg-background-full` (page ground).
- **Borders:** `border-border-button-default`, `border-separator-border` (dividers), `border-border-table` (tables), `border-border-error-default`.
- **Icons:** `text-foreground-icon-primary` through `text-foreground-icon-quaternary`.
- **Charts:** `chart-1` through `chart-5` (with `-active` variants).
- **Accents & CTAs:** `accent-50` through `accent-950` ramp.

For the full token matrix, inspect [tokens reference](references/tokens.md).

### 3. Use Composite Typography Utilities
Do not stack individual font modifiers (e.g. `text-sm font-medium leading-5`). Use BoardUI's composite type utilities which coordinate size, weight, line-height, and tracking in single classes:
- Page and hero headlines: `text-title-1-medium`, `text-title-2-medium`, `text-title-3-semibold`.
- Stat numbers and section headers: `text-headline-medium`.
- Interactive labels and body copy: `text-body-medium`, `text-body-regular`.
- Secondary actions and table values: `text-body-2-medium`, `text-body-2-regular`.
- Badges and captions: `text-caption-1-semibold`, `text-caption-1-regular`.

### 4. Layout Mechanics & Direction (RTL / LTR)
BoardUI provides native support for Arabic, Hebrew, and other right-to-left languages within the same components:
- **DirectionProvider:** Wrap the app or mixed region with `DirectionProvider` from `@/components/foundations/direction/direction` with an explicit BCP 47 locale (`ar`, `he`, `en-US`, `zh-CN`).
- **HTML Element:** Synchronize `<html lang="ar" dir="rtl">`.
- **Logical CSS Properties:** Always use logical styles:
  - Margins: `ms-*` / `me-*` (inline start/end).
  - Padding: `ps-*` / `pe-*`.
  - Positioning: `start-*` / `end-*`.
  - Text alignment: `text-start` / `text-end`.
  - Borders and radii: `border-s-*` / `border-e-*`, `rounded-s-*` / `rounded-e-*`.
- **Directional Mirroring:** Navigation chevrons, sidebar drawer motions, and disclosure arrows mirror in RTL via `@/utils/directional-icon`.
- **LTR Isolation:** Wrap code blocks, URLs, emails, and OTP digit inputs in explicit LTR regions (`dir="ltr"` or `<bdi>`).

For complete direction guidelines, inspect [RTL reference](references/rtl.md).

### 5. Progressive Scroll Edge Blur
Internal vertical scroll containers must soften the top edge with a progressive blur and surface fade once scrolled, rather than abruptly clipping text:
- Keep headers outside the scroll container.
- Implement a stationary, `pointer-events-none`, `aria-hidden` overlay in a relative wrapper:
  1. A 24px masked 1px backdrop blur.
  2. A 16px masked 4px backdrop blur.
  3. A gradient from the enclosing surface token to transparent.
- Ramp layer opacity from 0 to 1 over the initial 24px of scroll offset.

### 6. Component Conventions & Class Merging
- **Class Merging:** Always merge class names using `cx()` from `@/utils/cx` (tailwind-merge configured for BoardUI composite text styles). Never use plain string concatenation.
- **Icons:** Use RemixIcon glyphs (`@remixicon/react`), passed as component references (`leadingIcon={RiAddLine}`), not pre-rendered JSX elements.
- **Form Primitives:** Build upon React Aria Components. Extend installed BoardUI form components rather than creating raw inputs.
- **Focus Rings:** Apply accessible focus styling: `outline-none focus-visible:ring-2 focus-visible:ring-border-focus-ring`.

For the complete agent rules specification, inspect [rules reference](references/rules.md).

## Offline Component & Token Lookup

You can query components, tokens, and agent rules offline from the terminal using the included lookup script:
```bash
# List components by category
python3 -B scripts/component_lookup.py --list application

# Search components by keyword
python3 -B scripts/component_lookup.py --search chat

# Inspect semantic tokens
python3 -B scripts/component_lookup.py --tokens text

# Print agent rules summary
python3 -B scripts/component_lookup.py --rules
```

## Attribution & Provenance
BoardUI is created by Mertcan Dundar Esmergul ([BoardUI/boardui](https://github.com/BoardUI/boardui)) and licensed under the MIT License.
Preserved upstream snapshot commit: `ec5c5eb3e29c2441be63b9422cd54f411ef23466`.
All component source files and design tokens are integrated under the GraviDex governance protocol with zero external dependencies and strict zero-emoji compliance.

