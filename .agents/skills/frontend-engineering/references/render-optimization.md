# Frontend Render Optimization & Performance

## Core Principles
1. **Minimize Render Cascades**: Isolate fast-changing state (e.g. form inputs, timers) into leaf components.
2. **Selective Memoization**: Use `useMemo` and `useCallback` only when computation cost exceeds memoization overhead or when passing callbacks to memoized children.
3. **Core Web Vitals Thresholds**:
   - Largest Contentful Paint (LCP): < 2.5s
   - Interaction to Next Paint (INP): < 200ms
   - Cumulative Layout Shift (CLS): < 0.1
4. **Image & Asset Strategy**: Use modern formats (WebP/AVIF), specify explicit aspect ratios to eliminate layout shifts, and lazy-load below-the-fold assets.
