Compare multiple videos simultaneously by vertically splitting them:  
![Alt text](gallery/verticalSplit.png?raw=true "Compare multiple videos simultaneously by vertically splitting them")  
Compare videos of varied dimensions:  
![Alt text](gallery/differentSizes.png?raw=true "Compare videos of varied dimensions")  
Compare videos by horizontally splitting them and even viewing greyscale videos:  
![Alt text](gallery/greyHorizontalVaried.png?raw=true "Compare videos by horizontally splitting them and even viewing greyscale videos")  
You can view many more videos simultaneously.  
  
# Purpose
Inspired from the brilliant [Vivict](https://github.com/vivictorg/vivict) project, this program helps you visualize multiple videos side-by-side. It helps compare the quality difference between videos. This project was created because Vivict didn't support some file formats, and supported the display of only two videos simultaneously.
  
# Install
First you need to install some dependent libraries. Execute `pip3 install -r requirements.txt`. It's not necessary to install the exact versions mentioned in the `requirements.txt` file, so you can remove the `==versionNumber` if you'd like.
  
# Run
`python3 main.py -v video1.mkv video2.mp4`    
You can add more videos if you like:  
`python3 main.py -v video1.mkv video2.mp4 video3.flv video4.mov video5.ogx`    
The maximum number of videos supported, is the lowest value of the number of rows or columns of the smallest video, divided by 5 (where 5 is the minimum number of pixels that a video needs to display. You can change this value in the code). Displaying a lot of videos simultaneously requires a fast processor.
  
# Controls
* `Esc` to exit.
* `Spacebar` to pause for one second. You can press the spacebar multiple times to make it pause longer.
* `A` or `a` to toggle the axis of split (horizontal or vertical). The axis is vertical by default.
* `L` or `l` to toggle the display of the line separating the videos. This is switched on by default. No line will be shown if only one video is being played.
* `N` or `n` to toggle the display of filenames. This is switched off by default.
* `[` to cycle positions of the videos upward if split horizontally, and backward if split vertically.
* `]` to cycle positions of videos downward if split horizontally, and forward if split vertically.
* `up arrow` to decrease the delay between each frame shown (speeds the video if it had been slowed). 
* `down arrow` to increase the delay between each frame shown (slows the video).
* `left arrow` to seek backward.
* `right arrow` to seek forward toward any part of the video that has already been traversed and cached already.
    
# More info
* Videos will dynamically adapt to availability of video frames. So if two videos are played, where one ends after 1 minute and the other continues playing, the display will dynamically adapt to stop showing the first video when it no longer has any frames to display.
* No audio is played, since multiple videos may be involved. Also, since the focus is on visual quality evaluation.
* You can seek forward and backward only within the scope of how much of the video has already been played normally. This is because when the video plays normally, each frame is cached to allow for an accurate seek. Without this caching, [this unsolved issue](https://github.com/opencv/opencv/issues/9053) would lead to the video jumping to incorrect frames.  
* The seeking and slowing down or speeding up of the video have been implemented as fractions of the video which has the maximum framerate. If you are not comfortable with the granularity of it, you can alter it in `video.py` at the variables named `delayGranularity` and `seekGranularity` in the `DisplayVideos` class.
* Tested video formats: mkv, avi, mxf, flv, ogx, mp4, hevc, swf, m2ts, ts, m2v, vob, webm, mkv, wmv, mov, wtv, mpeg, 3gp, mpg, asf, mts (theoretically, it should support any video file that Python's OpenCV package supports).
  
# Known bug(s):
* If two videos of differing lengths are played, after the first one completes, the second one will be shown fullscreen and the line separator if present midscreen, will be switched off. Even if you seek backward until the first video appears back on screen, the line separator won't re-appear. This can be solved easily, but is left as-is for now as it isn't a critical feature.

# Feature upgrades possible:
* Split video depending on mouse pointer position (possibly practical only when not more than two videos are played simultaneously). 
* Add more key and mouse controls.
* Add more video metadata on-screen.
* Add support for multiple monitors
* Compare video quality objectively (https://superuser.com/a/338734/55249)

# Difficult to implement features:
Due to [this unsolved issue](https://github.com/opencv/opencv/issues/9053) with seek, the following features are difficult to implement:  
* Videos of two different framerates.
* Options for seeking to a specific point in the video and moving forward and backward (this has temporarily been solved partially, by caching the video upto whatever part of the video could be played normally).

  [![Donate](https://raw.githubusercontent.com/nav9/VCF_contacts_merger/main/gallery/thankYouDonateButton.png)](https://nrecursions.blogspot.com/2020/08/saying-thank-you.html)  
