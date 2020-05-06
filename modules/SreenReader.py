from PIL import Image, ImageGrab 
import numpy as np
import cv2
# for Fusion 3.64 and resolution 1366*768 - rect whit game (165, 30, 1201, 738)

class ScreenReaderClass():
    def __init__(self, ScreenShotingArea=(0, 0, 1366, 768)):
        self.ScreenShotingArea = ScreenShotingArea
        self.АctualScreenShot = self.SreenShot(ScreenShotingArea)
        self.SaveTestScreenShot(ScreenShotingArea)

        self.GRAY_MASK = ((0, 0, 5), (255, 255, 150))
        self.СutPicturesWithTheRoad = (500, 738)

    def SreenShot(self, ScreenShotRegion=None):
        return np.array(ImageGrab.grab(bbox=ScreenShotRegion))
    
    def SaveImage(self, Image, Name="SaveImage.png"):
        cv2.imwrite(Name, Image)

    def SaveTestScreenShot(self, ScreenShotRegion=None):
        self.SaveImage(self.SreenShot(ScreenShotRegion), 'TestScreenShot.png')

    def GetMask(self, Image=None, Mask=((0, 0, 0), (255, 255, 255))):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        
        HSVImage = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
        return  cv2.inRange(HSVImage[:, :, :], Mask[0], Mask[1])

    def GetGrayRoad(self, Image=None):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        GrayRoad = self.GetMask(Image, self.GRAY_MASK)[self.СutPicturesWithTheRoad[0]:self.СutPicturesWithTheRoad[1]]
        return GrayRoad

    def GetRoadMoment(self, Image=None):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        moments = cv2.moments(self.GetGrayRoad(Image), 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        x = int(dM10 / dArea)
        y = int(dM01 / dArea)

        return (int(x), int(y))
    
    def DrawPoint(self, Position, Image=None):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        cv2.line(Image, (Position[0], Position[1]), (Position[0], Position[1]),(255, 0, 0), 15)
        return Image
