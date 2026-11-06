# BoardUI Component Catalogue

Complete reference of the 69 free source components, application blocks, and foundations in BoardUI.

## 1. Application Blocks (16 Blocks)

High-level composed application blocks, agent UI interfaces, and complete panels.

| Block Name | Purpose & Structure | CLI Install Command |
| :--- | :--- | :--- |
| **Agent Chat** | Full chat application with app sidebar, streaming message stream, thinking indicator, composer pill with cancel/stop action, and local chat history thread rail. | `npx boardui@latest add agent-chat` |
| **Agent Log** | Streaming execution logger with ticker reveal, blur-in transitions, self-drawing hierarchical guide trees. Used for task execution lists and web research traces. | `npx boardui@latest add agent-log` |
| **Agent Thinking** | Thinking indicator for chat composers with dot wave, dot spin, star shimmer, and infinity variants, elapsed time counter, and text pulse. | `npx boardui@latest add agent-thinking` |
| **App Shell** | Adaptive application frame with collapsible sidebar, mobile phone drawer, responsive topbar, and card wrappers. | `npx boardui@latest add app-shell` |
| **Auth Card** | Unified sign-in and sign-up card with 24 social authentication providers (stacked or icon row), email validation, and submit actions. | `npx boardui@latest add auth-card` |
| **Composer Loader** | Iridescent orbital light rim animation with soft inward bloom that wraps the chat composer during agent execution. | `npx boardui@latest add composer-loader` |
| **Data Grid** | Virtualized high-performance spreadsheet with editable cells, range selections, multi-column filters, column resizing, undo/redo history, and CSV export. | `npx boardui@latest add data-grid` |
| **Data Table** | TanStack Table integration featuring multi-column sorting, row selection checkboxes, pagination, and filter drawers. | `npx boardui@latest add data-table` |
| **Important Alerts Card** | Scrollable notification and alert feed with semantic status circles, timestamps, and dismissal actions. | `npx boardui@latest add important-alerts-card` |
| **Notification Center** | Tabbed notification drawer with read/unread statuses, category tabs, user avatars, and inline trigger actions. | `npx boardui@latest add notification-center` |
| **Orders Chart Card** | Bar chart comparison card displaying 12-month order volumes against prior year with rolling count-up header and delta chip. | `npx boardui@latest add orders-chart-card` |
| **Patient Info Card** | Specialized profile metadata card featuring user avatar, demographic metrics, and structured key-value rows. | `npx boardui@latest add patient-info-card` |
| **Revenue Chart Card** | Interactive area chart comparing annual revenue trends against prior year with monthly hover inspection and delta badges. | `npx boardui@latest add revenue-chart-card` |
| **Settings Modal** | Multi-tab settings dialog containing General, Profile, Agent Tools, and Storage configuration sections. | `npx boardui@latest add settings-modal` |
| **Sidebar** | Floating dashboard navigation bar with organization switcher, nav items, announcement slot, and user profile menu. | `npx boardui@latest add sidebar` |
| **Stat Cards** | Metric KPI row with trend indicators, delta percentages, and sparkline references. | `npx boardui@latest add stat-cards` |
| **Theme Toggle** | Light/dark mode control with circular clip-path reveal animation and local storage persistence. | `npx boardui@latest add theme-toggle` |

## 2. Base Components (39 Components)

Core interactive UI building blocks built on React Aria Components.

