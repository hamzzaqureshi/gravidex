---
name: interface-design
description: "Design and critique production user interfaces across web, mobile, and desktop. Combines UI/UX guidelines across 22 frameworks, Apple Human Interface Guidelines (HIG), 9-pass anti-slop redline craft transformation, Swiss grid typography, and motion calibration. Use when designing user interfaces, auditing UI aesthetics, improving UX flows, or polishing AI-generated interfaces."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [ui, ux, apple-hig, anti-slop, typography, motion]
  sources_count: 5
---

# Interface Design

Consolidated capability for designing, reviewing, and transforming digital user interfaces across web, iOS/macOS, mobile, and desktop applications.

## When to Activate
- Designing UI components, layouts, screens, user flows, and forms.
- Reviewing interfaces for Apple Human Interface Guidelines (HIG) compliance and accessibility.
- Unslopping AI-generated interfaces to eliminate purple glows, generic cards, and vibecoded cliches.
- Enforcing Swiss grid typography, editorial density, and high-contrast typographic scales.
- Calibrating interactive motion dials (GSAP ScrollTrigger timelines, restrained transitions <300ms).

## When NOT to Activate
- Implementing production frontend React/Next.js code (use `frontend-engineering`).
- Authoring design tokens, color palette palettes, or raw SVG vectors (use `design-systems`).
- Writing backend services or REST API routes (use `backend-engineering`).

## Core Execution Workflow

1. **Design Hierarchy & Direction:**
   - Establish one bright focal element per view; keep chrome quiet and subordinate.
   - Enforce Swiss typographic discipline: geometric fonts, clear scale ratios, WCAG AAA contrast.
   - Consult [references/ui-ux-guidelines.md](references/ui-ux-guidelines.md).

2. **The 9-Pass Redline Craft Transformation (Unslopping):**
   - Apply the 9-pass audit: Purpose, Spacing, Color hierarchy, Iconography, Copywriting, Typography, Layout composition, Visual craft, and Motion restraint.
   - Consult [references/anti-slop-redline-craft.md](references/anti-slop-redline-craft.md).

3. **Platform Standards & HIG Review:**
   - Ground iOS, iPadOS, macOS, and cross-platform designs in Apple HIG component specifications.
   - Consult [references/apple-human-interface-guidelines.md](references/apple-human-interface-guidelines.md).

4. **Motion & Aesthetic Calibration:**
   - Tune the three creative dials: VARIANCE, MOTION, and DENSITY.
   - Restrain interface animations to <300ms standard easing. Ban generic floating cards and ambient glows.
   - Consult [references/taste-motion-calibration.md](references/taste-motion-calibration.md) and [references/anti-vcode-scorecard.md](references/anti-vcode-scorecard.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [ui-ux-guidelines.md](references/ui-ux-guidelines.md) | 79 styles, 192 product palettes, 74 font pairings, 119 UX guidelines | `hamzzaqureshi/gravidex` (`ui-ux-max`) |
| [apple-human-interface-guidelines.md](references/apple-human-interface-guidelines.md) | Apple HIG rules, mobile/desktop components, Liquid Glass, App Review gates | `dickwu/apple-design-skill` (`apple-design`) |
| [anti-slop-redline-craft.md](references/anti-slop-redline-craft.md) | 9-pass redline craft pass, purposeful visual hierarchy, eliminating AI cliches | `heydamir/unslop` (`unslop`) |
| [taste-motion-calibration.md](references/taste-motion-calibration.md) | Creative dials, GSAP timeline choreography, 12-point preflight checklist | `hamzzaqureshi/gravidex` (`taste`) |
| [anti-vcode-scorecard.md](references/anti-vcode-scorecard.md) | 40-pattern anti-slop code scanner and diagnostic scorecard | `hamzzaqureshi/gravidex` (`anti-vcode`) |
