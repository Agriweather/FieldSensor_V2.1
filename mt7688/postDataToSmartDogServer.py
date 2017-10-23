import serial
import time
import requests
import os
import re

class Smart7688ToDog: 
    def __init__(self):
        #self.s = None
        self.s = serial.Serial("/dev/ttyS0", 57600)

    def capDisplayImg(self):
        filePath = '/Media/SD-P1/FieldSensor_V2.1/mt7688/src/images/image.jpg'                                                                              
        cmd = 'fswebcam -r 1280x960 -i 0 -d v4l2:/dev/video0 --no-banner -p YUYV --jpeg 95 --save %s'%(filePath)                  
        os.system(cmd)
    def parserSensorValue(self, rawString= 'NaN'):
        if rawString is 'NaN':
            self.s.write('1')
            rawString= self.s.readline()
        #raw string: li234st24.5sh76c000s000g000t086r000p000h53b10020

        print "raw string: " + rawString
        infoDict= {}
        parser= re.compile("([a-z]+)([\.\d]+)")
        parserList= parser.findall(rawString)
        print parserList
        for i in range(0,len(parserList)):
            infoDict[parserList[i][0]] = float(parserList[i][1])
        
        temp = infoDict['t']
        infoDict['t'] = (temp - 32) * 5/9

        print infoDict
    #    print "result at: " + str(at) + ", ah: " + str(ah) + " ,ap: " + str(ap) + " ,li: " + str(li) + " ,st: " + str(st) + " ,sh: " + str(sh) + " ,wd: " + str(windDir) + " ,ws: " + str(windSpeed) + " ,rain: " + str(rain)



        return infoDict



    def capAndSaveImage(self, info= 'NaN'):
        if info is 'NaN':
            self.s.write('1')
            info= self.s.readline()
        ts = str(int(time.time()))
        fileName = ts + '-' + info.rstrip() + ".jpg"
        filePath = '/Media/SD-P1/images/' + fileName
        print("fileName: " + fileName)
        cmd = 'fswebcam -r 1280x960 -i 0 -d v4l2:/dev/video0 --no-banner -p YUYV --jpeg 95 --save %s'%(filePath)
        os.system(cmd)
        
        time.sleep(3)
        return filePath
        '''
        def setup():
            global s
            s = serial.Serial("/dev/ttyS0", 57600)
        '''
    def postData2Server(self, imgPath, sensorData):

        jpgb64 = open(imgPath,'rb').read().encode('base64').replace('\n','')
        sensorData['col10'] = jpgb64
        finalURL="{0}/".format('www.agri.com')
        
        r = requests.post(finalURL, data=sensorData)
        #print(r.text) #TEXT/HTML
        print(r.status_code, r.reason) #HTTPfinalURL="{0}/".format(hostURL)
     
    def loop(self ):
        self.s.write('1')
        info = self.s.readline()
        
        try:
            imgFilePath = capAndSaveImage(info)
            sensorData = parserSensorValue(info)
    #        print sensorData 
    #        postData2Server(imgFilePath,sensorData)
        except Exception as e: 
            print  e
s= None
def setup():
    global s
    s = serial.Serial("/dev/ttyS0", 57600)

if __name__ == '__main__':
    setup()
    while True:
        loop()


