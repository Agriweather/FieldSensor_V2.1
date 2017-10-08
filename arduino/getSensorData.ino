/***************************************************************************
  Field Sensor for Taiwan Farmers by Kobe Yu.

  data format:
  
 ***************************************************************************/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include "SparkFunHTU21D.h"
#include <SoftwareSerial.h>

#define SEALEVELPRESSURE_HPA (1013.25)

//不是所有的腳位都可以當作softwareSerial
//要有支援中斷(EINT)的才可以！！
SoftwareSerial swSerial(14,15);  //建立軟體串列埠腳位 (RX, TX)
HTU21D soilTHSensor;
Adafruit_BME280 bme; // I2C

int BH1750_address = 0x23; // i2c Addresse

byte bh1750Buff[2];

unsigned long delayTime;
float air_temp;
float pres;
float air_humi;
float soil_temp;
float soil_humi;
float light_intensity;
String aprs_string;
void setup() {

    Serial1.println("-- Setup start --");
    
    //setup serail port
    Serial1.begin(57600);
    Serial1.println(F("BME280 test")); 

    //init i2c 
    Wire.begin();

    bool status;
    // default settings
    status = bme.begin();
    if (!status) {
        Serial1.println("Could not find a valid BME280 sensor, check wiring!");
        while (1);
    }

    BH1750_Init(BH1750_address);
    soilTHSensor.begin();
    
    delayTime = 3000;
    
//    swSerial.begin(9600);

    air_temp = 0.0;
    pres = 0.0;
    air_humi = 0.0;
    Serial1.println("-- Setup end --");
    Serial1.println();
}


void loop() { 
    //Serial1.println("-- Loop start --");
    getBME280Value();
    getBH1750Value();
    getSHT20Value();
    getAPRSValue();
    
    printAllData();
    
    delay(delayTime);
    
}


void printAllData() {
  
  printBME280Value(air_temp,pres,air_humi);

  //print BH1750
  Serial1.print("li");Serial1.print(light_intensity);
  Serial1.print("st");Serial1.print(soil_temp);
  Serial1.print("sh");Serial1.print(soil_humi);
  Serial1.print(aprs_string);

  Serial1.println();
}

void getAPRSValue() {

  //to prevent serial rec buffer overflow
  //other ways //ref https://www.baldengineer.com/when-do-you-use-the-arduinos-to-use-serial-flush.html
  
  swSerial.begin(9600);
  while(Serial.available());

  //waiting buffer fillup
  delay(1000);
  aprs_string = swSerial.readStringUntil('\n');
  swSerial.end();
 
}



void getSHT20Value() {
  
  soil_humi = soilTHSensor.readHumidity();
  soil_temp = soilTHSensor.readTemperature();
}
  
void getBME280Value() {
  air_temp =  bme.readTemperature();
  pres = bme.readPressure() / 100.0F;
  air_humi = bme.readHumidity();
}

void printBME280Value(float air_temp, float pres, float air_humi) {
  Serial1.print("at");Serial1.print(air_temp);
  Serial1.print("ah");Serial1.print(air_humi);
  Serial1.print("ap");Serial1.print(pres);
  
}


void getBH1750Value() {
  float valf=0;

  if(BH1750_Read(BH1750_address)==2) {
    valf=((bh1750Buff[0]<<8)|bh1750Buff[1])/1.2;
    if(valf<0) {
      light_intensity = 0;
    } else {
      light_intensity =  valf;
    }
  }  
}




void BH1750_Init(int address) {
  Wire.beginTransmission(address);
  Wire.write(0x10); // 1 [lux] aufloesung
  Wire.endTransmission();
}

 
byte BH1750_Read(int address) {
   byte i=0;
  Wire.beginTransmission(address);
  Wire.requestFrom(address, 2);
  while(Wire.available()) {
    bh1750Buff[i] = Wire.read(); 
    i++;
  }
  Wire.endTransmission();  
  return i;
}
 
