🌾 CropGenie: AI-Powered Smart Farming with IoT & AR

🚀 CropGenie is an AI-powered smart farming system that brings precision agriculture to small-scale farmers.
By combining IoT sensors, Machine Learning, and Augmented Reality, it enables:

✅ Real-time crop monitoring
✅ Early pest & disease detection
✅ Actionable, data-driven farming insights
✅ Affordable and scalable adoption

🏆 Built at UDAYA 1.0 Hackathon by Team AXIS from Dayananda Sagar College of Engineering

🌍 The Problem We Solve

Modern farming struggles with:

🌊 Inefficient Resource Use → Water & nutrients wasted, higher costs.

🐛 Delayed Pest/Disease Detection → Major crop losses before action.

📊 Complex Data Overload → Farmers can’t easily act on raw sensor/weather data.

💰 High Cost of Precision Tools → Existing solutions too expensive for small farms.

🌱 Our Solution

CropGenie = Affordable + Scalable + Intuitive Farming Assistant

🔹 Collects real-time data via low-cost IoT sensors
🔹 Uses AI models (YOLOv8, XGBoost, PyTorch) for smart predictions
🔹 Visualizes everything through a farmer-friendly AR app

✨ Key Features

🔍 AI Disease & Pest Detection → YOLOv8 trained on 3000+ images

🌡 Real-time Environmental Monitoring → Soil moisture, temp, humidity, plant height

📈 Growth Forecasting → GDD (Growing Degree Days) + ML models

🕶 AR-based Visualization → Overlay insights directly on live crops via phone camera

🏗 System Architecture

CropGenie consists of 3 main components:

🖥 1. Edge Node (Hardware)

Controller → Arduino

Sensors → BME280, Ultrasonic, Soil Moisture

Connectivity → ESP8266 WiFi, HTTP POST

⚙️ 2. Core Brain (Backend)

API → Flask

ML Models → YOLOv8 (disease detection), XGBoost (environment), PyTorch (growth)

Data Processing → Real-time insights + forecasts

📱 3. User Interface (Mobile App)

AR Built with Unity + ARCore/Vuforia

Dashboard for metrics & alerts

Farmers can upload images for instant AI analysis

🛠 Tech Stack
Category	Technologies
🤖 ML/AI	YOLOv8, PyTorch, XGBoost, TensorFlow, Keras
⚙️ Backend	Python, Flask, Node.js, Express.js
📱 Frontend & AR	Unity, ARCore, Vuforia, Tailwind CSS
💾 Databases	MongoDB, MySQL
🔌 Hardware	Arduino, ESP8266, C++
🛠 Tools	Git, GitHub, OpenWeather API
🚀 Getting Started
🔧 Prerequisites

Python 3.8+

Arduino IDE

Unity Hub

Node.js

⚡ Installation

Clone the repository:

git clone https://github.com/GEARdHAX/CropGenie.git


Setup Backend:

cd CropGenie/backend
pip install -r requirements.txt
flask run


Setup Hardware:

Open /hardware .ino file in Arduino IDE

Install libraries: ESP8266WiFi, BME280, etc.

Flash code to Arduino/ESP8266

Build the Mobile App:

Open /mobile-app in Unity

Update API endpoint (Flask server)

Build APK & deploy to Android

🌟 Why CropGenie?

✅ Farmer-first design — Simple AR visualizations instead of confusing dashboards

✅ Affordable — Uses minimal, low-cost sensors

✅ Scalable — Works for small farms and can scale up

✅ Hackathon-proven — Designed for impact, speed, and usability

📜 License

This project is licensed under the MIT License
.

✨ “Turning crops into data, and data into growth.” 🌾
