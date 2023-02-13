import cv2
import time
import math
import numpy as np
from operatingSystem import screen
from loguru import logger as log
from collections import namedtuple

class Const:
    FIRST_LIST_ELEMENT = 0
    SECOND_LIST_ELEMENT = 0
    # MOUSE_HOVER_SPLIT_MAX_VIDEO = 4 #If MAX_SIMULTANEOUS_VIDEO_DISPLAY exceeds MOUSE_HOVER_SPLIT_MAX_VIDEO, the mouse hover (which dynamically alters the video split position) capability won't be available
    MAX_SIMULTANEOUS_VIDEO_DISPLAY = 8 #maximum number of videos that can be shown at once (feel free to increase this number as per the hardware capability of your computer). 
    #NUMPY_HORIZONTAL_AXIS = 0
    #NUMPY_VERTICAL_AXIS = 1
    RGB_VIDEO_DIMENSION_LEN = 3

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
        self.x1 = None #start x coordinate for portion of split video to display
        self.y1 = None #start y coordinate for portion of split video to display
        self.x2 = None #end x coordinate for portion of split video to display
        self.y2 = None #end y coordinate for portion of split video to display
        self.padding = namedtuple('Padding', 'top bottom left right')
        self.setPadding(0, 0, 0, 0)
        #self.padding = self.makePaddingEmptyArray()
    
    def setPadding(self, top, bottom, left, right):
        self.padding.top = top; self.padding.bottom = bottom; self.padding.left = left; self.padding.right = right

    # def createPadding(self, frame, paddingWidth, paddingHeight):
    #     if len(frame.shape) == Const.RGB_VIDEO_DIMENSION_LEN:#is a video with (height, width, RGB depth)
    #         self.padding = np.zeros((paddingHeight, paddingWidth, Const.RGB_VIDEO_DIMENSION_LEN))

