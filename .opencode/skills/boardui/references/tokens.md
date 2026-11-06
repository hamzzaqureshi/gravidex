# BoardUI Semantic Tokens & Design Foundations

Reference guide for BoardUI's 400+ semantic tokens, typography composite utilities, and layout foundations.

## 1. Color Token Architecture

BoardUI enforces semantic token usage exclusively. Raw Tailwind colors (e.g. `bg-white`, `text-gray-500`, `border-neutral-200`) or raw hex/oklch color literals must never be used. Every token resolves to variable values that adapt automatically between light and dark modes.

### Text Tokens
| Token Class | Light Appearance | Dark Appearance | Usage Role |
| :--- | :--- | :--- | :--- |
| `text-text-primary` | High contrast ink | Near white | Headings, hero copy, primary labels, table values |
| `text-text-secondary` | Medium neutral | Muted silver | Secondary descriptions, subheadings, unselected tabs |
| `text-text-tertiary` | Subtle neutral | Dim gray | Timestamps, metadata, footnotes, breadcrumb segments |
| `text-text-placeholder`| Faint neutral | Dark muted gray | Input placeholder text, disabled copy |
| `text-text-error-primary`| Semantic red | Bright red | Validation errors, destructive action confirmation |

### Surface & Background Tokens
| Token Class | Usage Role |
| :--- | :--- |
| `bg-background-full` | Root canvas / page ground surface behind all cards and sidebars |
| `bg-background-primary-default` | Primary elevated surface (cards, modals, dropdown menus, sidebars) |
| `bg-background-secondary-default` | Secondary container surface, table headers, inner wells |
| `bg-background-secondary-hover` | Hover state for interactive secondary surfaces |
| `bg-background-tertiary-default` | Subtle recessed wells, code snippets, search input backgrounds |

### Border & Separator Tokens
| Token Class | Usage Role |
| :--- | :--- |
| `border-border-button-default` | Default border for cards, buttons, inputs, and container outlines |
| `border-border-button-hover` | Elevated border on control hover |
| `border-separator-border` | Subtle hairline dividers between list rows and navigation groups |
| `border-border-table` | Table grid lines and header boundaries |
| `border-border-error-default` | Error state outline for failed inputs or dangerous confirmation alerts |
| `ring-border-focus-ring` | Focus ring outline for accessible keyboard focus states |

### Icon Foreground Tokens
| Token Class | Usage Role |
| :--- | :--- |
| `text-foreground-icon-primary` | High-emphasis icons (navigation active icons, primary button icons) |
| `text-foreground-icon-secondary` | Standard interactive icons (sidebar navigation, action triggers) |
| `text-foreground-icon-tertiary` | Supporting icons (dropdown chevrons, search indicators) |
| `text-foreground-icon-quaternary` | Decorative background glyphs, disabled icon indicators |

### Chart & Accent Tokens
- **Chart Palette:** `chart-1`, `chart-2`, `chart-3`, `chart-4`, `chart-5` (with corresponding `-active` variants for selected bars and data points).
- **Accent Ramp:** `accent-50`, `accent-100`, `accent-200`, `accent-300`, `accent-400`, `accent-500`, `accent-600`, `accent-700`, `accent-800`, `accent-900`, `accent-950`. Used for primary call-to-actions, active selection rings, and brand identity.

## 2. Typography: Composite Utilities

Each composite typography utility in BoardUI sets font-size, font-weight, line-height, and letter-spacing together in a single rule. Do not stack separate font-size and weight classes.

| Composite Utility Class | Intended Usage |
| :--- | :--- |
| `text-title-1-medium` | Page titles, hero headlines |
| `text-title-2-medium` | Modal titles, major section headers |
| `text-title-3-semibold` | Card headers, panel titles |
| `text-headline-medium` | Emphasized feature labels, stat numbers |
| `text-body-medium` | Default interactive elements (buttons, primary form inputs) |
| `text-body-regular` | Long-form reading paragraphs, conversational chat text |
| `text-body-2-medium` | Secondary action triggers, table cells |
| `text-body-2-regular` | Supporting descriptions, notification body copy |
| `text-caption-1-semibold` | Badge labels, stat delta chips |
| `text-caption-1-regular` | Timestamps, character counters, helper captions |

## 3. Shapes and Radii

- **Cards, Panels & Shells:** `rounded-3xl` paired with `border border-border-button-default`.
- **Inputs, Buttons & Menus:** `rounded-md` to `rounded-xl`.
- **Pills, Badges & Toggles:** `rounded-full`.
- **Focus States:** `outline-none focus-visible:ring-2 focus-visible:ring-border-focus-ring`.

## 4. Dark Mode Architecture

BoardUI flips color tokens via the `.dark` class applied to the root `<html>` element.
- Never write explicit `dark:` overrides with raw colors (e.g. `dark:bg-[#121212]` or `dark:text-white`).
- If a token combination does not provide sufficient contrast in dark mode, select a different semantic token, never an arbitrary color value.

