from googleapiclient.discovery import build

# Enter your API key here
API_KEY = "AIzaSyBhUjwo5XZnwFsN7RJk5Bcg3tbV4RAtAAg"
youtube = build("youtube", "v3", developerKey=API_KEY)

def search_videos_by_tag(user_tag, search_query=""):
    # Step 1: Search for videos (broad search)
    search_response = youtube.search().list(
        q=search_query or user_tag,  # fallback to tag as keyword
        type="video",
        part="id",
        maxResults=20  # number of results to check
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response['items']]

    # Step 2: Get video details (including tags)
    videos_response = youtube.videos().list(
        id=",".join(video_ids),
        part="snippet"
    ).execute()

    # Step 3: Filter videos by tag
    matching_links = []
    for video in videos_response['items']:
        tags = video['snippet'].get('tags', [])
        if user_tag.lower() in [t.lower() for t in tags]:
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            matching_links.append(video_url)

    return matching_links

# Example usage
if __name__ == "__main__":
    tag_input = input("Enter a tag to search for: ")
    results = search_videos_by_tag(tag_input)

    if results:
        print("\nVideos found with tag:", tag_input)
        for link in results:
            print(link)
    else:
        print("No videos found with that tag.")
