import os
from googleapiclient.discovery import build

# Set up your API key
API_KEY = "YOUR_API_KEY_HERE"

# Function to fetch the transcript for a video
def get_transcript(video_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.captions().list(part="snippet", videoId=video_id)
    response = request.execute()
    if "items" in response:
        for item in response["items"]:
            caption_id = item["id"]
            caption_request = youtube.captions().download(id=caption_id)
            caption_response = caption_request.execute()
            if "body" in caption_response:
                return caption_response["body"]
    return None

# Function to fetch playlist items
def get_playlist_items(playlist_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=50)
    playlist_items = []
    while request:
        response = request.execute()
        playlist_items.extend(response["items"])
        request = youtube.playlistItems().list_next(request, response)
    return playlist_items

# Main function to fetch transcript for each video in a playlist
def fetch_playlist_transcripts(playlist_id):
    playlist_items = get_playlist_items(playlist_id)
    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        transcript = get_transcript(video_id)
        if transcript:
            print(f"Transcript for video {video_id}:")
            print(transcript)
        else:
            print(f"No transcript found for video {video_id}")

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fetch_playlist_transcripts.py <playlist_id>")
        sys.exit(1)
        
    playlist_id = "sys.argv[1]"
    fetch_playlist_transcripts(playlist_id)
