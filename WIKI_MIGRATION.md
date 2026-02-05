# Wiki Migration Guide

## Overview

The wiki documentation has been moved from the repository's `wiki/` folder to GitHub's Wiki feature. This allows the wiki to be managed separately and prevents it from being cloned with the repository.

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

## Wiki Pages Available

The following wiki pages are available:

- **Home**: Main wiki landing page
- **Installation Guide**: How to install the library
- **Quick Start Tutorial**: Getting started guide
- **Basic Concepts**: Core concepts and terminology
- **Theme Management API**: API reference for theme management
- **Profile Management API**: API reference for profile management
- **Compression API**: API reference for file compression
- **Common Use Cases**: Examples and patterns
- **Troubleshooting Guide**: Solutions to common issues
- **Contributing Guide**: How to contribute to the project

## Migration Details

The wiki content was previously stored in the `wiki/` folder in the main repository. This has been removed to:
1. Reduce repository size
2. Prevent wiki documentation from being cloned with every repository clone
3. Allow wiki to be edited independently without affecting the main codebase
4. Follow GitHub's recommended practice of using the Wiki feature for documentation

## For Repository Maintainers

To set up the wiki content on GitHub:

1. Enable the Wiki feature in repository settings (Settings → Features → Wikis)

2. Clone the wiki repository:
   ```bash
   git clone https://github.com/DeepFriedDuck/theme-my-fox.wiki.git
   ```

3. Copy the wiki files from the old `wiki/` folder to the wiki repository

4. Commit and push:
   ```bash
   cd theme-my-fox.wiki
   git add .
   git commit -m "Initialize wiki with documentation"
   git push
   ```

Note: GitHub Wiki filenames use hyphens (e.g., `Home.md`, `Installation-Guide.md`) and will automatically be displayed with proper formatting in the Wiki interface.
