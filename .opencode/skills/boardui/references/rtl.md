# BoardUI RTL & Direction Architecture

Comprehensive guide for implementing accessible right-to-left (RTL) and bidirectional interfaces with BoardUI.

## 1. Core Direction Architecture

BoardUI provides native support for Arabic, Hebrew, and other right-to-left languages within the same component source code. Direction is not simply a CSS `dir="rtl"` attribute; accessible keyboard navigation, portal attachments, and calendar logic require coordinate synchronization across React Aria Components.

### Root Layout Setup

In your Next.js or React root layout, configure both the document element and the `DirectionProvider`:

```tsx
import { DirectionProvider } from "@/components/foundations/direction/direction";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <DirectionProvider locale="ar">
          {children}
        </DirectionProvider>
      </body>
    </html>
  );
}
```

### Supported BCP 47 Locales
- `ar`: Arabic (RTL layout, Arabic calendar and numerals).
- `he`: Hebrew (RTL layout, Hebrew localization).
- `en-US`: English (LTR layout).
- `zh-CN`: Chinese Simplified (LTR layout).

## 2. Logical CSS Properties

Always write CSS using modern logical properties rather than physical left/right rules:

| Avoid Physical Property | Use Logical Property | Tailwind Utility |
| :--- | :--- | :--- |
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` | `ms-*` / `me-*` |
| `padding-left` / `padding-right` | `padding-inline-start` / `padding-inline-end` | `ps-*` / `pe-*` |
| `left` / `right` | `inset-inline-start` / `inset-inline-end` | `start-*` / `end-*` |
| `text-align: left` / `right` | `text-align: start` / `end` | `text-start` / `text-end` |
| `border-left` / `border-right` | `border-inline-start` / `border-inline-end` | `border-s-*` / `border-e-*` |
| `rounded-l` / `rounded-r` | `rounded-inline-start` / `rounded-inline-end` | `rounded-s-*` / `rounded-e-*` |

## 3. Directional Icon Mirroring

- Navigation arrows, chevrons, sidebar toggle glyphs, and drawer animations must mirror automatically in RTL.
- BoardUI provides `DirectionalIcon` from `@/utils/directional-icon` to mirror directional icons while keeping non-directional icons (e.g. search, settings, profile avatars) unmirrored.
- Custom portal roots should consume `useDirection()`:
  ```tsx
  import { useDirection } from "@/components/foundations/direction/direction";

  export function CustomOverlay() {
    const dir = useDirection();
    return <div dir={dir} className="fixed inset-0 ...">...</div>;
  }
  ```

## 4. LTR Text Isolation Boundaries

Certain data formats must always maintain left-to-right reading order, even inside an RTL interface:
- **Code snippets and logs:** `<pre dir="ltr">` or `<code dir="ltr">`.
- **Email addresses & URLs:** Wrap with `<span dir="ltr">` or `<bdi>`.
- **Phone numbers & OTP input codes:** Explicit LTR container to prevent inverted digit sequencing.
- **Charts, Canvas & Measured Geometry:** Cartesian charts and coordinate canvases maintain physical coordinate systems.

## 5. Separation of Direction and Localization

- Layout direction (`DirectionProvider`) and copy translation (`TemplateCopyProvider`) are separate layers.
- Translating strings to Arabic or Hebrew should be handled through your application's translation catalog or `TemplateCopyProvider`.
- Numbers, currencies, and dates should be formatted with standard `Intl` formatters using the active locale.

