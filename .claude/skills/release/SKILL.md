---
name: release
description: Run the full release — commit, version bump, tag, push, GitHub Releases, sparq sync. No confirmations needed.
argument-hint: "[version] [short description]"
---

# Release Checklist

You are a release manager. Execute the full release process end-to-end without pausing for confirmations. Only stop if a step fails — fix it or report the error.

## Parse Arguments

- If the user provided a version (e.g., `/release v2.7.0`), use it. Otherwise, **offer version options** — look up the current version from MEMORY.md or the latest git tag, then present patch/minor/major bumps with a brief rationale for each (e.g., "v2.9.3 (patch) — small fix, no new features" / "v2.10.0 (minor) — new feature or meaningful improvement"). Recommend one.
- If the user provided a short description after the version (e.g., `/release v2.7.0 add release skill`), use it. Otherwise, suggest a description based on the pending changes and ask the user to confirm or edit it.
- Validate the version matches `vX.Y.Z` format.
- These are the ONLY questions to ask. Once you have the version and description, execute everything below without stopping.

## Step 1: Commit Pending Changes

- Run `git status` to check for uncommitted or untracked changes.
- If the tree is dirty:
  - Stage all modified and untracked files relevant to the project (use `git add` with specific files, not `git add -A`).
  - Review what's staged with `git diff --staged` and create an appropriate commit using conventional commit format (feat/fix/refactor/docs/chore).
  - Include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>` in the commit message.
- If the tree is already clean, skip to Step 2.
- Repeat until the working tree is clean — there may be multiple logical commits needed.

## Step 2: Update README.md Badge

- Read line 1 of `README.md`.
- Edit the badge to replace the old version with the new version (both the label text and the alt text).

## Step 3: Update CHANGELOG.md

- Read the top of `CHANGELOG.md` to see the format of existing entries.
- Prepend a new `## vX.Y.Z (YYYY-MM-DD)` section at the top with bullet points describing what changed.
- Use the short description provided, plus summarize any commits made in Step 1.

## Step 4: Commit the Version Bump

- Stage `README.md` and `CHANGELOG.md`.
- Commit: `docs: bump version to vX.Y.Z`
- Include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`.

## Step 5: Tag & Push

- Create the tag: `git tag vX.Y.Z`
- Push commits and tags: `git push origin master && git push origin --tags`

## Step 6: Create GitHub Release (origin)

- Run: `gh release create vX.Y.Z --title "vX.Y.Z — Short Description" --notes "## What's New\n- ..."`
- Use the CHANGELOG entry content for the release notes.

## Step 7: Sync Sparq Remote

- Run: `bash "$CLAUDE_PROJECT_DIR/.claude/scripts/sync-sparq.sh"`
- If the sparq remote doesn't exist, skip this step and Step 8.

## Step 8: Create GitHub Release (sparq)

- Run: `gh release create vX.Y.Z --repo zainnab-sparq/cc-self-train --title "vX.Y.Z — Short Description" --notes "..."` (same notes as Step 6)
- If the sparq remote doesn't exist, skip this step.

## Step 9: Update MEMORY.md

- Edit `~/.claude/projects/C--Users-Zain--Dropbox-Personal-Data-Science-Projects-cc-self-train/memory/MEMORY.md` to update "Current version: vX.Y.Z" to the new version.

## Step 10: Summary

Print a summary table showing each step and its result (commit hashes, release URLs, etc.).

## Important

- **No confirmations.** Execute all steps automatically. Only stop if a step fails.
- **Commit before releasing.** Never leave uncommitted changes behind — they should be part of the release.
- If any step fails, stop and help the user fix it before continuing.
