# /commit - Automated Git Workflow & PR Creation

Streamlines committing changes, creating PRs, and updating GitHub issues in one command.

## Steps

### 1. Sync with Main
```bash
git pull origin main
```

### 2. Stage & Commit Changes
```bash
# Add all files except system/test files
git add -A
git reset -- '*.pyc' '__pycache__' '.pytest_cache' 'node_modules' '*.log' '.env'

# Commit with descriptive message
git commit -m "feat: [auto-generated commit message based on changes]"
```

### 3. Push to Current Branch
```bash
git push origin HEAD
```

### 4. Create Pull Request
```bash
gh pr create --title "[Branch name] implementation" \
             --body "## Changes\n- [Summary of changes]\n\n## Related Issue\nCloses #[issue-number]" \
             --base main
```

### 5. Update GitHub Issue
```bash
gh issue comment [issue-number] --body "PR created: [PR URL]"
```

### 6. Output PR URL
Display the created PR URL for review.

## Usage
```
/commit
```

## Options
- Automatically detects current branch
- Infers issue number from branch name (e.g., `issue-7-integration` → Issue #7)
- Generates commit message from staged changes

## Output
- Commit hash
- PR number and URL
- Issue comment confirmation
- Direct link to review PR