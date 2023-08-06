#!/usr/bin/env python
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

def search_youtube_url(query):
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    print(f"API Key: {api_key}")
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query
    )
    response = request.execute()
    if not response['items']:
        return "No video found"
    video_id = response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    return video_url

if __name__ == "__main__":
    query = "Could an orca give a TED Talk?"
    print(search_youtube_url(query))