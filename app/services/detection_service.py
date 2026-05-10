from app.core.config import settings
import joblib
import cv2
import numpy as np

WASTE_CLASSES = {
    "plastic":   "recyclable",
    "paper":     "recyclable",
    "metal":     "recyclable",
    "glass":     "recyclable",
    "organic":   "organic",
    "food":      "organic",
    "hazardous": "non-recyclable",
    "general":   "non-recyclable",
}

def classify_image(image_path: str) -> dict:
    label, confidence = _run_model(image_path)
    category = WASTE_CLASSES.get(label, "non-recyclable")

    return {
        "label":      label,
        "confidence": round(confidence, 3),
        "category":   category,
        "disposal":   _disposal_advice(label, category),
    }

_model = None

def _run_model(image_path: str):
    global _model
    if _model is None:
        _model = joblib.load(settings.MODEL_PATH)

    img = cv2.imread(image_path)
    img = cv2.resize(img, (32, 32))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    features = img.flatten().reshape(1, -1)

    label      = _model.predict(features)[0]
    proba      = _model.predict_proba(features)[0]
    confidence = float(max(proba))

    return label, confidence

def _disposal_advice(label: str, category: str) -> str:
    advice = {
        "plastic":   "🔵 Place in the BLUE recycling bin. Rinse containers before disposal.",
        "paper":     "🔵 Place in the BLUE recycling bin. Flatten boxes to save space.",
        "metal":     "🔵 Place in the BLUE recycling bin. Rinse cans and tins before recycling.",
        "glass":     "🟤 Place in the BROWN glass bin. Remove lids and rinse bottles first.",
        "organic":   "🟢 Place in the GREEN compost bin. No plastics or packaging.",
        "food":      "🟢 Place in the GREEN compost bin. Wrap in newspaper if possible.",
        "hazardous": "🔴 Place in the RED hazardous waste bin. Do NOT mix with general waste — take to a designated collection point.",
        "general":   "⚫ Place in the BLACK general waste bin. Consider if any parts can be recycled first.",
    }

    fallback = {
        "recyclable":     "🔵 Place in the BLUE recycling bin.",
        "organic":        "🟢 Place in the GREEN compost bin.",
        "non-recyclable": "⚫ Place in the BLACK general waste bin.",
    }

    return advice.get(label, fallback.get(category, "Check local waste disposal guidelines."))
