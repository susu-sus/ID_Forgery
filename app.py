from flask import Flask, render_template, request, send_from_directory
import os
import cv2
import numpy as np
import pytesseract
from tensorflow.keras.models import load_model

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

model = load_model("model/id_forgery_model.h5")
IMG_SIZE = 128

# -----------------------------
# IMAGE FEATURES
# -----------------------------
def extract_features(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.Laplacian(gray, cv2.CV_64F).var()
    edges = np.sum(cv2.Canny(gray, 100, 200) > 0)
    brightness = np.mean(gray)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    return {
        "blur": round(blur, 2),
        "edges": int(edges),
        "brightness": round(brightness, 2),
        "faces": len(faces)
    }

# -----------------------------
# OCR + TEXT ANALYSIS
# -----------------------------
def extract_text(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)

def text_analysis(text):
    issues = []

    if len(text.strip()) < 15:
        issues.append("Very low text detected (possible fake font)")

    if "  " in text:
        issues.append("Irregular spacing detected")

    if any(char.islower() for char in text) and any(char.isupper() for char in text):
        issues.append("Inconsistent text casing")

    return issues

# -----------------------------
# REPORT GENERATION (MODEL FIRST)
# -----------------------------
def generate_report(path):
    img = cv2.imread(path)

    # MODEL
    img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) / 255.0
    img_resized = np.reshape(img_resized, (1, IMG_SIZE, IMG_SIZE, 3))

    pred = model.predict(img_resized)[0]

    fake_prob = float(pred[0]) * 100
    real_prob = float(pred[1]) * 100

    # FEATURES
    features = extract_features(path)

    # TEXT
    text = extract_text(path)
    text_issues = text_analysis(text)

    issues = []

    # IMAGE CHECKS
    if features["blur"] < 40:
        issues.append("Blur detected")

    if features["edges"] < 250:
        issues.append("Low structural detail")

    if features["faces"] == 0:
        issues.append("No face detected")

    # TEXT CHECKS
    issues.extend(text_issues)

    # FINAL DECISION (MODEL BASED)
    if fake_prob > 60:
        result = "Fake"
        confidence = fake_prob
    elif real_prob > 60:
        result = "Real"
        confidence = real_prob
    else:
        result = "Suspicious"
        confidence = max(fake_prob, real_prob)

    return {
        "prediction": result,
        "confidence": round(confidence, 2),
        "fake_score": round(fake_prob, 2),
        "real_score": round(real_prob, 2),
        "features": features,
        "issues": issues,
        "text": text[:300]
    }

# -----------------------------
# ROUTES
# -----------------------------
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']

    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        report = generate_report(filepath)

        return render_template(
            "report.html",
            report=report,
            filename=filename
        )

    return "No file uploaded"

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)