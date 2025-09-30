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
    try:
        header, encoded = data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        print(f"Error decoding image: {e}")
        return

    # Run YOLO inference
    results = model(image, conf=0.4)

    # Process results
    detections = []
    img_width, img_height = image.size

    for result in results:
        for box in result.boxes:
            # Original coordinates [x1, y1, x2, y2]
            coords = box.xyxy[0].tolist()
            class_name = model.names[int(box.cls[0])]
            confidence = box.conf[0].tolist()

            # ====================================================================
            # ## --- START OF MODIFICATION: Shrink the Bounding Box --- ##
            # ====================================================================

            # You can change this value. 0.05 = 5% padding on each side.
            padding_factor = 0.05

            x1, y1, x2, y2 = coords
            box_width = x2 - x1
            box_height = y2 - y1

            # Calculate the padding to add/subtract
            x_padding = box_width * padding_factor
            y_padding = box_height * padding_factor

            # Apply the padding to shrink the box
            new_x1 = x1 + x_padding
            new_y1 = y1 + y_padding
            new_x2 = x2 - x_padding
            new_y2 = y2 - y_padding

            # Ensure the new box is still valid
            if new_x1 < new_x2 and new_y1 < new_y2:
                shrunken_coords = [new_x1, new_y1, new_x2, new_y2]
            else:
                shrunken_coords = coords  # Use original if shrinking makes it invalid

            # ====================================================================
            # ## --- END OF MODIFICATION --- ##
            # ====================================================================

            detections.append(
                # Use the new, smaller coordinates
                {"box": shrunken_coords, "label": class_name, "confidence": confidence}
            )

    payload = {
        "detections": detections,
        "image_width": img_width,
        "image_height": img_height,
    }

    emit("detection_results", payload)


if __name__ == "__main__":
    print("🚀 Starting real-time detection server...")
    socketio.run(app, host="0.0.0.0", port=8080)
