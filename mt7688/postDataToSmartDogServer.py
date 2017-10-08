import serial
import time
import requests
import os
import fsParameter
 
s = None


def parserSensorValue(rawString):
    print "raw string: " + rawString
    keys = ["at","ah","ap","li","st","sh","c","s","g","t","r","p","h","b","eol"]

    at = 0.0
    ah = 0.0
    ap = 0.0
    li = 0.0
    st = 0.0
    sh = 0.0
    
    windDir = 0
    windSpeed = 0.0
    rain = 0.0

    
 
    string = rawString.partition(keys[0])[2]
    for index in range(1,len(keys)):
        key = keys[index] 
        partitionResult = string.partition(key)
       
        value = partitionResult[0]
	if value == "":
	    value = 0
        if index == 1:
            at = float(value)
       
	if index == 2:
	    ah = float(value)

	if index == 3:
	    ap = float(value)

	if index == 4:
	    li = float(value)

	if index == 5:
	    st = float(value)

	if index == 6:
	    sh = float(value)
	
	if index == 7:
	    windDir = int(value)

	if index == 8:
	    windSpeed = float(value)

	if index == 11:
	    rain = float(value)	

        string = partitionResult[2]

    print "result at: " + str(at) + ", ah: " + str(ah) + " ,ap: " + str(ap) + " ,li: " + str(li) + " ,st: " + str(st) + " ,sh: " + str(sh) + " ,wd: " + str(windDir) + " ,ws: " + str(windSpeed) + " ,rain: " + str(rain)

    payload = {'col0':'FieldSensorV2.1-001','col1':at,'col2':ah,'col3':ap,'col4':li,'col5':st,'col6':sh,'col7':windDir,'col8':windSpeed,'col9':rain}
    return payload



def capAndSaveImage(info):
    ts = str(int(time.time()))
    fileName = ts + '-' + info.rstrip() + ".jpg"
    filePath = '/Media/SD-P1/' + fileName
    print("fileName: " + fileName)
    cmd = 'fswebcam -r 1280x960 -i 0 -d v4l2:/dev/video0 --no-banner -p YUYV --jpeg 95 --save %s'%(filePath)
    os.system(cmd)
    
    time.sleep(3)
    return filePath

def setup():
    global s
    s = serial.Serial("/dev/ttyS0", 57600)

def postData2Server(imgPath, sensorData):

    jpgb64 = open(imgPath,'rb').read().encode('base64').replace('\n','')
    sensorData['col10'] = jpgb64
    finalURL="{0}/".format(fsParameter.hostURL)
    
    r = requests.post(finalURL, data=sensorData)
    #print(r.text) #TEXT/HTML
    print(r.status_code, r.reason) #HTTPfinalURL="{0}/".format(hostURL)
 
def loop():
    info = s.readline()

    try:
	imgFilePath = capAndSaveImage(info)
        sensorData = parserSensorValue(info)
        postData2Server(imgFilePath,sensorData)
    except Exception as e: 
	print  e


if __name__ == '__main__':
    setup()
    while True:
        loop()


