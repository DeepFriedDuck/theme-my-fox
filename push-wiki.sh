#!/bin/bash
set -e  # Exit on any error

# Script to push the prepared wiki content to GitHub Wiki

echo "This script will push the wiki content that has been prepared in /tmp/theme-my-fox.wiki"
echo ""

if [ ! -d "/tmp/theme-my-fox.wiki" ]; then
    echo "Error: Wiki repository not found at /tmp/theme-my-fox.wiki"
    echo "The wiki content needs to be prepared first."
    exit 1
fi

cd /tmp/theme-my-fox.wiki || exit 1

echo "Current wiki repository status:"
git log --oneline -5 2>/dev/null || echo "No commits yet"
echo ""

echo "Files to be pushed:"
if git rev-parse origin/master >/dev/null 2>&1; then
    git diff --stat origin/master master 2>/dev/null || git status --short
else
    echo "New wiki - all files will be pushed"
    git status --short
fi
echo ""

read -p "Do you want to push these changes to GitHub Wiki? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing to GitHub Wiki..."
    git push origin master
    
    if [ $? -eq 0 ]; then
        echo "✓ Wiki content successfully pushed to GitHub!"
        echo "You can view it at: https://github.com/DeepFriedDuck/theme-my-fox/wiki"
    else
        echo "✗ Push failed. You may need to authenticate."
        echo "Try using 'gh auth login' or configure git credentials."
    fi
else
    echo "Push cancelled."
fi
