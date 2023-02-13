![Alt text](gallery/verticalSplit.png?raw=true "Compare videos for quality")
  
# Purpose
Inspired from the brilliant [Vivict](https://github.com/vivictorg/vivict) project, this program helps you visualize multiple videos side-by-side. It helps compare the quality difference between videos. This project was created because Vivict didn't support some file formats, and supported the display of only two videos simultaneously.
  
# Install
pip3 install -r requirements.txt
  
# Run
`python3 main.py -v video1.mkv video2.mp4`    
You can add more videos if you like:  
`python3 main.py -v video1.mkv video2.mp4 video3.mkv`    
The maximum number of videos supported is the lowest value of the number of rows or columns of the smallest video, divided by 5 (where 5 is the minimum number of pixels that a video needs to display. You can change this value in the code). Displaying a lot of videos simultaneously requires a fast processor.
  
# Controls
* `Esc` to exit.
* `Spacebar` to pause for one second. You can press the spacebar multiple times to make it pause longer.
* `A` or `a` to toggle the axis of split (horizontal or vertical). This is vertical by default.
* `L` or `l` to toggle the display of the line separating the videos. This is switched on by default. No line will be shown if only one video is being played.
* `N` or `n` to toggle the display of filenames. This is switched off by default.
* `up arrow key` to switch positions of the videos upward if split horizontally, and backward if split vertically.
* `down arrow key` to switch positions of videos downward if split horizontally, and forward if split vertically.
    
# More info
* Videos will dynamically adapt to availability of video frames. So if two videos are played, where one ends after 1 minute and the other continues playing, the display will dynamically adapt to stop showing the first video when it no longer has any frames to display.
* No audio is played, since multiple videos may be involved. Also, the focus is on visual quality evaluation.
* Tested video formats: mkv, avi, mxf, flv, ogx, mp4, hevc, swf, m2ts, ts, m2v, vob, mjpeg, webm, mkv, wmv, mov, wtv, mpeg, 3gp, mpg, asf, mts (theoretically, it should support any video file that Python's OpenCV package supports).
  
# TODO
* Videos of two different framerates.
* Split video depending on mouse pointer position. 
* Add more key and mouse controls.
* Add more video metadata on-screen.
* Add support for multiple monitors
* Options for seeking to a specific point in the video and moving forward and backward.
* Video speed adjustment.
* Compare video quality objectively (https://superuser.com/a/338734/55249)