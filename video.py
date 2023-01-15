import cv2
import numpy as np

class VideoFile:
    """ Stores properties of the video """
    def __init__(self, videoNameWithPath) -> None:
        self.videoName = videoNameWithPath
        self.video = cv2.VideoCapture(self.videoName)
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.delay = int(self.fps)
        print(f"Video: {self.video}, height: {self.height}, width: {self.width}, fps: {self.fps}")
        self.windowName = 'video'
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.windowName, self.width, self.height) 
        while self.video.isOpened():
            ret, frame = self.video.read() #frame is a numpy nd array
            #print(f"Ret: {ret} Frame: {frame}")
            print(f"Type of frame {type(frame)}, dimensions {frame.shape}")
            if ret:
                x1 = 0; y1 = 0; x2 = 100; y2 = 100
                regionOfInterest = frame[y1:y2, x1:x2] #https://stackoverflow.com/questions/55943596/check-only-particular-portion-of-video-feed-in-opencv
                cv2.imshow(self.windowName, regionOfInterest)       
                keyCode = cv2.waitKey(self.delay) & 0xFF #https://stackoverflow.com/questions/57690899/how-cv2-waitkey1-0xff-ordq-works
                if keyCode == 27:#ord('q'):
                    break
            else:
                break
        self.close()

    def close(self):
        self.video.release()
        cv2.destroyAllWindows()

 
class DisplayVideos:
    """ Provides the functionality to display the videos next to each other """
    def __init__(self, videoLocations) -> None:
        self.videos = [VideoFile(videoFile) for videoFile in videoLocations]
        self.framerate = self.findMaxFramerate()
        self.width, self.height = self.determineMaxDisplaySize()

    def display(self):
        pass
    
    def determineMaxDisplaySize(self):
        width = max(set([video.width for video in self.videos]))
        height = max(set([video.height for video in self.videos]))
        return width, height

    def findMaxFramerate(self):
        return max(set([video.fps for video in self.videos]))
