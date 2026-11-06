# BoardUI Agent Design Rules

These rules apply when writing UI code for projects using BoardUI (React + Tailwind CSS v4, source-owned components under `components/`).

## 1. Components First

- Before hand-building any UI element, check for an installed BoardUI component under `components/base/` and `components/application/`, and prefer it.
- Missing a component? Install it via BoardUI MCP (`install_components`) or CLI (`npx boardui@latest add <name>`) instead of writing a lookalike.
- Import through the `@/` alias:
  ```tsx
  import { Button } from "@/components/base/buttons/button";
  ```

## 2. Color: Semantic Tokens Only

- Never use raw palette classes (`text-gray-500`, `bg-white`, `border-neutral-200`) or hex/oklch literals. Every color rides a BoardUI semantic token, which makes dark mode automatic.
- **Text:**
  - `text-text-primary`: Primary text headings and body.
  - `text-text-secondary`: Supporting descriptions and subheadings.
  - `text-text-tertiary`: Metadata, timestamps, captions.
  - `text-text-placeholder`: Input placeholder copy.
  - `text-text-error-primary`: Error messages and alert states.
- **Surfaces:**
  - `bg-background-primary-default`: Main card and panel surface.
  - `bg-background-secondary-default` / `-hover`: Secondary containers and interactive rows.
  - `bg-background-tertiary-default`: Subtle inner wells and elevated controls.
  - `bg-background-full`: Canvas and page ground surface.
- **Borders:**
  - `border-border-button-default` / `-hover`: Default control and card borders.
  - `border-separator-border`: Subtle dividers and table hairlines.
  - `border-border-table`: Data table borders.
  - `border-border-error-default`: Validation and error borders.
- **Icons:**
  - `text-foreground-icon-primary` through `text-foreground-icon-quaternary`.
- **Charts:**
  - `chart-1` through `chart-5` tokens (plus `-active` variants).
- **Accents:**
  - `accent-50` through `accent-950` ramp for CTAs, active selections, and brand moments.
- **Dark Mode:**
  - Dark mode flips tokens via the `.dark` class on `<html>`. Never write `dark:` overrides with raw colors.

## 3. Typography: Composite Utilities Only

- Use BoardUI composite type utilities rather than stacking Tailwind text modifiers:
  - `text-title-1-medium`, `text-title-2-medium`, `text-title-3-semibold`
  - `text-headline-medium`
  - `text-body-medium`, `text-body-regular`
  - `text-body-2-medium`, `text-body-2-regular`
  - `text-caption-1-semibold`, `text-caption-1-regular`
- Never rebuild type by stacking `text-sm font-medium leading-5`. Each composite utility synchronizes font size, weight, line-height, and letter-spacing together.

## 4. Spacing and Shape

- **Spacing:** Stay on Tailwind's default spacing scale (`gap-2`, `p-4`, `mt-6`). Prefer flex/grid `gap` over per-child margins.
- **Cards and Panels:** `rounded-3xl` with `border-border-button-default`.
- **Inputs and Menu Rows:** `rounded-md` to `rounded-xl`.
- **Pills and Badges:** `rounded-full`.

## 5. Layout Mechanics & Direction

- **DirectionProvider:** Wrap the application (or a mixed-language region) in `DirectionProvider` from `@/components/foundations/direction/direction` with an explicit BCP 47 `locale` (`ar`, `he`, `en-US`, `zh-CN`).
- **HTML Attributes:** Set matching `lang` and `dir` on `<html>` for full-app RTL. CSS `dir` alone does not configure React Aria keyboard navigation, popover placements, or date pickers.
- **Logical CSS Properties:**
  - Use `ms`/`me` (margin inline start/end) instead of `ml`/`mr`.
  - Use `ps`/`pe` (padding inline start/end) instead of `pl`/`pr`.
  - Use `start`/`end` instead of `left`/`right`.
  - Use `text-start`/`text-end` instead of `text-left`/`text-right`.
  - Use `border-s`/`border-e` and `rounded-s`/`rounded-e`.
- **Directional Mirroring:** Mirror navigation arrows, disclosure glyphs, and drawer transitions in RTL. Keep measured geometry, charts, canvas, code snippets, email addresses, OTP inputs, and URLs in explicit LTR regions.

## 6. Scroll Region Blur Softening

- Internal vertical scroll regions must soften the top edge with a progressive blur and surface fade once scrolled, rather than sharply clipping content.
- Keep headers outside the scroll region.
- Use a stationary, `pointer-events-none`, `aria-hidden` overlay in a relative wrapper:
  1. A 24px masked 1px backdrop blur.
  2. A 16px masked 4px backdrop blur.
  3. A gradient from the enclosing semantic surface token to transparent.
- Ramp layer opacity from 0 to 1 over the first 24px of scrolling. Apply opacity to individual layers, never the overlay parent.

## 7. Class Merging & Component Conventions

- **cx Utility:** Merge class names using `cx()` from `@/utils/cx` (tailwind-merge configured for BoardUI composite text styles). Never use plain string concatenation or unconfigured `clsx`.
- **Icons:** Use RemixIcon glyphs (`@remixicon/react`), passed as component references (`leadingIcon={RiAddLine}`), not pre-rendered elements.
- **Forms:** Build upon React Aria Components. Extend installed BoardUI form components rather than raw `<input>` or `<select>`.
- **Focus States:** Use consistent focus rings:
  ```css
  outline-none focus-visible:ring-2 focus-visible:ring-border-focus-ring
  ```

