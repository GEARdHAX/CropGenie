🌾 CropGenie Dashboard – Frontend

This is the official frontend dashboard for the CropGenie Smart Farming System.
It’s a real-time, interactive web app built with React, designed to give farmers instant insights into their crops, run live disease detection, and provide useful agricultural tools.

✨ Features

The dashboard has three main functional modules:

1️⃣ Live Plant Health Status

📡 Real-time Sensor Feed → Connects via WebSocket to live data from hardware.

📊 Key Metrics → Displays Soil Moisture, Temperature, Humidity.

🤖 AI Health Assessment → Shows health status (e.g., Healthy, High Stress) via Random Forest model.

📝 Actionable Suggestions → Provides instant recommendations for improving crop conditions.

2️⃣ Real-time Disease Detection

🎥 Live Camera Integration → Accesses device camera for video stream.

🔍 AI Object Detection → Sends frames via Socket.IO to YOLOv8 backend for analysis.

🖼️ Visual Feedback → Overlays bounding boxes + labels + confidence on crops.

✅ Connection Status → Clearly shows server connectivity.

3️⃣ Growing Degree Day (GDD) Calculator

🌡️ Utility Tool → Calculates GDD for predicting crop & pest growth stages.

🧮 Simple Form → Enter Max, Min, Base temperature → Get instant GDD value.

🛠️ Tech Stack

Core Framework → React

Real-Time Communication →

Socket.IO Client
 for YOLOv8 detection

Native WebSocket API
 for plant health sensor data

Styling → Custom CSS with Variables (responsive & modern design)

Icons → React Icons
 (Weather set used)

Browser APIs → navigator.mediaDevices.getUserMedia for camera access

🧱 Component Breakdown

App.jsx → Root layout + tab navigation

PlantHealth.jsx → WebSocket connection, sensor data visualization, AI health status & suggestions

DiseaseDetection.jsx → Camera access, Socket.IO video streaming, YOLOv8 detection overlay

GddCalculator.jsx → Standalone GDD form & calculation logic

App.css / index.css → Global styles, theming, responsive layout

🚀 Getting Started
1. Prerequisites

Node.js
 (v18+ recommended)

npm or yarn

2. Installation
# Clone repository
git clone <your-repository-url>
cd <repository-folder>

# Install dependencies
npm install

3. Configure Environment Variables

Create a .env file in the root folder:

VITE_PLANT_HEALTH_WS_URL=ws://<YOUR_COMPUTER_IP>:5000/ws
VITE_DISEASE_DETECTION_URL=http://<YOUR_COMPUTER_IP>:8080


Update components to use environment variables:

// PlantHealth.jsx
const WS_URL = import.meta.env.VITE_PLANT_HEALTH_WS_URL;

// DiseaseDetection.jsx
const serverUrl = import.meta.env.VITE_DISEASE_DETECTION_URL;

4. Run Development Server

Make sure backend servers (app.py, realtime_server.py) are running first, then:

npm run dev


Frontend runs at → http://localhost:5173

✅ Summary

🌱 Live health monitoring with AI suggestions

🦠 Real-time YOLOv8 disease detection with camera feed

🌡️ GDD calculator for predictive insights

⚡ Built with React + WebSockets + Socket.IO

✨ “CropGenie Dashboard: Making smart farming intuitive & visual for every farmer.” 🌾