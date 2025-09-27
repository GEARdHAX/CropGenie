import pandas as pd
import joblib
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from flask import Flask
from flask_sock import Sock

# --- This is the new part: A set to store all connected clients ---
clients = set()


# --- Part 1: Train and Save the ML Model (runs only if model files are missing) ---
def train_and_save_model():
    print("=" * 50)
    print(
        "🤖 Model files not found. Training a new model from plant_health_data.csv..."
    )
    try:
        df = pd.read_csv("plant_health_data.csv")
    except FileNotFoundError:
        print("❌ FATAL ERROR: 'plant_health_data.csv' not found.")
        return False

    features = ["Soil_Moisture", "Soil_Temperature", "Humidity"]
    target = "Plant_Health_Status"

    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])

    X = df[features]
    y = df[target]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    healthy_encoded_value = le.transform(["Healthy"])[0]
    healthy_plants_data = df[df[target] == healthy_encoded_value]
    average_healthy_values = healthy_plants_data[features].mean()

    joblib.dump(model, "plant_health_model.pkl")
    joblib.dump(le, "label_encoder.pkl")
    joblib.dump(average_healthy_values, "healthy_averages.pkl")

    print("\n✅ Model, Encoder, and Averages saved to .pkl files.")
    print("=" * 50)
    return True


# --- Part 2: Load Model and Define Prediction Logic ---
if not all(
    os.path.exists(f)
    for f in ["plant_health_model.pkl", "label_encoder.pkl", "healthy_averages.pkl"]
):
    if not train_and_save_model():
        exit()

model = joblib.load("plant_health_model.pkl")
le = joblib.load("label_encoder.pkl")
average_healthy_values = joblib.load("healthy_averages.pkl")
print("\n🧠 ML Model and helper files loaded successfully.")


def predict_and_recommend(sensor_data):
    input_df = pd.DataFrame(
        [sensor_data], columns=["Soil_Moisture", "Soil_Temperature", "Humidity"]
    )
    prediction_encoded = model.predict(input_df)[0]
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


# --- Part 3: Setup the Flask WebSocket Server with Broadcasting ---
app = Flask(__name__)
sock = Sock(app)


@sock.route("/ws")
def websocket_handler(ws):
    # Add the new client to our set of connected clients
    clients.add(ws)
    print(f"📲 Client connected. Total clients: {len(clients)}")

    try:
        while True:
            # We still listen for messages, primarily from the ESP8266
            message = ws.receive()
            sensor_readings = json.loads(message)
            print(f"📩 Received from ESP8266: {sensor_readings}")

            # Run the prediction
            status, suggestions = predict_and_recommend(sensor_readings)

            response_payload = {
                "live_data": sensor_readings,
                "plant_health_status": status,
                "improvement_suggestions": suggestions,
            }

            # --- This is the key change: Broadcast to ALL clients ---
            # Create a list of clients to iterate over, to avoid issues if the set changes size
            for client in list(clients):
                try:
                    client.send(json.dumps(response_payload))
                except Exception:
                    # If sending fails, the client has probably disconnected. Remove them.
                    clients.remove(client)

            print(f"📤 Broadcasted results to {len(clients)} client(s).")

    finally:
        # This code runs when a client disconnects
        clients.remove(ws)
        print(f"❌ Client disconnected. Total clients: {len(clients)}")


if __name__ == "__main__":
    print("\n🚀 Starting Flask Server with Broadcasting...")
    print("WebSocket is available at ws://172.25.25.112:5000/ws")
    app.run(host="0.0.0.0", port=5000)
