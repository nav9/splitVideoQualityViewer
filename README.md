![Alt text](gallery/verticalSplit.png?raw=true "Compare videos for quality")
  
# Purpose
Inspired from the brilliant [Vivict](https://github.com/vivictorg/vivict) project, this program helps you visualize two videos side-by-side, with half of one video shown on the left and the other half on the right. It helps compare the quality of two videos. 
  
# Install
pip3 install -r requirements.txt
  
# Run
`python3 main.py -v video1.mkv video2.mp4`  
  
# Controls
* Esc to exit.
* Spacebar to pause for one second.
  
# TODO
* Videos of two different framerates.
* Split video depending on mouse pointer position.
* Support for more than two videos shown simultaneously. 
* Checking if video can be displayed within current screen limits.
* Add more key and mouse controls.
* Add more video metadata displays on-screen.
* Won't implement: Videos of different dimensions (this is difficult to do in Python, since it needs high processing power. Skipping this).
* Add support for multiple monitors