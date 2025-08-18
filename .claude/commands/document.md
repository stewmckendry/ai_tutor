# /document - Comprehensive Documentation Update

Automatically review and update all project documentation to reflect current implementation state.

## Steps

### 1. Sync with Latest Code
```bash
git pull origin main
```

### 2. Review & Update /docs
- **Update existing docs** for accuracy with current implementation
- **Create new docs** ONLY for significant new architecture components
- Files to review:
  - `backend.md` - Backend API architecture
  - `web_interface.md` - Frontend implementation
  - `curriculum_content.md` - Content system
  - `component_inventory.md` - Component catalog

### 3. Update README.md
- Check implementation status sections
- Update completed features
- Verify repository structure
- Update development plan progress

### 4. Update CLAUDE.md
- Verify implementation status
- Update code structure if changed
- Check tech stack accuracy
- Update environment variables

### 5. Update Component Inventory
- Add new components created
- Update existing component paths/descriptions
- Document new API endpoints
- Update version history

### 6. Commit & Push
```bash
git add -A
git commit -m "docs: Update documentation to reflect current implementation"
git push origin main
```
Create PR if on feature branch.

## Usage
```
/document
```

## Output
- Summary of files updated
- List of new documentation created
- Components added to inventory
- Commit hash and PR link (if applicable)