import sys
import os
import pymongo
import main

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://instajob:80z93toSszx6yIlt@cluster0.csynum6.mongodb.net/?retryWrites=true&w=majority")
db = client["instajob"]
collection = db["videointerviews"]

# Ensure videos directory exists
videos_dir = "videos"
os.makedirs(videos_dir, exist_ok=True)

# Define a function to process new documents
def process_new_document(change):
    # Get the new document
    new_document = change["fullDocument"]
    # Retrieve the video blob from the new document
    video_blob = new_document["video"]
    # Generate a unique video path
    video_path = os.path.join(videos_dir, f"{new_document['_id']}.mp4")
    # Write the video blob to a file
    with open(video_path, "wb") as f:
        f.write(video_blob)
    # Process the video using main.py
    process_video(video_path, new_document)

# Function to process a single video using main.py
def process_video(video_path, video_document):
    print(f"Processing video: {video_path}")
    final_score = main.main(video_path)  # Get the final score from main.main
    if final_score is not None:
        print("Processing complete for:", video_path)
        video_id = video_document["_id"]
        collection.update_one(
            {"_id": video_id},
            {"$set": {"finalScore": final_score}},
            upsert=True  # Add the field if it doesn't exist
        )
        print("Final score updated for video:", video_id)
    else:
        print("Processing failed for:", video_path)

# Watch the collection for changes
with collection.watch() as stream:
    print("Watching for changes in the collection...")
    for change in stream:
        if change["operationType"] == "insert":
            process_new_document(change)
