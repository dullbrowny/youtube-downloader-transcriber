#!/bin/bash

# Variables
REPO_NAME="youtube-downloader-transcriber"
GITHUB_USER="dullbrowny"
GITHUB_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"
LOCAL_DIR="$(pwd)/$REPO_NAME"

# Function to create a new repository on GitHub using GitHub API
create_github_repo() {
  curl -u "$GITHUB_USER" https://api.github.com/user/repos -d "{\"name\":\"$REPO_NAME\"}"
  echo "GitHub repository created: $GITHUB_URL"
}

# Check if the local repo exists
if [ -d "$LOCAL_DIR/.git" ]; then
  echo "Local Git repository already exists at $LOCAL_DIR"
else
  echo "Creating local repository at $LOCAL_DIR"
  mkdir -p $LOCAL_DIR
  cd $LOCAL_DIR

  # Initialize a git repository
  git init
  echo "# YouTube Playlist Downloader and Transcriber" >> README.md

  # Create requirements.txt
  echo "yt-dlp" >> requirements.txt
  echo "whisper" >> requirements.txt
  echo "google-auth" >> requirements.txt
  echo "google-auth-oauthlib" >> requirements.txt
  echo "google-auth-httplib2" >> requirements.txt
  echo "google-api-python-client" >> requirements.txt
  echo "tkinter" >> requirements.txt

  # Create a basic Python script
  cat <<EOL > yt_downloader.py
# Python code here (copy the yt_downloader.py code above)
EOL

  git add .
  git commit -m "Initial commit - YouTube Downloader and Transcriber"
fi

# Ensure the script is in the correct directory
cd $LOCAL_DIR

# Check

