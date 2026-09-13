#!/usr/bin/env bash
# Commit generated files onto the latest main and retry if another job pushed first.
# Usage: scripts/commit_generated.sh "commit message" path [path...]
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 COMMIT_MESSAGE PATH [PATH...]" >&2
  exit 2
fi

msg=$1
shift

git config user.name github-actions
git config user.email github-actions@github.com

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

for path in "$@"; do
  if [ ! -e "$path" ]; then
    echo "missing generated path: $path" >&2
    exit 1
  fi
  mkdir -p "$tmpdir/$(dirname "$path")"
  cp -a "$path" "$tmpdir/$path"
done

for attempt in 1 2 3 4 5; do
  git fetch origin main
  git reset --hard origin/main

  for path in "$@"; do
    rm -rf "$path"
    mkdir -p "$(dirname "$path")"
    cp -a "$tmpdir/$path" "$path"
  done

  git add -- "$@"
  if git diff --staged --quiet; then
    echo "No generated changes to commit"
    exit 0
  fi

  git commit -m "$msg"
  if git push origin HEAD:main; then
    exit 0
  fi

  echo "Push raced with another job (attempt ${attempt}); retrying..."
  sleep $((attempt * 3))
done

echo "Failed to push after retries" >&2
exit 1
