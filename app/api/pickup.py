from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db, PickupSchedule
from datetime import datetime

router = APIRouter()

class PickupRequest(BaseModel):
    name:       str
    address:    str
    waste_type: str
    date:       str
    time:       str
    notes:      str = ""

@router.post("/")
def schedule_pickup(data: PickupRequest, db: Session = Depends(get_db)):
    if not data.name or not data.address or not data.waste_type:
        raise HTTPException(400, "Name, address and waste type are required.")

    pickup = PickupSchedule(
        name       = data.name,
        address    = data.address,
        waste_type = data.waste_type,
        date       = data.date,
        time       = data.time,
        notes      = data.notes,
        status     = "pending"
    )
    db.add(pickup)
    db.commit()
    db.refresh(pickup)

    return {
        "id":        pickup.id,
        "status":    "scheduled",
        "message":   f"Pickup scheduled for {data.date} at {data.time}",
        "reference": f"ECO-{pickup.id:04d}"
    }

@router.get("/")
def get_pickups(db: Session = Depends(get_db)):
    rows = db.query(PickupSchedule).order_by(PickupSchedule.created_at.desc()).all()
    return [
        {
            "id":         r.id,
            "name":       r.name,
            "address":    r.address,
            "waste_type": r.waste_type,
            "date":       r.date,
            "time":       r.time,
            "status":     r.status,
            "reference":  f"ECO-{r.id:04d}",
            "created_at": r.created_at,
        }
        for r in rows
    ]