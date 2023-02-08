import cv2
import time
import numpy as np
from operatingSystem import screen
from loguru import logger as log

class Const:
    FIRST_LIST_ELEMENT = 0
    SECOND_LIST_ELEMENT = 0
    # MOUSE_HOVER_SPLIT_MAX_VIDEO = 4 #If MAX_SIMULTANEOUS_VIDEO_DISPLAY exceeds MOUSE_HOVER_SPLIT_MAX_VIDEO, the mouse hover (which dynamically alters the video split position) capability won't be available
    MAX_SIMULTANEOUS_VIDEO_DISPLAY = 8 #maximum number of videos that can be shown at once (feel free to increase this number as per the hardware capability of your computer). 
    NUMPY_HORIZONTAL_AXIS = 0
    NUMPY_VERTICAL_AXIS = 1

class VideoSplit:#The maximum number of splits will be approximately 10% of the smallest video's width or height (depending on whether it is split vertically or horizontally)
    NONE = None #There's only one video or none
    HORIZONTAL = 0 #videos will be split horizontally. To show 6 videos, there will be 5 splits horizontally. Video split position can change on mouse hover only if there are 2 videos.
    VERTICAL = 1 #videos will be split vertically. So to show 8 videos, there will be 7 vertical splits. Video split position can change on mouse hover only if there are 2 videos.

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
        log.info(f"Video: {self.video}, height: {self.height}, width: {self.width}, fps: {self.fps}, name: {videoNameWithPath}")

#Note: It's not necessary that all videos will have the same dimensions, codec or framerate
class VideoProcessor:
    """ Performs various calculations on the videos """
    def __init__(self) -> None:
        #self.videos = videos
        self.videoSplitType = None        
        #self.determineVideoSplitType() #Whether and how a video needs to be split
        self.videoOrder = []
        self.allowMouseHover = False
        self.splitLineColor = (255, 255, 255) #TODO: Draw half the line as black and half as white (or contrast it based on background pixel color)
        self.lineThickness = 1
        self.lineType = 8

    def determineVideoSplitType(self, videos):
        if len(videos) <= 1: self.videoSplitType = VideoSplit.NONE
        else: self.videoSplitType = Const.NUMPY_VERTICAL_AXIS #the default

    def toggleSplitAxis(self):
        if self.videoSplitType == Const.NUMPY_HORIZONTAL_AXIS: self.videoSplitType = Const.NUMPY_VERTICAL_AXIS
        if self.videoSplitType == Const.NUMPY_VERTICAL_AXIS: self.videoSplitType = Const.NUMPY_HORIZONTAL_AXIS

    def calculatePaddings(self, videos):
        self.determineVideoSplitType(videos)

    def splitAndArrangeVideoPieces(self, videos, mouseX=0, mouseY=0):#videos is a dict {VideoFile object: video frame}
        if self.videoOrder != list(videos.keys()):#check if keys are in the exact same order (to ensure that the User did not change anything and to ensure that all video frames are the same as they were previously, because sometimes a video may run out of frames while the other videos continue playing)
            self.calculatePaddings(videos)
            self.videoOrder = list(videos.keys())
        #--- hardcoding temporarily
        counter = 0
        for video in videos:
            if counter == 0: 
                leftVideo = video
                leftVideoFrame = videos[video]
            if counter == 1: 
                rightVideo = video
                rightVideoFrame = videos[video]
            counter += 1
        #--- Region of Interest: Left/top side        
        if self.videoSplitType == VideoSplit.VERTICAL: 
            x1 = 0; y1 = 0; x2 = int(leftVideo.width / 2); y2 = leftVideo.height                
        if self.videoSplitType == Const.NUMPY_HORIZONTAL_AXIS:            
            x1 = 0; y1 = int(leftVideo.height / 2); x2 = leftVideo.width; y2 = leftVideo.height
        leftRegionOfInterest = leftVideoFrame[y1:y2, x1:x2] #https://stackoverflow.com/questions/55943596/check-only-particular-portion-of-video-feed-in-opencv
        #--- Region of Interest: Right/bottom side
        if self.videoSplitType == VideoSplit.VERTICAL:
            x1 = int(rightVideo.width / 2); y1 = 0; x2 = rightVideo.width; y2 = rightVideo.height
        if self.videoSplitType == Const.NUMPY_HORIZONTAL_AXIS:                            
            x1 = 0; y1 = int(rightVideo.height / 2); x2 = rightVideo.width; y2 = rightVideo.height
        rightRegionOfInterest = rightVideoFrame[y1:y2, x1:x2]

        joined = np.concatenate((leftRegionOfInterest, rightRegionOfInterest), axis=self.videoSplitType)
        #---draw the splitter line 
        point1 = None; point2 = None
        if self.videoSplitType == VideoSplit.VERTICAL:
            point1 = (x1, y1); point2 = (x1, y2)
        if self.videoSplitType == Const.NUMPY_HORIZONTAL_AXIS:
            point1 = (x1, y1); point2 = (x2, y1)
        cv2.line(img=joined, pt1=point1, pt2=point2, color=self.splitLineColor, thickness=self.lineThickness, lineType=self.lineType, shift=0)
        return joined

