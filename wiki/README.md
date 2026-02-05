# Wiki Content for Theme My Fox

This directory contains comprehensive wiki documentation for the Theme My Fox project.

## 📚 Wiki Pages

1. **[Home.md](Home.md)** - Wiki homepage with overview and quick links
2. **[Installation.md](Installation.md)** - Detailed installation guide for all platforms
3. **[API-Reference.md](API-Reference.md)** - Complete function documentation
4. **[Usage-Examples.md](Usage-Examples.md)** - Practical code examples and recipes
5. **[Troubleshooting.md](Troubleshooting.md)** - Common issues and solutions
6. **[FAQ.md](FAQ.md)** - Frequently asked questions
7. **[Contributing.md](Contributing.md)** - Contribution guidelines

## 🚀 How to Upload to GitHub Wiki

GitHub wikis are separate git repositories. To upload this content:

### Method 1: Manual Upload (Easiest)

1. Go to your repository: https://github.com/DeepFriedDuck/theme-my-fox
2. Click on the **"Wiki"** tab
3. Click **"Create the first page"** (if wiki doesn't exist)
4. For each markdown file:
   - Click **"New Page"**
   - Copy the filename (without .md) as the page title
   - Paste the content from the file
   - Click **"Save Page"**

### Method 2: Clone and Push (Recommended)

```bash
# Clone the wiki repository
git clone https://github.com/DeepFriedDuck/theme-my-fox.wiki.git
cd theme-my-fox.wiki

# Copy all wiki files
cp /path/to/theme-my-fox/wiki/*.md .

# Commit and push
git add .
git commit -m "Add comprehensive wiki documentation"
git push origin master
```

### Method 3: Automated Script

```bash
# From the theme-my-fox directory
cd wiki

# Clone wiki repo in a separate directory
git clone https://github.com/DeepFriedDuck/theme-my-fox.wiki.git temp-wiki
cd temp-wiki

# Copy all markdown files
cp ../*.md .

# Commit and push
git add *.md
git commit -m "Add comprehensive wiki documentation"
git push origin master

# Clean up
cd ..
rm -rf temp-wiki
```

## 📝 Page Structure

The wiki is organized as follows:

```
Home (landing page)
├── Installation
├── API Reference
├── Usage Examples
├── Troubleshooting
├── FAQ
└── Contributing
```

Each page has:
- Clear table of contents
- Code examples with syntax highlighting
- Cross-references to related pages
- Practical, real-world examples

## ✏️ Editing the Wiki

### After Initial Upload

Once uploaded to GitHub Wiki, you can edit pages directly on GitHub:
1. Navigate to the wiki
2. Click the **"Edit"** button on any page
3. Make your changes
4. Click **"Save Page"**

### Keeping Local Copy in Sync

If you make changes on GitHub Wiki and want to update this local copy:

```bash
# Clone the wiki repo
git clone https://github.com/DeepFriedDuck/theme-my-fox.wiki.git

# Copy updated files back to this directory
cp theme-my-fox.wiki/*.md /path/to/theme-my-fox/wiki/
```

## 🎨 Markdown Features Used

The wiki uses standard GitHub Flavored Markdown:
- Code blocks with syntax highlighting
- Tables
- Lists (ordered and unordered)
- Headers and sub-headers
- Links (internal wiki links and external)
- Inline code
- Blockquotes
- Emoji 🦊

## 📋 Content Overview

### Home.md
- Project overview
- Quick links to all pages
- Key features
- How it works
- Use cases

### Installation.md
- Prerequisites
- All installation methods (pip, PDM, Poetry, from source)
- Platform-specific notes
- Verification steps
- Troubleshooting installation issues

### API-Reference.md
- Complete function documentation
- Parameters, return values, exceptions
- Code examples for each function
- Type hints
- Best practices

### Usage-Examples.md
- Basic examples (listing profiles, themes)
- Theme scheduler (automatic switching)
- Multi-profile management
- Backup and restore
- System theme integration
- Error handling

### Troubleshooting.md
- Installation issues
- Profile issues
- Theme switching issues
- Permission issues
- Platform-specific issues
- Debugging tips

### FAQ.md
- General questions
- Installation questions
- Compatibility questions
- Usage questions
- Technical questions
- Best practices

### Contributing.md
- Ways to contribute
- Development setup
- Workflow guidelines
- Code style
- Testing guidelines
- PR process

## 🔄 Updating the Wiki

When you make changes to the code:

1. **Update relevant wiki pages** in this directory
2. **Test code examples** to ensure they work
3. **Upload changes to GitHub Wiki** using one of the methods above

## 📞 Questions?

If you have questions about the wiki content or structure:
- Open an issue on GitHub
- Email: deepfriedduck.opensourceapis@gmail.com

---

**Note:** This README.md file is for documentation purposes and should NOT be uploaded to the GitHub Wiki. Only upload the other markdown files (Home.md, Installation.md, etc.).
