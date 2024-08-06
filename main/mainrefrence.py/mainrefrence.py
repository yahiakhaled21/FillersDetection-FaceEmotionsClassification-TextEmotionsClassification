# main.py
import script1

video_path = "Testing\Tell Me About Yourself.mp4"

# Call the function from script1 to process the video and get information
result = script1.process_video_and_get_info(video_path)

if result is not None:
    total_frames, frame_width, frame_height = result
    print(f"Total Frames: {total_frames}")
    print(f"Frame Width: {frame_width}")
    print(f"Frame Height: {frame_height}")
else:
    print("Error processing video in script1.py")
