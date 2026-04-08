# ID Forgery Detection System

## Overview

This project detects whether an ID document is **Real or Fake** using Deep Learning and Image Processing techniques.

---

## Approach

The system uses:

* **CNN Model (Primary)**

  * Learns visual patterns from ID images
  * Classifies documents as Real or Fake

* **Image Processing (Supporting)**

  * Blur Detection
  * Edge Detection
  * Image Quality Checks

* **OCR (Text Analysis)**

  * Extracts text from ID
  * Detects inconsistencies

---

## Architecture

User Upload → Flask App → Preprocessing → CNN Model → Feature Analysis → Prediction → Report Display

---

## Tools & Technologies

* Python
* Flask
* TensorFlow / Keras
* OpenCV
* Tesseract OCR
* HTML, CSS

---

## Features

* AI-based forgery detection
* Real vs Fake classification
* Image quality analysis
* OCR-based text validation
* Professional report UI

---

## ▶️ How to Run

1. Install dependencies:
   pip install flask opencv-python numpy pytesseract tensorflow

2. Run the app:
   python app.py

3. Open in browser:
   http://127.0.0.1:5000

---

## Output

* Prediction: Real / Fake / Suspicious
* Confidence score
* Image analysis results
* Extracted text

---

## Limitations

* Depends on training data quality
* Not 100% accurate

---

## Future Improvements

* Cloud upload (Google Drive)
* Advanced font detection
* Explainable AI (heatmaps)

---

## Summary

This project combines Deep Learning, Image Processing, and OCR to provide an automated solution for detecting forged ID documents.

The dataset used in this project was manually collected and prepared for experimental purposes.
