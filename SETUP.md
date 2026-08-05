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

Both workflows also run on a schedule after the first successful run.

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
| 3D contribution graph | yoshi389111/github-profile-3d-contrib | Action (daily) |
| Contribution snake | Platane/snk | Action (every 12h) |
