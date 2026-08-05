# Setup Guide

This repo powers the GitHub profile README at [github.com/vrelay](https://github.com/vrelay).

## Enable GitHub Actions

In **Settings → Actions → General**:
- Allow all actions and reusable workflows
- Allow GitHub Actions to create and approve pull requests (if prompted for write access)

## Generate the 3D contribution graph

**Actions → generate 3D contribution graph → Run workflow**

Writes SVGs under `profile-3d-contrib/` (including `profile-night-rainbow.svg`) and commits them to `main`.

## Generate the contribution snake

**Actions → generate contribution snake → Run workflow**

Writes colored SVGs under `dist/` and commits them to `main`.  
Each loop holds the full contribution grid for ~18s before the snake starts (GitHub READMEs cannot start animations on scroll).

Both workflows also run automatically **twice a week** (Monday & Thursday, 18:00 UTC).

## Refreshing your profile

Not everything updates the same way.

### Live stats (no action needed)

These fetch fresh data from external APIs whenever someone loads your profile. They usually update within a few minutes of new GitHub activity, but providers may cache for ~15–30 minutes.

- Stats card, top languages, streak
- Trophies, activity graph
- Header, typing animation, skill icons

If numbers look stale, hard-refresh the page (`Ctrl+Shift+R` / `Cmd+Shift+R`).

### Generated assets (run a workflow)

Snake and 3D graph are **SVG files committed to this repo**. They do not update on page load.

| What | How to refresh | Auto schedule |
|------|----------------|---------------|
| Contribution snake | **Actions → generate contribution snake → Run workflow** | Mon & Thu, 18:00 UTC |
| 3D contribution graph | **Actions → generate 3D contribution graph → Run workflow** | Mon & Thu, 18:00 UTC |

After a workflow succeeds, wait ~30 seconds and hard-refresh your profile. The new SVGs are served from `dist/` and `profile-3d-contrib/` on `main`.

## Widgets used

| Widget | Provider | Updates |
|--------|----------|---------|
| Animated header & footer | capsule-render.vercel.app | Live |
| Typing SVG | readme-typing-svg.demolab.com | Live |
| Skill icons | skillicons.dev | Live |
| GitHub trophies | github-profile-trophy-psi.vercel.app | Live |
| Stats + top langs + pins | github-stats-extended.vercel.app | Live |
| Streak | github-readme-streak-stats-salesp07.vercel.app | Live |
| Activity graph | github-readme-activity-graph.vercel.app | Live |
| 3D contribution graph | yoshi389111/github-profile-3d-contrib | Action (2×/week) |
| Contribution snake | Platane/snk | Action (2×/week) |
