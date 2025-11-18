from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load model
model = tf.keras.models.load_model("model.h5")

labels = [
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___healthy'
]

def preprocess_image(image_file):
    img = Image.open(image_file).resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")   # serve frontend

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    img = preprocess_image(request.files["image"])
    preds = model.predict(img)
    idx = np.argmax(preds)
    conf = float(np.max(preds)) * 100

    return jsonify({
        "disease": labels[idx],
        "confidence": round(conf, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
