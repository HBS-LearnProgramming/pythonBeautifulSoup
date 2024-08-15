import os
import json
import googleapiclient.discovery
import googleapiclient.errors

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyBByOd1BTwwL4vHJ_g5ox7RkRqhC8pFuU4"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

# Function to load existing data from JSON if it exists
def load_existing_data():
    if os.path.exists('youtube_review.json'):
        with open('youtube_review.json', 'r') as json_file:
            return json.load(json_file)
    return []

# Function to save data to JSON
def save_data_to_json(data):
    with open('youtube_review.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Load existing data
existing_data = load_existing_data()

# Get the video title
video_id = "H71IxqmCfxQ"
video_request = youtube.videos().list(
    part="snippet",
    id=video_id
)
video_response = video_request.execute()
video_title = video_response['items'][0]['snippet']['title']

# Prepare the new data entry
new_entry = {
    "video_id": video_id,
    "video_title": video_title,
    "comments": []
}

# Get the comments
comment_request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=100
)
comment_response = comment_request.execute()

for item in comment_response['items']:
    comment_data = {
        "author_name": item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
        "comment": item['snippet']['topLevelComment']['snippet']['textOriginal'],
        "likes": item['snippet']['topLevelComment']['snippet']['likeCount']
    }
    new_entry["comments"].append(comment_data)

# Append the new entry to the existing data
existing_data.append(new_entry)

# Save the updated data back to JSON
save_data_to_json(existing_data)

print(f"Data has been written to youtube_review.json:{existing_data}")
