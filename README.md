![Alt text](gallery/verticalSplit.png?raw=true "Compare videos for quality")
  
# Purpose
Inspired from the brilliant [Vivict](https://github.com/vivictorg/vivict) project, this program helps you visualize multiple videos side-by-side. It helps compare the quality difference between videos. 
  
# Install
pip3 install -r requirements.txt
  
# Run
`python3 main.py -v video1.mkv video2.mp4`    
You can add more videos if you like:  
`python3 main.py -v video1.mkv video2.mp4 video3.mkv`    
The maximum number of videos supported is the lowest value of the number of rows or columns of the smallest video, divided by 5 (where 5 is the minimum number of pixels that a video needs to display. You can change this value in the code). Displaying a lot of videos simultaneously requires a fast processor.
  
# Controls
* `Esc` to exit.
* `Spacebar` to pause for one second.
* `A` or `a` to toggle the axis of split (horizontal or vertical).
* `L` or `l` to toggle the display of the line separating the videos. No line will be shown if only one video is being played.
    
# Extra functionality explanation
* Videos will dynamically adapt to availability of video frames. So if two videos are played, where one ends after 1 minute and the other continues playing, the display will dynamically adapt to stop showing the first video when it no longer has any frames to display.
* No audio is played, since multiple videos may be involved. Also, the focus is on visual quality evaluation.
* Tested filetypes: mkv, mp4 (though it should support any video file that Python OpenCV supports).
  
# TODO
* Videos of two different framerates.
* Split video depending on mouse pointer position. 
* Add more key and mouse controls.
* Add more video metadata displays on-screen.
* Add support for multiple monitors
* Support for showing grayscale videos (2D) along with colour videos (3D).
* Compare video quality objectively (https://superuser.com/a/338734/55249)