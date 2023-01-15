import cv2
import time
import numpy as np

class KeyCodes:
    ESC = 27
    SPACEBAR = 32

class VideoFile:
    """ Stores properties of the video """
    def __init__(self, videoNameWithPath) -> None:
        self.videoName = videoNameWithPath
        self.video = cv2.VideoCapture(self.videoName)
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)        
        print(f"Video: {self.video}, height: {self.height}, width: {self.width}, fps: {self.fps}")

#TODO: This has currently been designed to support only two videos, but can be made generic to support more
class DisplayVideos:
    """ Provides the functionality to display the videos next to each other """
    def __init__(self, videoLocations) -> None:
        self.videos = [VideoFile(videoFile) for videoFile in videoLocations]
        MAX_VIDEOS_MOUSE_HOVER_SUPPORTS = 4
        self.mouseHoverSupport = True
        if len(self.videos) > MAX_VIDEOS_MOUSE_HOVER_SUPPORTS:
            self.mouseHoverSupport = False
        self.framerate = self.findMaxFramerate()
        self.width, self.height = self.determineMaxDisplaySize()
        self.delay = int(self.framerate)
        #---TODO: Make video display more generic. Hardcoding now to create a basic version
        self.leftVideo = self.videos[0]
        self.rightVideo = self.videos[1]

    def display(self):
        #Concatenate images: https://stackoverflow.com/questions/7589012/combining-two-images-with-opencv
        self.windowName = 'Comparing'
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.windowName, self.width, self.height) 
        while self.leftVideo.video.isOpened() and self.rightVideo.video.isOpened():
            ret_left, frame_left = self.leftVideo.video.read() #frame is a numpy nd array
            ret_right, frame_right = self.rightVideo.video.read() 
            if ret_left and ret_right:
                x1 = 0; y1 = 0; x2 = int(self.leftVideo.width / 2); y2 = self.leftVideo.height                
                regionOfInterest_left = frame_left[y1:y2, x1:x2] #https://stackoverflow.com/questions/55943596/check-only-particular-portion-of-video-feed-in-opencv
                x1 = int(self.rightVideo.width / 2); y1 = 0; x2 = self.rightVideo.width; y2 = self.rightVideo.height
                regionOfInterest_right = frame_right[y1:y2, x1:x2]
                joined = np.concatenate((regionOfInterest_left, regionOfInterest_right), axis=1)
                #---draw the vertical line TODO: Draw half the line as black and half as white (or contrast it based on background pixel color)
                cv2.line(img=joined, pt1=(x1, y1), pt2=(x1, y2), color=(255, 255, 255), thickness=1, lineType=8, shift=0)                
                cv2.imshow(self.windowName, joined)       
                keyCode = cv2.waitKey(self.delay) & 0xFF #https://stackoverflow.com/questions/57690899/how-cv2-waitkey1-0xff-ordq-works
                if keyCode == KeyCodes.ESC:
                    break
                if keyCode == KeyCodes.SPACEBAR:
                    time.sleep(1)
                if keyCode == ord('h'):#to split the video horizontally
                    pass
            else:
                break
        self.close()

    def close(self):
        for video in self.videos:
            video.video.release()
        cv2.destroyAllWindows()

    def determineMaxDisplaySize(self):
        width = max(set([video.width for video in self.videos]))
        height = max(set([video.height for video in self.videos]))
        return width, height

    def findMaxFramerate(self):
        return max(set([video.fps for video in self.videos]))
