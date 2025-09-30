🌾 CropGenie: AI Backend Servers

This repository contains the backend servers for the CropGenie project.
It provides two real-time machine learning services powered by Flask and WebSockets, delivering instant agricultural insights for farmers.

🏗️ Architecture Overview

The backend consists of two independent microservices:

🌱 Plant Health Server (app.py)

WebSocket server

Receives live sensor data: soil moisture, temperature, humidity

Uses a Random Forest model to predict plant health

Broadcasts analysis & improvement suggestions to all connected clients

🦠 Disease Detection Server (realtime_server.py)

Socket.IO server

Receives video frames or images from frontend/phone

Runs a custom YOLOv8 model (best.pt) to detect diseases in real time

Sends back detection coordinates + labels

✨ Features

⚡ Real-Time Analysis → Low-latency communication with WebSockets (flask-sock & flask-socketio)

🌱 Predictive Health Monitoring → Random Forest model provides actionable crop recommendations

🔍 Live Object Detection → YOLOv8 identifies crop diseases with bounding boxes from live feed

📡 Broadcasting → Plant Health Server streams results to multiple dashboards or apps simultaneously

⚙️ Setup & Installation

Follow these steps to get the servers running locally.

1. Prerequisites

Python 3.8+

pip (Python package manager)

2. Clone the Repository
git clone <your-repository-url>
cd <your-repository-name>

3. Create a Virtual Environment
# Create venv
python -m venv venv  

# Activate venv
# On Windows:
venv\Scripts\activate  
# On macOS/Linux:
source venv/bin/activate  

4. Install Dependencies

Create a requirements.txt file with:

# Common
Flask
gunicorn

# For app.py
flask-sock
pandas
scikit-learn
joblib

# For realtime_server.py
flask-socketio
ultralytics
Pillow
python-engineio==4.8.0
python-socketio==5.10.0
numpy


Then install all packages:

pip install -r requirements.txt

5. Pre-trained Models

Place the following in the root directory:

best.pt → YOLOv8 model (for disease detection)

plant_health_model.pkl, label_encoder.pkl, healthy_averages.pkl → Random Forest model files

👉 If missing, app.py will auto-train a new model using plant_health_data.csv during first run.

🚀 Running the Servers

Run each service in a separate terminal:

🌱 Start Plant Health Server (app.py)

Port: 5000

python app.py


Serves WebSocket endpoint at: ws://localhost:5000/ws

🦠 Start Disease Detection Server (realtime_server.py)

Port: 8080

python realtime_server.py


Serves detection endpoint at: http://localhost:8080

✅ Your Backend is Ready!

Frontend / AR app can connect to:

🌱 Plant Health → ws://localhost:5000/ws

🦠 Disease Detection → http://localhost:8080

Your backend is now fully operational, streaming real-time insights to farmers 🌾.

✨ CropGenie: Turning Crops into Data, and Data into Growth. 🌱