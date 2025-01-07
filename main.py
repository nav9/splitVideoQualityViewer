import video
import argparse
from loguru import logger as log

if __name__ == "__main__":
    log.info('Program begins')
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", type=str, nargs='+', required=True, help='Usage: python3 main.py -v video1.mkv video2.mp4 video3.mkv video4.mkv')
    args = parser.parse_args()

    log.info(f"Videos: {args.v}")
    display = video.DisplayVideos(args.v)
    print("-----------------------------------------")
    print("| Welcome to Split Video Quality Viewer |")
    print("-----------------------------------------")
    print("There is an unsolved bug in OpenCV and encoders due to which seeking (jumping) to random points in a video is time consuming and may")
    print("cause errors in the exact frame reached during seek. To mitigate this, a pre-caching feature has been implemented, which pre-loads")
    print("all videos into memory before displaying them. This is ok for small videos, but can consume massive memory for large videos. If you have")
    print("large videos, it is recommended you do not use pre-caching. Although do remember that not pre-caching will mean that your ")
    print("video seek (jumping to specific positions in the video) may not be accurate, and frames of videos may not match exactly after the seek.")
    print("\nPlease press Enter or Y or y to proceed without pre-caching. To use pre-caching, press N or n")
    response = input("Do you want to avoid pre-caching: [y/n] : ")
    if response.lower() == "n":
        display.preCacheVideos()
    else:
        display.doNotPreCacheVideos()        

    display.display()
    
    log.info("Program completed")
