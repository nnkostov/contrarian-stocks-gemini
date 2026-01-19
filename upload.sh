#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
  echo "Error: Please provide a commit message."
  echo "Usage: ./upload.sh \"Your commit message here\""
  exit 1
fi

echo "📦 Staging changes..."
git add .

echo "💾 Committing with message: '$1'..."
git commit -m "$1"

echo "🚀 Pushing to GitHub..."
git push

echo "✅ Done! Changes are live on GitHub."

