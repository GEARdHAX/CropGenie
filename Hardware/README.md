# **CropGenie - Predictive Farming System**
This directory contains all the necessary firmware for the CropGenie hardware controllers. This project gathers real-time environmental data to feed a backend prediction model, which provides insights into weather patterns and plant health.

Overview
The system is split into two main components that work together to form the complete data collection firmware:

Sensor & Control Hub (Sensors-Data.ino): An Arduino Mega 2560 acts as the primary controller. It is responsible for reading all sensors (soil moisture, temperature/humidity), and sending the compiled data to the ESP8266.

Wi-Fi & Communication Gateway (Wi-Fi.ino): An ESP8266 board serves as a dedicated Wi-Fi gateway. It listens for data from the Mega, constructs a JSON object, and forwards it to the backend prediction model over a WebSocket connection.

This decoupled architecture allows for clean separation of concerns, making the code easier to manage and debug.

## **Hardware Requirements**

Sensor & Control Hub: 
Arduino Mega 2560 ESP8266 Wi-Fi Combined board

Sensors:
BME280 (Temperature and Humidity)
Capacitive Soil Moisture Sensor

Other:

DIP Switches for deployment(on board)
Connecting Wires & Breadboard

## **System Architecture & Wiring**
The two microcontrollers chips on same board communicate with each other.

[ Arduino Mega 2560 ] <--- On Board(DIP switches) ---> [ ESP8266 ] <--- Wi-Fi ---> [ Backend Prediction Model ]
    |                                
    +---- BME280 Sensor
    |
    +---- Soil Moisture Sensor


## **Wiring Connections:**

Sensors & Relay to Arduino Mega:
Soil Moisture (Analog): A0
BME280 SDA: 20 (SDA)
BME280 SCL: 21 (SCL)


## **Code Deployment**
This section covers the complete setup process from a fresh Arduino IDE installation.

Install Arduino IDE: 
Ensure you have the latest version from the official website.

Install Board Managers:
In the IDE, go to Tools > Board > Boards Manager... and install Arduino AVR Boards.
Add the ESP8266 board URL in File > Preferences > Additional Boards Manager URLs:
[http://arduino.esp8266.com/stable/package_esp8266com_index.json]
Install esp8266 from the Boards Manager.

Install Libraries:
Go to Sketch > Include Library > Manage Libraries....

Install the following libraries:
Adafruit BME280 Library
Adafruit Unified Sensor
WebSockets by Markus Sattler
ArduinoJson

Configure Firmware:
In the Wi-Fi.ino sketch, update the following variables with your credentials:
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";
const char* websocket_host = "SERVER_IP";

In the ATMega2560_Sensor_Hub.ino sketch, calibrate your soil moisture sensor by updating SOIL_DRY_VALUE and SOIL_WET_VALUE.

## **Deployment using DIP Switches**
This hardware setup uses DIP switches to easily toggle between uploading firmware and running the integrated system.

Step 1: Upload to Arduino Mega
Set DIP switches: ON: 3, 4 | OFF: All others
Connect the Arduino Mega via USB.
Select Arduino Mega or Mega 2560 board and the correct COM Port.
Upload the Sensors-Data.ino sketch.
Disconnect the USB.

Step 2: Upload to ESP8266
Set DIP switches: ON: 5, 6, 7 | OFF: All others
Select the Generic ESP8266 Module correct COM Port.
Upload the Wi-Fi.ino sketch.
Keep the USB connected.

Step 3: Connect to Wi-Fi
Set DIP switches: ON: 5, 6 | OFF: All others (especially 7)
Press the physical RESET button on the board. The ESP will now connect to your Wi-Fi network.

Step 4: Run the Data Collection System
Set DIP switches: ON: 2, 5, 6 | OFF: All others

The Arduino Mega will now send sensor data to the ESP8266, which will forward it as JSON to your backend prediction model.

## **LICENSE**
Arduino Hardware License (for the Mega 2560 board) License: Creative Commons Attribution Share-Alike (CC BY-SA)
What it means: The design for the physical Arduino board is open source. You are free to view the schematics, create your own versions of the board, and even sell them. In return, you must give credit to Arduino and share any modified designs under this same license.

Arduino Software License (for the IDE & Core Libraries) License: GNU Lesser General Public License (LGPL)
What it means: This license is very flexible. You can write your own code (like your .ino sketches) that uses the standard Arduino functions (digitalWrite, delay, Serial.println, etc.) for any purpose, including in commercial or closed-source projects