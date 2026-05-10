from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import defaultdict
from app.core.database import get_db, Detection
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(Detection).count()
    by_category = (
        db.query(Detection.category, func.count(Detection.id))
        .group_by(Detection.category)
        .all()
    )
    by_label = (
        db.query(Detection.label, func.count(Detection.id))
        .group_by(Detection.label)
        .all()
    )
    avg_conf = db.query(func.avg(Detection.confidence)).scalar() or 0

    return {
        "total_detections": total,
        "average_confidence": round(avg_conf, 3),
        "by_category": {cat: cnt for cat, cnt in by_category},
        "by_label":    {lbl: cnt for lbl, cnt in by_label},
    }

@router.get("/weekly")
def get_weekly(db: Session = Depends(get_db)):
    """Returns daily detection counts for the past 7 days."""
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    rows = (
        db.query(func.date(Detection.created_at), func.count(Detection.id))
        .filter(Detection.created_at >= seven_days_ago)
        .group_by(func.date(Detection.created_at))
        .all()
    )
    return [{"date": str(date), "count": cnt} for date, cnt in rows]

@router.get("/recent")
def get_recent(limit: int = 10, db: Session = Depends(get_db)):
    rows = (
        db.query(Detection)
        .order_by(Detection.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id":         r.id,
            "label":      r.label,
            "category":   r.category,
            "confidence": r.confidence,
            "created_at": r.created_at,
        }
        for r in rows
    ]
