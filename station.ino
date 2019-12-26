#include "DHT.h"
#include <Wire.h>
#include <SoftwareSerial.h>
#include <LowPower.h>

#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial HC12(10, 11);

// a variable with count the iterations our loop()
// we want the first 15 counts to delay each measurement for 20 seconds and after the first 15 counts
// we take the measurements each 15 minutes.
// It is mainly for debugging. We test if measurements are stored in Google Sheets.
int numCycles = 0;

//declare a struct for the data
struct DHTsensor {
  float humidity;
  float temperature;
  float moisture;
} myDht;


// declare time variables which are used for the measurements
unsigned long seconds = 1000L; 
unsigned long minutes = seconds * 60;

void setup() {
  // initialization 
  HC12.begin(9600);
  Serial.begin(9600);
  dht.begin();

}

void loop() {
  // we use a library for power saving. It is not so efficient as a bare atmega MCU
  LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  
  delay(250);
  dhtsensor(&myDht);
  capacitiveMoistureSensor(&myDht);
  
  char res1[8];

  // Transmit data for Air Humidity
  dtostrf(myDht.humidity, 4,  2, res1);
  HC12.write(res1);
  HC12.write("#");

  char res2[8];
  dtostrf(myDht.temperature, 4,  2, res2);
  HC12.write(res2);
  HC12.write("#");

  char res3[8];
  dtostrf(myDht.moisture, 4,  2, res3);
  HC12.write(res5);
  HC12.write("#");

//  Logging Info in Serial Monitor of Arduino IDE
//  Serial.print("Humidity: ");
//  Serial.print(myDht.humidity);
//  Serial.print(" %\n");
//  Serial.print("Temperature: ");
//  Serial.print(myDht.temperature);
//  Serial.println(" *C ");
//  Serial.print("Moisture: ");
//  Serial.println(myDht.moisture);
//  Serial.println();

  if (numCycles < 15){
    delay(20000);
  }else {
    delay(15 * minutes);
  }
}

void capacitiveMoistureSensor(struct DHTsensor *ms) {
  // we calibrated the soil moisture sensor, simply getting the values when it is on air and inside a water
  // the main thinking is that a wet soil has a value between this two extreme values
  const double AirValue = 897;   
  const int WaterValue = 416;     
  double soilMoistureValue = 0;

  soilMoistureValue = analogRead(A0);  //put Sensor insert into soil
  
  double relative_val;
  relative_val = (1 - (soilMoistureValue - WaterValue)/(AirValue - WaterValue)) * 100;
  (*ms).moisture = relative_val;

}

void dhtsensor(struct DHTsensor *ms) {
