# /merge - Automated PR Merge & Cleanup

Merges PR, cleans up branches/worktrees, and updates GitHub issues in one command.

## Usage
```
/merge <PR_URL> <ISSUE_NUMBER>
```

## Arguments
- `PR_URL`: Full GitHub PR URL or PR number
- `ISSUE_NUMBER`: GitHub issue number to update

## Steps

### 1. Merge Pull Request
```bash
gh pr merge [PR] --merge --delete-branch
```

### 2. Update Local Repository
```bash
git fetch origin
git pull origin main
```

### 3. Clean Up Local Branch
```bash
# Extract branch name from PR
BRANCH=$(gh pr view [PR] --json headRefName -q .headRefName)
git branch -D $BRANCH
```

### 4. Clean Up Worktree
```bash
# Find and remove worktree for branch
git worktree list | grep $BRANCH
git worktree remove --force [worktree-path]
```

### 5. Update GitHub Issue
```bash
gh issue comment [ISSUE] --body "✅ PR #[PR] merged and cleaned up"
gh issue close [ISSUE] --comment "Implementation complete"
```

### 6. Print Summary
```
✅ Merged: PR #[PR]
✅ Deleted: Local and remote branch [BRANCH]
✅ Removed: Worktree at [PATH]
✅ Closed: Issue #[ISSUE]
```

## Example
```
/merge https://github.com/stewmckendry/ai_tutor/pull/12 7
/merge 12 7
```

## Output
- PR merge confirmation
- Branch cleanup status
- Worktree removal confirmation
- Issue update confirmation
- Final summary of all actions