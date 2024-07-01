#!/bin/bash

# Check if a URL is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <youtube_url>"
    exit 1
fi

# Define the download path and template
download_path="~/Downloads/%(title)s.%(ext)s"

# Download the video with the specified format and output template
youtube_url="$1"
filename=$(yt-dlp -f 251 -o "$download_path" --get-filename "$youtube_url")

# Run the file with the specified script
python3 ~/dev/whisper/whis.py "$filename"