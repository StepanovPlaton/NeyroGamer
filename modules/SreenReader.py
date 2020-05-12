from PIL import Image as PILImage, ImageGrab 
import numpy as np
import cv2, time, math
import threading
from flask import Flask, render_template, Response, jsonify

# for Fusion 3.64 and resolution 1366*768 - rect whit game (165, 30, 1201, 738)

class ScreenReaderClass():
    def __init__(self, ScreenShotingArea=(0, 0, 1366, 768), RoadK = 0.7):
        self.ScreenShotingArea = ScreenShotingArea
        self.АctualScreenShot = self.SreenShot(ScreenShotingArea)
        self.SaveTestScreenShot(ScreenShotingArea)

        self.GRAY_MASK = ((0, 0, 15), (255, 255, 150))
        self.RED_MASK = ((170, 50, 50), (180, 255, 255))
        self.RED_MASK_CAR = ((0, 50, 20), (5, 255, 255))
        self.TopLineRoad = int((self.ScreenShotingArea[3]-self.ScreenShotingArea[1])*RoadK)

        self.Statistics = []

    def SetStatistics(self, Input):
        self.Statistics = [Input]

    def SreenShot(self, ScreenShotRegion=None):
        return cv2.cvtColor(np.array(ImageGrab.grab(bbox=ScreenShotRegion)), cv2.COLOR_RGB2BGR)
    
    def SaveImage(self, Image, Name="SaveImage.png"):
        cv2.imwrite(Name, Image)

    def SaveTestScreenShot(self, ScreenShotRegion=None):
        self.SaveImage(self.SreenShot(ScreenShotRegion), 'TestScreenShot.png')

    def GetMask(self, Image=None, Mask=((0, 0, 0), (255, 255, 255))):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        
        HSVImage = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
        return  cv2.inRange(HSVImage, Mask[0], Mask[1])

    def GetRoadMoment(self, NumberMoments=3, Image=None, Mask=-1, Save=False):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        Mask = (lambda x: self.GRAY_MASK if(x==-1) else x)(Mask)

        ReturnValues = []
        Step = int(((self.ScreenShotingArea[3]-self.ScreenShotingArea[1])-self.TopLineRoad)/(NumberMoments))
        
        if(Save): 
            ImageWithDrawImage = cv2.cvtColor(self.GetMask(Image, Mask), cv2.COLOR_GRAY2BGR)
            cv2.line(ImageWithDrawImage, (0, self.TopLineRoad), 
                                        (self.ScreenShotingArea[2]-self.ScreenShotingArea[0], self.TopLineRoad), (0, 255, 0), 2)

        for i in range(NumberMoments):
            GrayRoad = self.GetMask(Image, Mask)[self.TopLineRoad+Step*i:self.TopLineRoad+Step*(i+1), :]
            
            if(Save): cv2.line(ImageWithDrawImage, (0, self.TopLineRoad+Step*(i+1)), 
                                        (self.ScreenShotingArea[2]-self.ScreenShotingArea[0], self.TopLineRoad+Step*(i+1)), (0, 255, 0), 2)

            moments = cv2.moments(GrayRoad, 1)
            dM10 = moments['m10']
            dArea = moments['m00']
            x = -1
            if(dArea != 0): x = int(dM10 / dArea)
            if(x!= -1): 
                ReturnValues.append(x/(self.ScreenShotingArea[2]-self.ScreenShotingArea[0]))
            else: ReturnValues.append(-1)

        if(Save): 
            self.SaveImage(ImageWithDrawImage, "GrayRoad.png")

        return ReturnValues
    
    def GetSpeed(self, Image=None, Save=False):
        if(Image is None): Image = self.SreenShot(self.ScreenShotingArea)
        Speedometer = Image[110:130, 400:500]
        SpeedometerWithMask = self.GetMask(Speedometer, self.RED_MASK)

        if(Save): self.SaveImage(SpeedometerWithMask, "SpeedometerWithMask.png")
        if(Save): self.SaveImage(Speedometer, "Speedometer.png")

        moments = cv2.moments(SpeedometerWithMask, 1)
        dM10 = moments['m10']
        dArea = moments['m00']
        x = -1
        if(dArea != 0): x = int(dM10 / dArea)
        if(x != -1): 
            return x/100*200
        else: return -1

    def demon(self):
        app = Flask(__name__)

        def image2jpeg(image):
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

        @app.route('/')
        def index():
            return render_template('index.html')

        def Gen():
            while True:
                image = self.SreenShot(self.ScreenShotingArea)
                x = self.GetRoadMoment(10)
                Step = int(((self.ScreenShotingArea[3]-self.ScreenShotingArea[1])-self.TopLineRoad)/(10))
                for i in range(len(x)):
                    cv2.circle(image, (int(x[i]*(self.ScreenShotingArea[2]-self.ScreenShotingArea[0])), int(Step*(i+1)+self.TopLineRoad)-3), 2, (0, 255, 0), thickness=3, lineType=8, shift=0)

                x = self.GetRoadMoment(10, Mask=self.RED_MASK_CAR)
                Step = int(((self.ScreenShotingArea[3]-self.ScreenShotingArea[1])-self.TopLineRoad)/(10))
                for i in range(len(x)):
                    cv2.circle(image, (int(x[i]*(self.ScreenShotingArea[2]-self.ScreenShotingArea[0])), int(Step*(i+1)+self.TopLineRoad)-3), 2, (0, 0, 255), thickness=3, lineType=8, shift=0)

                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + image2jpeg(image) + b'\r\n\r\n')

        @app.route("/GetStatistics", methods=["POST"])        
        def GetStatistics():
            return jsonify({"Data": (''.join([str(i) for i in self.Statistics])).replace("\n", "<br />")})

        @app.route('/video')
        def video():
            return Response(Gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

        app.run(host='0.0.0.0', debug=False, threaded=True)

    def StartDemon(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()
