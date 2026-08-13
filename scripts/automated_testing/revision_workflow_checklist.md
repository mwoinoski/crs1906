# Course 1906 Revision Workflow Checklist

## Overview
This workflow keeps the repo clean by running validation on a temporary branch, capturing generated changes to a patch, and reverting those changes before reviewing and committing only intentional course fixes.

---

## Quick Start (Automated)

### Bash
```bash
bash scripts/automated_testing/course_revision_cycle.sh
```

### PowerShell
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\automated_testing\course_revision_cycle.ps1
```

---

## Manual Workflow Checklist

### Phase 1: Setup
- [ ] Ensure you are on `master` branch
  ```
  git status
  git branch
  ```
- [ ] Confirm working tree is clean (no uncommitted changes)
  ```
  git status
  ```
- [ ] Optional: Pull latest from remote (if desired)
  ```
  git pull --ff-only
  ```

### Phase 2: Create Revision Branch
- [ ] Create a new branch for this revision cycle
  ```
  git checkout -b course-revision-YYYYMMDD
  ```
  (Replace `YYYYMMDD` with today's date, e.g., `course-revision-20260813`)

### Phase 3: Run Validation Sweep
- [ ] Run the full course validation
  ```
  python scripts/automated_testing/refresh_and_sweep.py
  ```
- [ ] Note the exit code:
  - If validation **passes** (exit 0), continue to Phase 4
  - If validation **fails** (exit non-zero), note the errors and go to Phase 5

### Phase 4A: After Successful Validation
- [ ] View what was changed by the validation
  ```
  git diff
  ```
- [ ] Save the generated changes to a patch (for reference/review)
  ```
  git diff > validation-generated.patch
  ```
- [ ] Revert all validation-generated changes
  ```
  git restore --worktree --staged .
  ```
- [ ] Verify working tree is now clean
  ```
  git status
  ```
- [ ] Continue to Phase 6

### Phase 4B: After Validation Failure
- [ ] Review error messages and fix the root cause
- [ ] Save the generated changes to a patch (for debugging later if needed)
  ```
  git diff > validation-generated.patch
  ```
- [ ] Revert all validation-generated changes
  ```
  git restore --worktree --staged .
  ```
- [ ] Fix the underlying issue in your course materials
- [ ] Re-run the validation sweep from Phase 3

### Phase 5: Review and Commit Intentional Changes
- [ ] View any course material changes you made (not validation-generated)
  ```
  git status
  git diff
  ```
- [ ] Stage changes interactively (recommended for careful review)
  ```
  git add -p
  ```
  Choose `y` for each hunk that represents an intentional course fix.
  Choose `n` to skip any validation-generated or unintended changes.

- [ ] Commit your changes
  ```
  git commit -m "Revise course materials - [describe your changes]"
  ```

- [ ] If no intentional changes were made, skip the commit and go to Phase 6

### Phase 6: Merge Back to Master
- [ ] Ensure you are on your revision branch
  ```
  git branch
  ```
- [ ] Switch to master
  ```
  git checkout master
  ```
- [ ] Merge the revision branch (using `--no-ff` to preserve history)
  ```
  git merge --no-ff course-revision-YYYYMMDD
  ```
- [ ] Optionally delete the revision branch
  ```
  git branch -d course-revision-YYYYMMDD
  ```

### Phase 7: Cleanup
- [ ] Review the validation patch (if needed for debugging)
  ```
  type validation-generated.patch
  ```
  (or `cat validation-generated.patch` in bash/PowerShell)
- [ ] Delete the patch file (optional)
  ```
  rm validation-generated.patch
  ```
- [ ] Verify master is now ahead with your commits
  ```
  git log --oneline -5
  git status
  ```

---

## Key Points

- **Branch isolation**: All work happens on a temporary revision branch; master stays clean.
- **Validation separation**: Generated validation edits are captured in a patch and reverted before you review.
- **Selective commit**: You review and commit only the intentional course fixes using `git add -p`.
- **Local venvs preserved**: Because you use branches (not worktrees), your local virtual environments are not re-created.
- **Repeatable**: You can run this workflow multiple times during the year without affecting master.

---

## Troubleshooting

### I accidentally committed validation-generated changes
If you committed changes before reviewing them carefully:
- Amend the last commit and remove the unwanted changes
  ```
  git reset HEAD~1
  git add -p
  git commit -m "..."
  ```
- Or use `git revert <commit-hash>` to undo a past commit

### I deleted my revision branch but still have unmerged commits
- Switch to master and check the reflog
  ```
  git reflog
  git merge <branch-sha-from-reflog>
  ```

### Validation passed but I don't see any changes to review
This is normal if the validation only updated internal manifests or generated intermediate files. Check the patch file:
```
type validation-generated.patch
```

### I want to preserve the validation patch for later comparison
Before running Phase 7 cleanup:
```
copy validation-generated.patch validation-generated-archive-20260813.patch
```

---

## Environment Variables (for scripted versions)

When running the bash or PowerShell scripts, you can override defaults:

### Bash
```bash
BRANCH_NAME="my-custom-branch" \
SWEEP_CMD="python scripts/automated_testing/refresh_and_sweep.py" \
PATCH_FILE="my-patch.patch" \
bash scripts/automated_testing/course_revision_cycle.sh
```

### PowerShell
```powershell
.\scripts\automated_testing\course_revision_cycle.ps1 `
  -BranchName "my-custom-branch" `
  -SweepCommand "python scripts/automated_testing/refresh_and_sweep.py" `
  -PatchFile "my-patch.patch"
```
