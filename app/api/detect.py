import os, shutil, uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, Detection
from app.core.config import settings
from app.services.detection_service import classify_image

router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

@router.post("/")
async def detect_waste(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Only JPEG, PNG, or WEBP images are accepted.")

    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.MAX_FILE_SIZE_MB} MB limit.")

    # Save to disk
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext       = file.filename.rsplit(".", 1)[-1]
    save_name = f"{uuid.uuid4()}.{ext}"
    save_path = os.path.join(settings.UPLOAD_DIR, save_name)

    with open(save_path, "wb") as f:
        f.write(contents)

    # Run model
    result = classify_image(save_path)

    # Persist to DB
    detection = Detection(
        filename   = save_name,
        label      = result["label"],
        confidence = result["confidence"],
        category   = result["category"],
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

    return {
        "id":         detection.id,
        "label":      result["label"],
        "confidence": result["confidence"],
        "category":   result["category"],
        "disposal":   result["disposal"],
    }
