#!/bin/bash

# 🚀 Website Scraper Deployment Script for Render
# This script helps you prepare and deploy your app to Render

echo "🌐 Website Scraper - Render Deployment Helper"
echo "=============================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if files are staged
if [ -z "$(git status --porcelain)" ]; then
    echo "📝 No changes to commit"
else
    echo "📝 Staging all files..."
    git add .
    
    echo "💾 Committing changes..."
    git commit -m "Update for Render deployment - $(date)"
    echo "✅ Changes committed"
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 No remote origin found."
    echo "Please add your GitHub repository as remote origin:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo ""
    echo "Then push your code:"
    echo "git push -u origin main"
else
    echo "🔗 Remote origin found: $(git remote get-url origin)"
    echo ""
    echo "📤 Pushing to GitHub..."
    git push origin main
    echo "✅ Code pushed to GitHub"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login and create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Use these settings:"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn --worker-class eventlet -w 1 wsgi:app --bind 0.0.0.0:\$PORT"
echo "   - Plan: Free"
echo ""
echo "🚀 Your app will be deployed automatically!"
echo "📖 See DEPLOYMENT.md for detailed instructions"
