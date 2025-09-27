#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>


#define SOIL_PIN A0
const int SOIL_DRY_VALUE = 537;
const int SOIL_WET_VALUE = 300;


Adafruit_BME280 bme;
float temperature, humidity;
int soilPercent = 0;


unsigned long lastReadTime = 0;
const long readInterval = 2000;

void setup() {
  Serial.begin(9600);


  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
}

void loop() {
  if (millis() - lastReadTime >= readInterval) {
    lastReadTime = millis();

    int soilRaw = analogRead(SOIL_PIN);
    soilPercent = map(soilRaw, SOIL_DRY_VALUE, SOIL_WET_VALUE, 0, 100);
    soilPercent = constrain(soilPercent, 0, 100);

    temperature = bme.readTemperature();
    humidity = bme.readHumidity();


    String dataString = "DATA:" + String(soilPercent) + "," +
                        String(temperature) + "," +
                        String(humidity);
    Serial.println(dataString);

    String debugString = "DEBUG >> Moisture: " + String(soilPercent) + "% | " +
                         "Temp: " + String(temperature) + "C | " +
                         "Humidity: " + String(humidity) + "%";
    Serial.println(debugString);
  }
}