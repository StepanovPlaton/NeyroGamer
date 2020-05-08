from PIL import Image as PILImage, ImageGrab 
import numpy as np
import cv2, time, math
import threading
from flask import Flask, render_template, Response

# for Fusion 3.64 and resolution 1366*768 - rect whit game (165, 30, 1201, 738)

class ScreenReaderClass():
    def __init__(self, ScreenShotingArea=(0, 0, 1366, 768)):
        self.ScreenShotingArea = ScreenShotingArea
        self.АctualScreenShot = self.SreenShot(ScreenShotingArea)
        self.SaveTestScreenShot(ScreenShotingArea)

        self.GRAY_MASK = ((0, 0, 15), (255, 255, 150))
        self.СutPicturesWithTheRoadUP = (525, 550)
        self.СutPicturesWithTheRoadDOWN = (650, 738)

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

    def GetRoadMoment(self, Image=None):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)

        GrayRoadUp = self.GetMask(Image, self.GRAY_MASK)[self.СutPicturesWithTheRoadUP[0]:self.СutPicturesWithTheRoadUP[1]]
        GrayRoadDown = self.GetMask(Image, self.GRAY_MASK)[self.СutPicturesWithTheRoadDOWN[0]:self.СutPicturesWithTheRoadDOWN[1]]

        self.SaveImage(GrayRoadUp, "GRAY_ROAD_UP.png")
        self.SaveImage(GrayRoadDown, "GRAY_ROAD_DOWN.png")

        moments = cv2.moments(GrayRoadUp, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        x1=-1
        y1=-1
        if(dArea != 0):
            x1 = int(dM10 / dArea)
            y1 = int(dM01 / dArea)

        moments = cv2.moments(GrayRoadDown, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        x2=-1
        y2=-1
        if(dArea != 0):
            x2 = int(dM10 / dArea)
            y2 = int(dM01 / dArea)

        return [(int(x1), int(y1)), (int(x2), int(y2))]
    
    def DrawPoint(self, Position, Image=None):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        cv2.line(Image, (Position[0], Position[1]), (Position[0], Position[1]),(255, 0, 0), 15)
        return Image

    def demon(self):
        app = Flask(__name__)

        def image2jpeg(image):
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

        @app.route('/')
        def index():
            return render_template('index.html')

        def Gen():
            count = 0
            while True:
                count+=1
                if(count >= 100): Color = True
                elif(count >= 0): Color = False
                if(count > 200): count = 0
                
                if(Color): image = cv2.cvtColor(self.SreenShot(self.ScreenShotingArea), cv2.COLOR_RGB2BGR)
                else: 
                    image_gray = self.GetMask(None, self.GRAY_MASK)
                    image = cv2.cvtColor(self.GetMask(None, self.GRAY_MASK), cv2.COLOR_GRAY2BGR)
                    
                #image = cv2.copyMakeBorder(image, 0, 0, 0, 500, cv2.BORDER_CONSTANT, value=(0, 0, 0))
                if(not Color):
                    (x1, _), (x2, _) =  self.GetRoadMoment()

                    point1 = (x1, int((self.СutPicturesWithTheRoadUP[0]+self.СutPicturesWithTheRoadUP[1])/2))
                    point2 = (x2, int((self.СutPicturesWithTheRoadDOWN[0]+self.СutPicturesWithTheRoadDOWN[1])/2))
                    deviation_point1 = int(x1 - abs(self.ScreenShotingArea[0]-self.ScreenShotingArea[2])/2)
                    deviation_point2 = int(x2 - abs(self.ScreenShotingArea[0]-self.ScreenShotingArea[2])/2)

                    distance_between_x1_x2 = abs(int((self.СutPicturesWithTheRoadUP[0]+self.СutPicturesWithTheRoadUP[1])/2) -
                                                    int((self.СutPicturesWithTheRoadDOWN[0]+self.СutPicturesWithTheRoadDOWN[1])/2))

                    angle = math.tan(distance_between_x1_x2/(abs(x1-x2)+0.01))*(180/3.14)
                    if(x2<x1): angle *= -1

                    cv2.line(image, point1, point2, (255, 0, 0), 10)
                    cv2.line(image, (x1+int(self.ScreenShotingArea[2]/8), self.СutPicturesWithTheRoadUP[0]), 
                                    (x2+int(self.ScreenShotingArea[2]/2), self.СutPicturesWithTheRoadDOWN[1]), 
                                    (255, 0, 0), 10)
                    cv2.line(image, (x1-int(self.ScreenShotingArea[2]/8), self.СutPicturesWithTheRoadUP[0]), 
                                    (x2-int(self.ScreenShotingArea[2]/2),self.СutPicturesWithTheRoadDOWN[1]), 
                                    (255, 0, 0), 10)

                    cv2.putText(image, "X center of the road at the bottom of the frame = "+str(x1), (self.ScreenShotingArea[2]-1000, 270), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                    cv2.putText(image, "Deviation of the road from the center from below = "+str(deviation_point1), (self.ScreenShotingArea[2]-1000, 300), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                    cv2.putText(image, "X center of the road on top of the frame = "+str(x2), (self.ScreenShotingArea[2]-1000, 350), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                    cv2.putText(image, "Deviation of the road from the center from above = "+str(deviation_point2), (self.ScreenShotingArea[2]-1000, 380), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                    cv2.putText(image, "Road angle = "+str(angle), (self.ScreenShotingArea[2]-1000, 410), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                    image = np.array(image)
                    
                    image[np.where((image==[255,255,255]).all(axis=2))] = [0, 255, 0]
                        #image = cv2.bitwise_and(image, image, mask=image_gray)
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + image2jpeg(image) + b'\r\n\r\n')
                
        @app.route('/video')
        def video():
            return Response(Gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        app.run(host='0.0.0.0', debug=False, threaded=True)

    def StartDemon(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()
