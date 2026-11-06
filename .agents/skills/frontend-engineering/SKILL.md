---
name: frontend-engineering
description: "Build and maintain production-grade web applications. Covers React/Next.js component architecture, state management, render performance optimization, Three.js WebGL rendering, and Playwright UI browser verification. Use when building UI features, optimizing React components, implementing 3D WebGL scenes, or running automated post-deploy browser smoke tests."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [frontend, react, nextjs, performance, webgl, browser-qa]
  sources_count: 3
---

# Frontend Engineering

Consolidated engineering capability for building, optimizing, and verifying production web applications across React, Next.js, WebGL, and browser automation.

## When to Activate
- Implementing React, Next.js, or TypeScript frontend components.
- Designing component state architecture, client-side caching, and render lifecycles.
- Profiling and eliminating frontend performance bottlenecks (re-renders, bundle size, Core Web Vitals).
- Implementing 3D WebGL scenes, shaders, kinetic typography, or interactive backgrounds.
- Running post-deploy automated browser verification (smoke tests, visual regression, form verification).

## When NOT to Activate
- Pure visual interface design and artistic exploration (use `interface-design`).
- Constructing design tokens, color harmonies, or logo marks (use `design-systems`).
- Backend API route handler development or database schema design (use `backend-engineering`).

## Core Execution Workflow

1. **Architecture & State Design:**
   - Organize components by domain/feature, maintaining small, cohesive files (<400 lines).
   - Enforce immutability: create new state objects, never mutate existing ones in place.
   - Separate server components (data fetching) from client components (interactivity) in Next.js App Router.
   - Consult [references/component-architecture.md](references/component-architecture.md).

2. **Render & Performance Optimization:**
   - Optimize bundle splitting, memoization, and lazy loading for high Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms).
   - Prevent unnecessary re-renders through selective context splitting and stable callbacks.
   - Consult [references/render-optimization.md](references/render-optimization.md).

3. **Interactive 3D & WebGL Integration:**
   - When 3D graphics or WebGL components are required, follow Three.js lifecycle management (scene setup, geometry disposal, 60fps render loop).
   - Consult [references/threejs-webgl-patterns.md](references/threejs-webgl-patterns.md).

4. **Automated Browser UI Verification:**
   - Run automated smoke checks using Playwright/browser automation.
   - Verify console errors, accessibility trees (axe-core), form flows, and responsive layouts across mobile, tablet, and desktop viewports.
   - Consult [references/browser-verification-qa.md](references/browser-verification-qa.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [component-architecture.md](references/component-architecture.md) | React/Next.js patterns, hooks, state machines, props design | `affaan-m/ECC` (`frontend-patterns`) |
| [render-optimization.md](references/render-optimization.md) | Virtualization, memoization, image optimization, Core Web Vitals | `affaan-m/ECC` (`frontend-patterns`) |
| [threejs-webgl-patterns.md](references/threejs-webgl-patterns.md) | 104 Three.js components, shaders, kinetic typography, WebGL lifecycle | `hamzzaqureshi/gravidex` (`threeui`) |
| [browser-verification-qa.md](references/browser-verification-qa.md) | Playwright UI smoke tests, visual regression, console error audits | `affaan-m/ECC` (`browser-qa`) |
