# Setup Guide

This repo powers the GitHub profile README at [github.com/vrelay](https://github.com/vrelay).

## Enable GitHub Actions

In **Settings → Actions → General**:
- Allow all actions and reusable workflows
- Allow GitHub Actions to create and approve pull requests (if prompted for write access)

## Refresh the profile

One workflow does everything: **Actions → update profile → Run workflow**.

| Job | Writes |
|-----|--------|
| **graphics** | `profile/*.svg`, `profile-3d-contrib/*.svg`, `dist/*snake*.svg` on `main` |
| **activity** | `contributions.svg` on the `output` branch |

It also runs automatically twice a week (Monday & Thursday, 18:00 UTC).

After it succeeds, wait ~30 seconds and hard-refresh the profile (`Ctrl+Shift+R` / `Cmd+Shift+R`).

Cards, trophies, graphs, and the snake are **SVG files in this repo**. They do not fetch live data when someone opens your profile.

## Why some numbers still differ

| Number | Source | What it counts |
|--------|--------|----------------|
| Total contributions | streak | GitHub contribution calendar (commits + PRs + issues + reviews) |
| Commits trophy | trophies | Commit-based trophy score |
| Total Commits on the stats card | stats | Commits GitHub can attribute to `vrelay` (author email). Often lower than the calendar. |
| Stars / forks | stats + 3D graph | Stars and forks on repos you own |
| Top languages | languages card | Language bytes across **your** repos, not forks. HTML/CSS are hidden because generated markup drowned out TypeScript / Python / Go. |

If Total Commits still looks far too low, the commit author email in git is probably not [linked to your GitHub account](https://github.com/settings/emails).

Private contributions need a PAT (`repo` + `read:user`) stored as a repo secret and passed into the workflow instead of `GITHUB_TOKEN`.