class DisplayVideos:
    """ Receives video frames and displays videos together """
    def __init__(self, videoLocations) -> None:
        self.videos = [VideoFile(videoFile) for videoFile in videoLocations]
        self.framerate = self.findMaxFramerate()
        self.width, self.height = self.findMaxDisplaySize()
        self.defaultDelay = int(self.framerate)  
        self.processor = VideoProcessor()

    def display(self):
        #Concatenate images: https://stackoverflow.com/questions/7589012/combining-two-images-with-opencv
        self.windowName = 'Comparing Videos'
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.windowName, self.width, self.height)         
        while True:
            #---iterate videos assuming that one of them might stop supplying frames eariler than the others
            activeVideos = dict()            
            for video in self.videos:
                if video.video.isOpened():
                    gotValidFrame, videoFrame = video.video.read() #frame is a numpy nd array
                    if gotValidFrame:
                        activeVideos[video] = videoFrame
            if not activeVideos:#if there are no active videos remaining
                break #exit while
            joined = self.processor.splitAndArrangeVideoPieces(activeVideos)
            cv2.imshow(self.windowName, joined)       
            keyCode = cv2.waitKey(self.defaultDelay) & 0xFF #https://stackoverflow.com/questions/57690899/how-cv2-waitkey1-0xff-ordq-works
            if keyCode == KeyCodes.ESC:
                break
            if keyCode == KeyCodes.SPACEBAR:
                time.sleep(1)
            if keyCode == ord('s') or keyCode == ord('S'):#to split the video horizontally
                self.processor.toggleSplitAxis()
            #time.sleep(0.05) #0.05 is 50 millisecond
        self.close()
        
    # def display(self):
    #     #Concatenate images: https://stackoverflow.com/questions/7589012/combining-two-images-with-opencv
    #     self.windowName = 'Comparing Videos'
    #     cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
    #     cv2.resizeWindow(self.windowName, self.width, self.height) 
    #     while self.leftVideo.video.isOpened() and self.rightVideo.video.isOpened():
    #         returnValueLeft, leftVideoFrame = self.leftVideo.video.read() #frame is a numpy nd array
    #         returnValueRight, rightVideoFrame = self.rightVideo.video.read() 
    #         if returnValueLeft and returnValueRight:#obtained both frames
    #             joined = self.processor.splitVideo(leftVideoFrame, self.leftVideo, rightVideoFrame, self.rightVideo)
    #             cv2.imshow(self.windowName, joined)       
    #             keyCode = cv2.waitKey(self.defaultDelay) & 0xFF #https://stackoverflow.com/questions/57690899/how-cv2-waitkey1-0xff-ordq-works
    #             if keyCode == KeyCodes.ESC:
    #                 break
    #             if keyCode == KeyCodes.SPACEBAR:
    #                 time.sleep(1)
    #             if keyCode == ord('s') or keyCode == ord('S'):#to split the video horizontally
    #                 self.processor.toggleSplitAxis()
    #         else:#either the left or right frame or both could not be obtained
    #             break
    #         #time.sleep(0.05) #0.05 is 50 millisecond
    #     self.close()

    def close(self):
        """ Clear resources """
        for video in self.videos:
            video.video.release()
        cv2.destroyAllWindows()

    def findMaxDisplaySize(self):
        """ Returns the maximum width of any video and maximum height of any video in the list of videos """
        monitor = screen.MonitorInfo()
        monitorWidth, monitorHeight = monitor.getMonitorDimensions()
        width = max(set([video.width for video in self.videos]))
        height = max(set([video.height for video in self.videos]))
        if width > monitorWidth or height > monitorHeight:
            log.warning(f"\n\nYour primary monitor width {monitorWidth} and height {monitorHeight} are less than the video width {width} and height {height}.")
        return width, height

    def findMaxFramerate(self):
        """ Returns the maximum framerate among all videos """
        return max(set([video.fps for video in self.videos]))
