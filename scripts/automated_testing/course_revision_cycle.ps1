param(
    [string]$BranchName = ("course-revision-" + (Get-Date).ToString("yyyyMMdd")),
    [string]$SweepCommand = "python scripts/automated_testing/refresh_and_sweep.py",
    [string]$PatchFile = "validation-generated.patch"
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $RepoRoot

Write-Host "==> Starting revision workflow on branch: $BranchName"

git checkout master
# Pull latest master only if desired; keep this comment as a reminder.
# git pull --ff-only

try {
    git checkout -b $BranchName
}
catch {
    Write-Host "Branch already exists; switching to it instead."
    git checkout $BranchName
}

Write-Host "`n==> Running validation sweep..."
try {
    Invoke-Expression $SweepCommand
}
catch {
    Write-Host "`nValidation command failed to start. Saving generated changes to $PatchFile before cleanup..."
    git diff | Set-Content -Path $PatchFile
    Write-Host "`n==> Reverting generated validation edits..."
    git restore --worktree --staged .
    Write-Host "`nReview the diff and fix only the intentional course changes."
    Write-Host "When ready, stage the real fixes with: git add -p"
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nValidation failed. Saving generated changes to $PatchFile before cleanup..."
    git diff | Set-Content -Path $PatchFile
    Write-Host "`n==> Reverting generated validation edits..."
    git restore --worktree --staged .
    Write-Host "`nReview the diff and fix only the intentional course changes."
    Write-Host "When ready, stage the real fixes with: git add -p"
    exit 1
}

Write-Host "`n==> Validation passed. Saving generated changes to $PatchFile..."
git diff | Set-Content -Path $PatchFile

Write-Host "`n==> Reverting generated validation edits..."
git restore --worktree --staged .

Write-Host "`nReview the diff and keep only the intentional course fixes."
Write-Host "Then commit them and merge back to master."
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  git diff"
Write-Host "  git add -p"
Write-Host "  git commit -m 'Revise course materials'"
Write-Host "  git checkout master"
Write-Host "  git merge --no-ff $BranchName"
Write-Host "  git branch -d $BranchName"

exit 0
