#!/usr/bin/env bash
set -euo pipefail

# Course 1906 revision workflow for a temporary branch + stash cycle.
# This keeps the repo clean while allowing the validation scripts to mutate the
# starter templates and exercise files in place.
#
# Usage:
#   bash scripts/automated_testing/course_revision_cycle.sh
# Optional environment variables:
#   BRANCH_NAME=${BRANCH_NAME:-course-revision-$(date +%Y%m%d)}
#   SWEEP_CMD=${SWEEP_CMD:-python scripts/automated_testing/refresh_and_sweep.py}

BRANCH_NAME="${BRANCH_NAME:-course-revision-$(date +%Y%m%d)}"
SWEEP_CMD="${SWEEP_CMD:-python scripts/automated_testing/refresh_and_sweep.py}"
PATCH_FILE="${PATCH_FILE:-validation-generated.patch}"

printf '==> Starting revision workflow on branch: %s\n' "$BRANCH_NAME"

git checkout master
# Pull latest master only if desired; keep this comment as a reminder.
# git pull --ff-only

git checkout -b "$BRANCH_NAME"

printf '\n==> Running validation sweep...\n'
if ! bash -lc "$SWEEP_CMD"; then
    printf '\nValidation failed. Saving generated changes to %s before cleanup...\n' "$PATCH_FILE"
    git diff > "$PATCH_FILE"
    printf '\n==> Reverting generated validation edits...\n'
    git restore --worktree --staged .
    printf '\nReview the diff and fix only the intentional course changes.\n'
    printf 'When ready, stage the real fixes with: git add -p\n'
    exit 1
fi

printf '\n==> Validation passed. Saving generated changes to %s...\n' "$PATCH_FILE"
git diff > "$PATCH_FILE"

printf '\n==> Reverting generated validation edits...\n'
git restore --worktree --staged .

printf '\nReview the diff and keep only the intentional course fixes.\n'
printf 'Then commit them and merge back to master.\n'
printf '\nUseful commands:\n'
printf '  git diff\n'
printf '  git add -p\n'
printf '  git commit -m "Revise course materials"\n'
printf '  git checkout master\n'
printf '  git merge --no-ff %s\n' "$BRANCH_NAME"
printf '  git branch -d %s\n' "$BRANCH_NAME"

exit 0
