#!/bin/bash
# Script to create GitHub repository and push the module

# Configuration
GITHUB_USERNAME="Ka10U"
REPO_NAME="odoo-ambassador-coupons"
REPO_DESCRIPTION="Odoo module for tracking discount coupon usage by brand ambassadors"

echo "Creating GitHub repository: $GITHUB_USERNAME/$REPO_NAME"

# Check if gh is installed
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI..."
    gh repo create "$REPO_NAME" --public --description "$REPO_DESCRIPTION" --source=. --push
else
    echo "GitHub CLI not found. Please create the repository manually:"
    echo ""
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Description: $REPO_DESCRIPTION"
    echo "4. Set to Public"
    echo "5. DO NOT initialize with README, .gitignore, or license"
    echo "6. Click 'Create repository'"
    echo ""
    echo "Then run these commands:"
    echo ""
    echo "  git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
fi
