🌾 CropGenie: AI-Powered Smart Farming with IoT & AR

🚀 CropGenie is an AI-powered smart farming system that brings precision agriculture to small-scale farmers.
By combining IoT sensors, Machine Learning, and Augmented Reality, it enables:

✅ Real-time crop monitoring
✅ Early pest & disease detection
✅ Actionable, data-driven farming insights
✅ Affordable and scalable adoption

🏆 Built at UDAYA 1.0 Hackathon by Team AXIS from Dayananda Sagar College of Engineering

🌍 The Problem We Solve

🌊 Inefficient water & nutrient use → Higher costs, lower sustainability

🐛 Late pest/disease detection → Major yield loss

📊 Complex raw data → Farmers lack simple actionable insights

💰 Expensive tools → Precision farming usually out of reach for small farms

🌱 Our Solution

CropGenie = Affordable + Scalable + Intuitive Farming Assistant

🔹 Real-time IoT-based data collection
🔹 AI-powered predictions & crop diagnostics
🔹 Farmer-friendly AR visualization

✨ Key Features

🔍 Disease & Pest Detection → realtime_server.py runs a YOLOv8 model via laptop or phone browser for instant leaf disease detection.

🌡 Environmental Monitoring → app.py (Flask backend) uses a Random Forest Classifier on real-time sensor data for crop health assessment & smart suggestions.

🔄 Real-time Communication → Powered by WebSockets, ensuring continuous sync between IoT hardware, backend, and AR app.

🕶 AR Overlay → Mobile app overlays health data, risks, and growth predictions directly onto live crops.

🏗 System Architecture
🖥 Edge Node (Hardware)

Controller → Arduino

Sensors → BME280, Soil Moisture, Ultrasonic

Connectivity → ESP8266 WiFi + HTTP POST

⚙️ Core Brain (Backend)

realtime_server.py → YOLOv8 detection server for crop disease (browser-based)

app.py → Flask backend + Random Forest Classifier for environmental analysis & farming suggestions

WebSockets → Real-time communication between IoT, backend, and app

📱 User Interface (Mobile App)

Unity + ARCore + Vuforia

Dashboard with crop metrics, alerts, and insights

Farmers can capture images → YOLOv8 returns disease diagnosis in real-time

🛠 Tech Stack
Category	Technologies
🤖 ML/AI	YOLOv8, RandomForestClassifier, PyTorch, XGBoost, TensorFlow, Keras
⚙️ Backend	Python, Flask, WebSockets, Node.js, Express.js
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

Clone repo

git clone https://github.com/GEARdHAX/CropGenie.git


Start Flask Backend (app.py)

cd CropGenie/backend
pip install -r requirements.txt
python app.py


Start Disease Detection Server (realtime_server.py)

python realtime_server.py


👉 Visit the local server in your browser to upload/capture crop images.

Setup Hardware

Open /hardware .ino in Arduino IDE

Install ESP8266WiFi, BME280, etc.

Flash to Arduino/ESP8266

Build Mobile AR App

Open /mobile-app in Unity

Update Flask/WebSocket endpoints

Build APK for Android

🌟 Why CropGenie?

📡 Real-time, WebSocket-driven communication

🧑‍🌾 Farmer-first design → AR insights instead of raw data

💰 Affordable IoT sensors & open-source stack

🔮 Predictive + Diagnostic AI models

📜 License

This project is licensed under the MIT License
.

✨ “Turning crops into data, and data into growth.” 🌾
