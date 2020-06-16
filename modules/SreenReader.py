from PIL import Image as PILImage, ImageGrab 
import numpy as np
import cv2, time, math
import threading
from flask import Flask, render_template, Response, jsonify

# for Fusion 3.64 and resolution 1366*768 - rect whit game (165, 30, 1201, 738)

class ScreenReaderClass():
    def __init__(self, ScreenShotingArea=(0, 0, 1366, 768), RoadK = 0.8):
        self.ScreenShotingArea = ScreenShotingArea
        self.АctualScreenShot = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
        self.SaveTestScreenShot(ScreenShotingArea)

        self.GRAY_MASK = ((0, 0, 15), (255, 255, 150))
        self.RED_MASK = ((170, 50, 50), (180, 255, 255))
        self.RED_MASK_CAR = ((0, 50, 20), (5, 255, 255))
        self.TopLineRoad = int((self.ScreenShotingArea[3]-self.ScreenShotingArea[1])*RoadK)
        self.ScreenShotingAreaRoad = (ScreenShotingArea[0], self.TopLineRoad, ScreenShotingArea[2], ScreenShotingArea[3])

        self.Statistics = []
        self.StartScreenShotingDemon()
    def SetStatistics(self, Input):
        self.Statistics = [Input]

    def ScreenShotingDemon(self):
        counter = 0
        StartTime = time.time()
        while True:
            self.АctualScreenShot = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
            if(time.time()-StartTime >= 10):
                print("FPS ScreenShot - {}".format(counter/(time.time()-StartTime)))
                StartTime = time.time()
                counter = 0
            counter+=1
            time.sleep(0.005)
    def StartScreenShotingDemon(self):
        demon = threading.Thread(target=self.ScreenShotingDemon)
        demon.daemon = True
        demon.start()

    def SreenShot(self, ScreenShotRegion=None, Save=False):
        if(ScreenShotRegion != None): image = np.array(self.АctualScreenShot)[ScreenShotRegion[1]:ScreenShotRegion[3], ScreenShotRegion[0]:ScreenShotRegion[2]]
        else: image = np.array(self.АctualScreenShot)
        if(Save): self.SaveImage(image, "MiniScreen.png")
        return image
    
    def SreenShotMini(self, ScreenShotRegion=None, Size=(64, 16), Save=False):
        if(ScreenShotRegion != None):
            image = cv2.resize(np.array(self.АctualScreenShot)[ScreenShotRegion[1]:ScreenShotRegion[3], ScreenShotRegion[0]:ScreenShotRegion[2]],
                                (int(Size[0]),int(Size[1])))
        else: image = cv2.resize(np.array(self.АctualScreenShot), (int(Size[0]),int(Size[1])))
        if(Save): self.SaveImage(image, "MiniScreen.png")
        return image

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
        ReturnValues2 = []
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
                ReturnValues2.append(np.sum(GrayRoad)/1000000)
            else: 
                ReturnValues.append(-1)
                ReturnValues2.append(-1)

        if(Save): 
            self.SaveImage(ImageWithDrawImage, "GrayRoad.png")

        return ReturnValues, ReturnValues2
    
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
                x, _ = self.GetRoadMoment(10)
                Step = int(((self.ScreenShotingArea[3]-self.ScreenShotingArea[1])-self.TopLineRoad)/(10))
                for i in range(len(x)):
                    cv2.circle(image, (int(x[i]*(self.ScreenShotingArea[2]-self.ScreenShotingArea[0])), int(Step*(i+1)+self.TopLineRoad)-3), 2, (0, 255, 0), thickness=3, lineType=8, shift=0)

                x, _ = self.GetRoadMoment(10, Mask=self.RED_MASK_CAR)
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
