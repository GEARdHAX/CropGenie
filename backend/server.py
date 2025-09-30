from flask import Flask
from flask_socketio import SocketIO  # <-- Note: 'emit' is no longer imported directly
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import pandas as pd
import joblib
import os
import json
import base64
import io

# --- 1. Initialize Flask App and SocketIO with CORS ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# --- 2. Load Both of Your AI Models ---
try:
    health_model = joblib.load("plant_health_model.pkl")
    le = joblib.load("label_encoder.pkl")
    average_healthy_values = joblib.load("healthy_averages.pkl")
    print("✅ Plant health model loaded successfully.")
except FileNotFoundError:
    print("❌ Plant health model files not found. The health page will not work.")
    health_model = None

try:
    disease_model = YOLO("best.pt")
    print("✅ Disease detection (YOLO) model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading disease detection model: {e}")
    disease_model = None


# --- 3. Plant Health Prediction Logic ---
def predict_and_recommend(sensor_data):
    if not health_model:
        return "Model Not Loaded", []

    input_df = pd.DataFrame(
        [sensor_data], columns=["Soil_Moisture", "Soil_Temperature", "Humidity"]
    )
    prediction_encoded = health_model.predict(input_df)[0]
    prediction_label = le.inverse_transform([prediction_encoded])[0]

    recommendations = []
    if prediction_label != "Healthy":
        for feature in ["Soil_Moisture", "Soil_Temperature", "Humidity"]:
            current_val = sensor_data[feature]
            healthy_val = average_healthy_values[feature]
            diff = healthy_val - current_val
            recommendations.append(
                f"{'Increase' if diff > 0 else 'Decrease'} {feature.replace('_', ' ')} by {abs(diff):.2f}"
            )
    return prediction_label, recommendations


# --- 4. WebSocket Event Handlers ---
@socketio.on("connect")
def handle_connect():
    print("✅ Client connected.")


@socketio.on("disconnect")
def handle_disconnect():
    print("❌ Client disconnected.")


@socketio.on("sensor_data")
def handle_sensor_data(data):
    """Listens for data from your ESP8266"""
    print(f"📩 Received sensor data: {data}")
    status, suggestions = predict_and_recommend(data)
    payload = {
        "live_data": data,
        "plant_health_status": status,
        "improvement_suggestions": suggestions,
    }
    # Broadcast health updates to ALL connected web browsers
    socketio.emit("health_update", payload)
    print(f"📤 Broadcasted health update.")


@socketio.on("process_frame")
def handle_process_frame(data):
    """Listens for camera frames from your React app"""
    if not disease_model:
        return

    header, encoded = data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_bytes))

    results = disease_model(image, conf=0.4)
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append(
                {
                    "box": box.xyxy[0].tolist(),
                    "label": disease_model.names[int(box.cls[0])],
                    "confidence": box.conf[0].tolist(),
                }
            )

    # --- THIS IS THE CORRECTED LINE ---
    # We now use our main 'socketio' object to emit the message.
    socketio.emit("detection_results", {"detections": detections})


if __name__ == "__main__":
    print("🚀 Starting Unified Real-Time Server...")
    socketio.run(app, host="0.0.0.0", port=5000)
