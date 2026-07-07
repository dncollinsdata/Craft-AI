# Galaxy Craft Expo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a first native Expo version of Galaxy Craft AI from the provided HTML mockups.

**Architecture:** Use Expo Router for app navigation, shared themed components for the cosmic/glass visual language, and static craft mission data for the first usable pass. Keep AI/photo generation as clear placeholders so the app can run now and be wired to backend or on-device flows later.

**Tech Stack:** Expo, React Native, Expo Router, TypeScript, `expo-linear-gradient`, `expo-blur`, `expo-image`, `expo-haptics`, `@expo/vector-icons`, Vitest for data contract tests.

---

### Task 1: Project Scaffold

**Files:**
- Create: `package.json`
- Create: `app.json`
- Create: `tsconfig.json`
- Create: `babel.config.js`
- Create: `.gitignore`
- Create: `app/_layout.tsx`

- [ ] **Step 1: Create Expo package manifest**

Add scripts for `expo start`, `expo start --ios`, `expo start --android`, `expo start --web`, `tsc --noEmit`, and `vitest run`.

- [ ] **Step 2: Install dependencies**

Run: `npm install`

Expected: `node_modules` and `package-lock.json` are created.

- [ ] **Step 3: Add Expo Router root layout**

Create a stack layout with the header hidden, using dark app backgrounds.

### Task 2: Craft Data Contract

**Files:**
- Create: `src/data/crafts.test.ts`
- Create: `src/data/crafts.ts`

- [ ] **Step 1: Write failing tests**

Test that the featured mission has a title, materials, steps, stats, safety tip, upgrade tip, and saved missions list.

- [ ] **Step 2: Run test to verify failure**

Run: `npm test`

Expected: FAIL because `src/data/crafts.ts` does not exist yet.

- [ ] **Step 3: Implement craft data**

Add static data for the welcome, mission, and saved screens based on the pasted HTML.

- [ ] **Step 4: Run tests to verify pass**

Run: `npm test`

Expected: PASS.

### Task 3: Shared UI System

**Files:**
- Create: `src/theme.ts`
- Create: `src/components/CosmicBackground.tsx`
- Create: `src/components/GlassPanel.tsx`
- Create: `src/components/GalaxyHeader.tsx`
- Create: `src/components/BottomTabs.tsx`
- Create: `src/components/CosmicButton.tsx`

- [ ] **Step 1: Add theme tokens**

Define colors, spacing, radii, and typography constants from the mockup.

- [ ] **Step 2: Add reusable UI components**

Implement background, glass panels, header, bottom tab bar, and gradient buttons with Expo packages.

- [ ] **Step 3: Run typecheck**

Run: `npm run typecheck`

Expected: PASS.

### Task 4: Screens

**Files:**
- Create: `app/index.tsx`
- Create: `app/mission.tsx`
- Create: `app/saved.tsx`

- [ ] **Step 1: Implement welcome screen**

Create the Galaxy Craft AI hero, process steps, featured idea row, and camera floating action button.

- [ ] **Step 2: Implement mission screen**

Create the Nebula Nightlight result screen with stats, materials, steps, safety, upgrade tip, and actions.

- [ ] **Step 3: Implement saved missions screen**

Create saved mission cards and empty-state-ready layout.

- [ ] **Step 4: Run verification**

Run: `npm test` and `npm run typecheck`.

Expected: both pass.