| Component Name | Category | Description & Features | CLI Install Command |
| :--- | :--- | :--- | :--- |
| **Announcement** | Feedback | Dismissible alert banner used in navigation footers and app headers. | `npx boardui@latest add announcement` |
| **Avatar** | Data Display | Image, initials, and fallback avatar with status indicator rings. | `npx boardui@latest add avatar` |
| **Badge** | Data Display | Status counter pills, dot chips, and shortcut hint labels. | `npx boardui@latest add badge` |
| **Breadcrumb** | Navigation | Accessible path trail with custom chevron separators. | `npx boardui@latest add breadcrumb` |
| **Button** | Inputs | Primary, secondary, ghost, and danger buttons in sm/md/lg with icon slots. | `npx boardui@latest add button` |
| **Button Group** | Inputs | Fused button group with hairline dividers and toggle selection. | `npx boardui@latest add button-group` |
| **Carousel** | Layout | CSS scroll-snap carousel with touch gestures, arrows, and dots. | `npx boardui@latest add carousel` |
| **Checkbox** | Inputs | Accessible checkbox with animated checkmark and indeterminate state. | `npx boardui@latest add checkbox` |
| **Checkbox Card** | Inputs | Selectable card wrapper controlled by an integrated checkbox. | `npx boardui@latest add checkbox-card` |
| **Chip** | Data Display | Compact filter chip with dismissal button and active state. | `npx boardui@latest add chip` |
| **Combobox** | Inputs | Autocomplete search input with filtered popover dropdown list. | `npx boardui@latest add combobox` |
| **Date Picker** | Inputs | Accessible calendar date selector with locale-aware formatters. | `npx boardui@latest add date-picker` |
| **Date Range Picker** | Inputs | Two-date interval selector with preset shortcuts and calendar view. | `npx boardui@latest add date-range-picker` |
| **Dialog / Modal** | Overlays | Accessible modal dialog with focus trap, backdrop blur, and escape key handling. | `npx boardui@latest add dialog` |
| **Dropdown Menu** | Overlays | Action menu with submenus, keyboard navigation, and checkable items. | `npx boardui@latest add dropdown-menu` |
| **Dropdown Select** | Inputs | Form select menu with custom trigger, item search, and icon support. | `npx boardui@latest add dropdown-select` |
| **Empty State** | Layout | Centered empty illustration state with call-to-action button. | `npx boardui@latest add empty-state` |
| **File Upload** | Inputs | Drag-and-drop file upload target with file list and upload progress bar. | `npx boardui@latest add file-upload` |
| **Filter** | Navigation | Multi-criteria filter bar with active tag pills and clear all button. | `npx boardui@latest add filter` |
| **Input** | Inputs | Single-line text input with label, leading/trailing icons, error text, and clear button. | `npx boardui@latest add input` |
| **Kbd** | Data Display | Visual keyboard shortcut indicator tag (e.g. Cmd+K). | `npx boardui@latest add kbd` |
| **Number Input** | Inputs | Numeric stepper input with increment/decrement steppers and range validation. | `npx boardui@latest add number-input` |
| **Pagination** | Navigation | Page navigation strip with page numbers, ellipsis, and jump-to controls. | `npx boardui@latest add pagination` |
| **Password Input** | Inputs | Secure input with visibility toggle eye icon and strength meter. | `npx boardui@latest add password-input` |
| **Popover** | Overlays | Floating anchored card with smart edge detection and outside dismiss. | `npx boardui@latest add popover` |
| **Radio Group** | Inputs | Accessible single-select radio button set. | `npx boardui@latest add radio-group` |
| **Radio Card** | Inputs | High-emphasis selectable cards driven by radio selections. | `npx boardui@latest add radio-card` |
| **Search Input** | Inputs | Search bar with search icon, clear button, and shortcut trigger badge. | `npx boardui@latest add search-input` |
| **Segmented Control** | Inputs | Pill-style segmented switcher with sliding highlight pill animation. | `npx boardui@latest add segmented-control` |
| **Skeleton** | Feedback | Shimmer loading skeleton placeholders for text, cards, and avatars. | `npx boardui@latest add skeleton` |
| **Slider** | Inputs | Continuous range slider with tooltip thumb and tick marks. | `npx boardui@latest add slider` |
| **Social Button** | Inputs | Pre-styled authentication buttons for 24 OAuth providers. | `npx boardui@latest add social-button` |
| **Status Dot** | Data Display | Semantic status dot indicator for table rows and badges. | `npx boardui@latest add status-dot` |
| **Switch** | Inputs | Smooth toggle switch with skeuomorphic thumb styling. | `npx boardui@latest add switch` |
| **Switch Card** | Inputs | Bordered settings item row with title, description, and switch. | `npx boardui@latest add switch-card` |
| **Table** | Data Display | Semantic table primitives (header, row, cell, footer) for custom layouts. | `npx boardui@latest add table` |
| **Tabs** | Navigation | Underline and pill variants for section navigation. | `npx boardui@latest add tabs` |
| **Textarea** | Inputs | Auto-growing multiline input with character counter. | `npx boardui@latest add textarea` |
| **Tooltip** | Overlays | Informational tooltip with arrow pointer and delayed reveal. | `npx boardui@latest add tooltip` |
| **Tree View** | Navigation | Hierarchical folder tree with expand/collapse, active node styling, and guides. | `npx boardui@latest add tree-view` |

## 3. Foundations (14 Foundations)

Token registries, global stylesheets, helper hooks, utilities, and agent rules.

| Foundation | Description | CLI Install Command |
| :--- | :--- | :--- |
| **Agent rules** | Always-on design rules for AI agents (tokens, type, conventions) installed in `.cursor/rules/boardui.mdc` or `AGENTS.md`. | `npx boardui@latest add rules` |
| **Agent runtime** | Server-side streaming endpoint handling Anthropic, OpenAI, Gemini, OpenRouter, Groq, xAI, or custom OpenAI-compatible backends. | `npx boardui@latest add agent-runtime` |
| **Chevron icons** | Stroke-accurate SVG chevron glyphs matching Figma designs. | `npx boardui@latest add chevrons` |
| **cx utility** | Tailwind-merge utility specifically configured for BoardUI composite type classes. | `npx boardui@latest add cx` |
| **Direction Provider** | React context provider delivering layout direction, locale, and RTL coordination for React Aria interactions. | `npx boardui@latest add direction` |
| **Directional icons** | Dynamic icon wrapper that mirrors directional arrows in RTL while preserving symmetric icons. | `npx boardui@latest add directional-icon` |
| **Directional scrolling** | Scroll offset math utilities ensuring carousels and tab lists align correctly across RTL and LTR. | `npx boardui@latest add scroll-direction` |
| **Global styles** | Main stylesheet importing theme, typography, animations, and dark-mode styles. | `npx boardui@latest add globals` |
| **Logo** | Placeholder brand mark designed to be easily replaced by application brand assets. | `npx boardui@latest add logo` |
| **Template copy** | Copy translation context provider allowing string localization without altering layout structure. | `npx boardui@latest add template-copy` |
| **Theme tokens** | 400+ semantic tokens covering light/dark surfaces, borders, text, charts, accents, and shadows. | `npx boardui@latest add theme` |
| **Typography tokens** | Composite font utilities combining size, weight, leading, and tracking into single Tailwind classes. | `npx boardui@latest add typography` |
| **useCountUp** | React hook providing smooth rolling number transitions for stat cards and chart headers. | `npx boardui@latest add use-count-up` |
| **useDismissOnOutsidePress**| React hook closing floating popovers and menus without swallowing the outside click event. | `npx boardui@latest add use-dismiss-on-outside-press` |

