# CropGenie: AI-Powered Smart Farming with IoT

[](https://opensource.org/licenses/MIT)

CropGenie is an AI-powered smart farming system designed to make precision agriculture accessible and affordable for small-scale farmers. By integrating IoT sensors, advanced Machine Learning models, and Augmented Reality, CropGenie provides real-time crop monitoring, early disease detection, and actionable insights to increase yield and promote sustainable practices.

[cite\_start]This project was developed for the **UDAYA 1.0 Hackathon** by **Team AXIS** from Dayananda Sagar College of Engineering[cite: 3, 43, 46].

-----

## Core Problem

Modern agriculture faces significant challenges that CropGenie aims to address:

  * [cite\_start]**Inefficient Resource Management:** Wasted water and nutrients increase costs and harm the environment[cite: 55].
  * [cite\_start]**Late Detection of Threats:** Pests and diseases often go unnoticed until significant crop loss is unavoidable[cite: 57].
  * [cite\_start]**Data-to-Action Gap:** Farmers often struggle to convert complex sensor and weather data into simple, actionable steps[cite: 56].
  * [cite\_start]**High Cost of Technology:** Precision farming tools are frequently too expensive for small-scale farmers[cite: 58].

## Our Solution

**CropGenie** is a cost-effective, scalable, and user-friendly system that combines hardware and software to solve these problems. [cite\_start]It uses affordable IoT sensors to collect real-time environmental data, processes it with powerful AI models in the cloud, and visualizes the results intuitively through an Augmented Reality mobile application[cite: 66, 67].

### Key Features 🧑‍🌾

  * **Precision Pest & Disease Diagnostics:** Utilizes a **YOLOv8 model** trained on a custom dataset of over **3000 images** to instantly identify plant diseases and pests from a smartphone camera.
  * [cite\_start]**GDD-Optimized Growth Forecasting:** Leverages Growing Degree Days (GDD) along with sensor data to accurately predict plant growth stages, helping optimize planning and harvesting[cite: 88].
  * [cite\_start]**Real-time Environmental Monitoring:** Continuously assesses soil moisture, temperature, and other environmental factors to recommend ideal growing conditions[cite: 90].
  * [cite\_start]**Augmented Reality Visualization:** Overlays AI-driven insights—like pest risks, water levels, and nutrient status—directly onto the physical crops, turning complex data into intuitive visuals[cite: 80, 91].

-----

## System Architecture

The CropGenie ecosystem is composed of three main parts: the Edge Node (hardware), the Core Brain (backend server), and the User Interface (AR mobile app).

### 1\. Edge Node (Hardware)

The hardware unit is placed in the field to collect crucial environmental data.

  * [cite\_start]**Controller:** An **Arduino** board serves as the main controller for the sensors[cite: 129].
  * [cite\_start]**Sensors:** A suite of minimal, cost-effective sensors like **BME280 (temperature, humidity, pressure), Ultrasonic sensors (plant height), and Soil Moisture sensors** gather data directly from the environment[cite: 154].
  * [cite\_start]**Communication:** An **ESP8266 Wi-Fi Module** transmits the collected sensor data to our backend server via HTTP POST requests[cite: 133, 134].

### 2\. Core Brain (Backend Server)

[cite\_start]A **Flask API server** acts as the central hub for all data processing and machine learning inference[cite: 135].

  * **Real-time Disease Detection:** Receives images from the mobile app and processes them using a custom-trained **YOLOv8 model** (`best.pt`). [cite\_start]This convolutional neural network (CNN) can identify a wide range of plant diseases in real-time and send the diagnosis back to the user[cite: 131, 143].
  * [cite\_start]**Environmental Analysis:** An **XGBoost** model analyzes incoming sensor data to assess crop health and calculate Growing Degree Days (GDD)[cite: 138, 147].
  * [cite\_start]**Growth Prediction:** A **PyTorch**-based model forecasts future plant growth based on environmental data and GDD calculations[cite: 146].

### 3\. User Interface (AR Mobile App)

The mobile app is the primary interface for the farmer.

  * [cite\_start]**Data Visualization:** Displays sensor metrics, soil analysis, and model predictions on a user-friendly dashboard[cite: 141].
  * [cite\_start]**AR Overlay:** Built with **Unity** and **ARCore/Vuforia**, the app allows users to point their camera at crops and see AR visualizations of their health status, water needs, and any detected diseases[cite: 167, 169, 170].
  * **Interaction:** Farmers can capture and upload images of potentially diseased plants for instant AI analysis.

-----

## Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Machine Learning** | `TensorFlow`, `Keras`, `PyTorch`, `YOLOv8`, `XGBoost` |
| **Backend** | [cite\_start]`Python`, `Flask`, `Node.js`, `Express.js` [cite: 167, 186] |
| **Frontend & Mobile** | [cite\_start]`Unity`, `ARCore`, `Vuforia`, `Tailwind CSS` [cite: 167, 169, 170, 197] |
| **Databases** | [cite\_start]`MongoDB`, `MySQL` [cite: 163, 164] |
| **Hardware** | [cite\_start]`Arduino`, `ESP8266`, `C++` [cite: 129, 133, 161] |
| **DevOps & Tools** | [cite\_start]`Git`, `GitHub`, `OpenWeather API` [cite: 168, 196] |

-----

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

  * Python 3.8+
  * Arduino IDE
  * Unity Hub
  * Node.js

### Installation

1.  **Clone the repo**

    ```sh
    git clone https://github.com/GEARdHAX/CropGenie.git
    ```

2.  **Setup Backend**

    ```sh
    cd CropGenie/backend
    pip install -r requirements.txt
    flask run
    ```

3.  **Setup Hardware**

      * Open the `.ino` file in the `/hardware` directory with Arduino IDE.
      * Install the required libraries (ESP8266WiFi, BME280, etc.).
      * Flash the code to your Arduino/ESP8266 board.

4.  **Build the Mobile App**

      * Open the `/mobile-app` project in Unity.
      * Connect it to the running Flask server by updating the API endpoint.
      * Build the APK for your Android device.

-----
