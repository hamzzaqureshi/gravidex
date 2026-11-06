---
name: design-systems
description: "Construct and maintain coherent design token systems, aesthetic theme registries, historical Japanese palettes, brand identity marks, and editorial diagrams. Combines 67 design system themes, Sanzo Wada historical color combinations, professional logo engineering, and 45 editorial HTML/SVG diagram specifications."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [design-systems, tokens, color-theory, logo-design, diagrams]
  sources_count: 4
---

# Design Systems

Consolidated capability for authoring, cataloging, and scaling design tokens, historical color harmonies, visual identity marks, and editorial diagrams.

## When to Activate
- Authoring semantic design tokens (color, spacing, typography, elevation).
- Choosing or customizing themes from 67 curated aesthetic families (Bento, Brutalism, Editorial, Neobrutalism).
- Generating WCAG-compliant color palettes using Sanzo Wada historical pigment harmonies.
- Engineering brand logos, wordmarks, monograms, and 16px favicon SVGs.
- Rendering editorial architecture, sequence, state, flowchart, or timeline diagrams.

## When NOT to Activate
- Designing UI screen layouts or interactive flows (use `interface-design`).
- Coding React components (use `frontend-engineering`).

## Core Execution Workflow

1. **Design Token Foundations & Themes:**
   - Define semantic tokens for colors, typography scales, border radii, and spacing units.
   - Consult [references/theme-tokens-catalog.md](references/theme-tokens-catalog.md).

2. **Color Harmony & WCAG Matrix:**
   - Select harmonious duo, trio, or quad palettes from Sanzo Wada 159 historical Japanese pigments.
   - Enforce WCAG AAA/AA contrast ratios for foreground and background pairings.
   - Consult [references/sanzo-wada-palette-matrix.md](references/sanzo-wada-palette-matrix.md).

3. **Brand Identity & Vector Mark Construction:**
   - Design vector marks with clean geometric construction, optical alignment, and 16px monochrome readability.
   - Consult [references/logo-identity-systems.md](references/logo-identity-systems.md).

4. **Editorial & Architectural Diagrams:**
   - Create branded SVG/HTML diagrams across 45 supported types (flowchart, sequence, architecture, ER model).
   - Consult [references/editorial-diagram-design.md](references/editorial-diagram-design.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [theme-tokens-catalog.md](references/theme-tokens-catalog.md) | 67 design system themes, token foundations, component rules | `hamzzaqureshi/gravidex` (`designs`) |
| [sanzo-wada-palette-matrix.md](references/sanzo-wada-palette-matrix.md) | 348 curated palettes, 159 Japanese pigments, WCAG matrix | `hamzzaqureshi/gravidex` (`sanzo-wada-colors`) |
| [logo-identity-systems.md](references/logo-identity-systems.md) | Logo types, clean vector construction, optical refinement, 16px testing | `hamzzaqureshi/gravidex` (`logo-design`) |
| [editorial-diagram-design.md](references/editorial-diagram-design.md) | 45 diagram types, sequence/flowchart/architecture HTML+SVG rendering | `hamzzaqureshi/gravidex` (`diagram-design`) |
