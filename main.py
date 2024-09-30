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
    display.preCacheVideos()
    display.display()
    
    log.info("Program completed")
