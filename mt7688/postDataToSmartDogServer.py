import serial
import time
import requests
import os
import re

class Smart7688ToDog: 
    def __init__(self):
        #self.s = None
        self.s = serial.Serial("/dev/ttyS0", 57600)


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
        '''
        keys = ["at","ah","ap","li","st","sh","c","s","g","t","r","p","h","b","eol"]
        #keys = ["st","sh","sp","li","st","sh","c","s","g","t","r","p","h","b","eol"]

        at = 30.0
        ah = 78.0
        ap = 1000.0
        li = 333.0
        st = 28.0
        sh = 87.0
        
        windDir = 0
        windSpeed = 0.0
        rain = 0.0
        
        infoDict = {} 
        string = rawString.partition(keys[0])[2]
        for index in range(1,len(keys)):
            key = keys[index] 
            partitionResult = string.partition(key)
           
            value = partitionResult[0]
            if value == "":
                value = 0

            if index == 1:
                at = float(value)
                infoDict[keys[0]] = at

            if index == 2:
                ah = float(value)
                infoDict[keys[1]] = ah
         
            if index == 3:
                ap = float(value)
                infoDict[keys[2]] = ap

            if index == 4:
                li = float(value)
                infoDict[keys[3]] = li

            if index == 5:
                st = float(value)
                infoDict[keys[4]] = st

            if index == 6:
                sh = float(value)
                infoDict[keys[5]] = sh	

            if index == 7:

                windDir = int(value)
                infoDict[keys[6]] = windDir

            if index == 8:
                windSpeed = float(value)
                infoDict[keys[7]] = windSpeed
                
            if index == 11:
                rain = float(value)	
                infoDict[keys[10]] = rain

            string = partitionResult[2]
            print string
        payload = {'col0':'FieldSensorV2.1-001','col1':at,'col2':ah,'col3':ap,'col4':li,'col5':st,'col6':sh,'col7':windDir,'col8':windSpeed,'col9':rain}
        '''
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


