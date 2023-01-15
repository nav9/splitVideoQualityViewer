import video

if __name__ == "__main__":
    videos = ["/home/navin/code/ffmpegProfilerFindingOptimalSettings/originals/surfing.mkv",
                "/home/navin/code/ffmpegProfilerFindingOptimalSettings/encoded/surfing/o-presetfast_-crf35_.mp4"]
    display = video.DisplayVideos(videos)
    display.display()
    
    print("Completed")
