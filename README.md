![Alt text](gallery/verticalSplit.png?raw=true "Compare videos for quality")
  
# Purpose
Inspired from the brilliant [Vivict](https://github.com/vivictorg/vivict) project, this program helps you visualize two videos side-by-side, with half of one video shown on the left and the other half on the right. It helps compare the quality of two videos. 
  
# Install
pip3 install -r requirements.txt
  
# Run
`python3 main.py -v video1.mkv video2.mp4`    
You can add more videos if you like:
`python3 main.py -v video1.mkv video2.mp4 video3.mkv`    
The maximum number of videos supported is the lowest value of the number of rows or columns of the smallest video, divided by 5 (where 5 is the minimum number of pixels that a video needs to display. You can change this value in the code). Displaying a lot of videos simultaneously requires a fast processor.
  
# Controls
* Esc to exit.
* Spacebar to pause for one second.
  
# TODO
* Videos of two different framerates.
* Split video depending on mouse pointer position. 
* Add more key and mouse controls.
* Add more video metadata displays on-screen.
* Add support for multiple monitors
* Support for showing grayscale videos (2D) along with colour videos (3D).