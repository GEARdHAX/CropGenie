from flask import Flask
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
from PIL import Image
import io
import base64

app = Flask(__name__)
# Allow all origins for easy development
socketio = SocketIO(app, cors_allowed_origins="*")

# Load your custom-trained YOLOv8 model
try:
    model = YOLO("best.pt")
    print("✅ YOLO model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading YOLO model: {e}")
    exit()


@socketio.on("connect")
def handle_connect():
    print("✅ Client connected to detection server.")


@socketio.on("disconnect")
def handle_disconnect():
    print("❌ Client disconnected.")


@socketio.on("process_frame")
def handle_process_frame(data):
    """
    Receives a video frame from the client, runs detection, and sends results back.
    """
    # The client sends the frame as a Base64 encoded Data URL
    # We need to strip the header and decode it
    try:
        header, encoded = data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        print(f"Error decoding image: {e}")
        return

    # Run YOLO inference
    results = model(image, conf=0.4)  # Adjust confidence threshold as needed

    # Process results
    detections = []
    # Get image dimensions for scaling on the frontend
    img_width, img_height = image.size

    for result in results:
        for box in result.boxes:
            coords = box.xyxy[0].tolist()
            class_name = model.names[int(box.cls[0])]
            confidence = box.conf[0].tolist()
            detections.append(
                {"box": coords, "label": class_name, "confidence": confidence}
            )

    payload = {
        "detections": detections,
        "image_width": img_width,
        "image_height": img_height,
    }

    # Send the results back to the client that sent the frame
    emit("detection_results", payload)


if __name__ == "__main__":
    print("🚀 Starting real-time detection server...")
    # Use '0.0.0.0' to make it accessible on your local network
    socketio.run(app, host="0.0.0.0", port=5000)
