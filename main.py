import video
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=str)
    parser.add_argument("right", type=str)
    args = parser.parse_args()

    videos = [args.left, args.right]
    display = video.DisplayVideos(videos)
    display.display()
    
    print("Completed")
