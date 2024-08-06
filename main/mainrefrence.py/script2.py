import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script1.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]

    print(f"Analyzing video at path: {video_path}")

    # x1 = analyze_video(video_path)
    # print(x1)
