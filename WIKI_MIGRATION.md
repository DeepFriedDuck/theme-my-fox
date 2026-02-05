# Wiki Migration Guide

## Overview

The wiki documentation has been moved from the repository's `wiki/` folder to GitHub's Wiki feature. This allows the wiki to be managed separately and prevents it from being cloned with the repository.

## ✅ Migration Status

**The wiki content has been prepared and is ready to be pushed to GitHub!**

All 10 wiki pages have been:
- ✅ Extracted from the main repository
- ✅ Committed to the wiki repository at `/tmp/theme-my-fox.wiki`
- ⏳ Ready to be pushed to GitHub (requires authentication)

To complete the migration, run:
```bash
./push-wiki.sh
```

Or manually push the wiki content:
```bash
cd /tmp/theme-my-fox.wiki
git push origin master
```

## How to Access the Wiki

You can access the wiki through:
- GitHub UI: Click the "Wiki" tab at the top of the repository page
- Direct URL: https://github.com/DeepFriedDuck/theme-my-fox/wiki

## How to Contribute to the Wiki

The GitHub Wiki is a separate git repository. To contribute:

### Method 1: Edit Directly on GitHub (Recommended for Small Changes)
1. Navigate to https://github.com/DeepFriedDuck/theme-my-fox/wiki
2. Click on the page you want to edit
3. Click the "Edit" button
4. Make your changes
5. Click "Save Page"

### Method 2: Clone the Wiki Repository (For Larger Changes)
1. Clone the wiki repository:
   ```bash
   git clone https://github.com/DeepFriedDuck/theme-my-fox.wiki.git
   ```

2. Make your changes to the markdown files

3. Commit and push:
   ```bash
   git add .
   git commit -m "Update documentation"
   git push
   ```

## Wiki Pages Migrated

The following 10 wiki pages have been prepared and are ready to push:

1. **Home.md** (2.0 KB) - Main wiki landing page
2. **Installation-Guide.md** (4.0 KB) - How to install the library
3. **Quick-Start-Tutorial.md** (5.6 KB) - Getting started guide
4. **Basic-Concepts.md** (6.1 KB) - Core concepts and terminology
5. **Profile-Management-API.md** (7.1 KB) - API reference for profile management
6. **Contributing-Guide.md** (9.1 KB) - How to contribute to the project
7. **Troubleshooting-Guide.md** (11 KB) - Solutions to common issues
8. **Compression-API.md** (12 KB) - API reference for file compression
9. **Theme-Management-API.md** (12 KB) - API reference for theme management
10. **Common-Use-Cases.md** (16 KB) - Examples and patterns

**Total: 3,398 lines of documentation ready to be published!**

## Migration Details

The wiki content was previously stored in the `wiki/` folder in the main repository. This has been removed and prepared for migration to:
1. Reduce repository size
2. Prevent wiki documentation from being cloned with every repository clone
3. Allow wiki to be edited independently without affecting the main codebase
4. Follow GitHub's recommended practice of using the Wiki feature for documentation

### What Has Been Done

✅ **Completed:**
- Removed `wiki/` folder from the main repository
- Cloned the GitHub Wiki repository to `/tmp/theme-my-fox.wiki`
- Copied all 10 wiki markdown files to the wiki repository
- Created a commit with all the documentation (3,398 lines)
- Prepared push script (`push-wiki.sh`) for easy deployment

⏳ **Pending:**
- Push the prepared wiki content to GitHub (requires authentication)
  - Run `./push-wiki.sh` or
  - Manually: `cd /tmp/theme-my-fox.wiki && git push origin master`

## For Repository Maintainers

### Completing the Migration

The wiki content is already prepared and committed at `/tmp/theme-my-fox.wiki`. To complete the migration:

**Option 1: Using the provided script**
```bash
./push-wiki.sh
```

**Option 2: Manual push**
```bash
cd /tmp/theme-my-fox.wiki
git push origin master
```

If you need to authenticate with GitHub:
```bash
# Using GitHub CLI
gh auth login

# Or configure git credentials
git config --global credential.helper store
```

After pushing, the wiki will be immediately available at:
https://github.com/DeepFriedDuck/theme-my-fox/wiki

### Verifying the Migration

Once pushed, verify that all pages appear correctly:
- Navigate to the Wiki tab on GitHub
- Check that all 10 pages are listed in the sidebar
- Verify the content renders properly
- Test the navigation between pages