#Note: It's not necessary that all videos will have the same dimensions, codec or framerate
class VideoProcessor:
    """ Performs various calculations on the videos """
    def __init__(self) -> None:
        #self.videos = videos
        self.videoSplitType = VideoSplit.NONE
        #self.determineVideoSplitType() #Whether and how a video needs to be split
        self.videoOrder = []
        self.allowMouseHover = False
        self.splitLineColor = (255, 255, 255) #TODO: Draw half the line as black and half as white (or contrast it based on background pixel color)
        self.lineThickness = 1
        self.lineType = 8

    def determineVideoSplitType(self, videos):
        if len(videos) > 1 and self.videoSplitType == VideoSplit.NONE: #if the videoSplitType has never neen assigned based on the number of videos (when there are more than 1 video)
            self.videoSplitType = VideoSplit.VERTICAL #the default

    def toggleSplitAxis(self, videos):
        if self.videoSplitType == VideoSplit.NONE: log.error(f"No split type has been set yet. You can only set it after any valid video is detected. Also, there's no point setting a split type when there's only one video.")
        else:
            if self.videoSplitType == VideoSplit.HORIZONTAL: self.videoSplitType = VideoSplit.VERTICAL
            else:
                if self.videoSplitType == VideoSplit.VERTICAL: self.videoSplitType = VideoSplit.HORIZONTAL
        self.calculateSplitDimensionsAndPaddings(videos)

    #https://stackoverflow.com/questions/43391205/add-padding-to-images-to-get-them-into-the-same-shape
    def calculateSplitDimensionsAndPaddings(self, videos):#if videos are of different sizes, to join pieces of their frames, you need to pad the remaining space with zeroes
        #Note: videos is a dict {video object reference: video frame}. The frame is a numpy array (videoHeight, videoWidth, rgb axis)
        self.determineVideoSplitType(videos)
        widths = set([video.width for video in videos])
        heights = set([video.height for video in videos])
        self.maxWidth = max(widths)#; minWidth = min(widths)
        self.maxHeight = max(heights)#; minHeight = min(heights)        
        #---find coordinates to split each video into and the padding it needs
        splitPercentage = 1 / len(videos)
        ordinal = 0#; FIRST_VIDEO = 0; LAST_VIDEO = len(videos)-1
        print(f"---new split dimensions. SplitType: {self.videoSplitType}")
        for video in videos:            
            top = 0; bottom = self.maxHeight - video.height; left = 0; right = 0 #padding values
            if self.videoSplitType == VideoSplit.VERTICAL:
                video.y1 = 0; video.y2 = video.height
                video.x1 = math.floor(ordinal * (video.width * splitPercentage))
                video.x2 = math.floor(video.x1 + (video.width * splitPercentage))
                #---padding calculation
                if video.height != self.maxHeight: #video.makePaddingEmptyArray() #no need of padding, since the video is as big as the largest video
                    bottom = self.maxHeight - video.height                    
                    #videos[video] = cv2.copyMakeBorder(videos[video], top, bottom, left, right, cv2.BORDER_CONSTANT)
                    print(f"w {video.width} h {video.height}. Padding bottom {bottom}")
                else: print(f"{video.height}={self.maxHeight}. No padding needed")
                #else: video.createPadding(videos[video], video.x2 - video.x1, maxHeight - video.y2)                
            if self.videoSplitType == VideoSplit.HORIZONTAL:
                video.x1 = 0; video.x2 = video.width
                video.y1 = math.floor(ordinal * (video.height * splitPercentage))
                video.y2 = math.floor(video.y1 + (video.height * splitPercentage))                
                #---padding calculation
                if video.width != self.maxWidth: #video.makePaddingEmptyArray() #no need of padding, since the video is as big as the largest video
                    right = self.maxWidth - video.width
                    #videos[video] = cv2.copyMakeBorder(videos[video], top, bottom, left, right, cv2.BORDER_CONSTANT)
                    print(f"w {video.width} h {video.height}. Padding right {right}")
                else: print(f"{video.width}={self.maxWidth}. No padding needed")
                #else: video.createPadding(videos[video], maxWidth - video.x2, video.y2 - video.y1)
            video.setPadding(top, bottom, left, right)
            #---generate numpy array with padding
            ordinal += 1                

    def splitAndArrangeVideoPieces(self, videos, mouseX=0, mouseY=0):#videos is a dict {VideoFile object: video frame}
        if self.videoOrder != list(videos.keys()):#check if keys are in the exact same order (to ensure that the User did not change anything and to ensure that all video frames are the same as they were previously, because sometimes a video may run out of frames while the other videos continue playing)
            self.calculateSplitDimensionsAndPaddings(videos)
            self.videoOrder = list(videos.keys())
        paddingAxis = 0
        if self.videoSplitType == 0: paddingAxis = 1 #the axis along which padding arrays are joined with their respective video arrays, is the opposite axis of the video slices being joined with each other
        #---join the various video slices
        joined = np.array(None); EMPTY_ARRAY = 1
        print(f"=========== new. splitType {self.videoSplitType}")
        for video in videos:
            print(f"w {video.width} h {video.height} vid {video}")
            #---apply padding
            videos[video] = cv2.copyMakeBorder(videos[video], video.padding.top, video.padding.bottom, video.padding.left, video.padding.right, cv2.BORDER_CONSTANT)
            #---cut desired portion of frame
            newFrame = videos[video][video.y1:self.maxHeight, video.x1:self.maxWidth] #select region to be displayed
            print(f"newframe shape {newFrame.shape}")
            #---join the padding with the video slice
            #if video.padding.size != EMPTY_ARRAY: padded = np.concatenate((newFrame, video.padding), axis=paddingAxis)                
            #else: padded = newFrame
            #---join the padded video slice with the other video slices
            if joined.size == EMPTY_ARRAY: joined = newFrame
            else: joined = np.concatenate((joined, newFrame), axis=self.videoSplitType)
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
                        #print(f"dimensions:  {videoFrame.ndim}, {videoFrame.shape}")
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
                print("\n\n\n\n TOGGLE DETECTED \n\n\n\n")
                self.processor.toggleSplitAxis(activeVideos)            
            #time.sleep(0.05) #0.05 is 50 millisecond
        self.close()

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
