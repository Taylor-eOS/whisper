#!/bin/bash

# Check if a URL is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <youtube_url>"
    exit 1
fi

# Define the download path and template with timestamp
timestamp=$(date +%s)
download_path="$HOME/%(title)s_$timestamp.%(ext)s"

# Download the video with the specified format and output template
youtube_url="$1"
yt-dlp -f 251 -o "$download_path" "$youtube_url"

# Find the downloaded file
filename=$(find "$HOME" -type f -name "*_$timestamp.*")

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "The file '$filename' does not exist."
    exit 1
fi

# Run the file with the specified script
python3 ~/dev/whisper/whis.py "$filename"
