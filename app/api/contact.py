from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db, ContactMessage

router = APIRouter()

class ContactIn(BaseModel):
    name:    str
    email:   EmailStr
    message: str

@router.post("/")
def submit_contact(data: ContactIn, db: Session = Depends(get_db)):
    if len(data.message.strip()) < 10:
        raise HTTPException(400, "Message too short.")

    msg = ContactMessage(name=data.name, email=data.email, message=data.message)
    db.add(msg)
    db.commit()

    # TODO: send email notification here (e.g. via SendGrid / SMTP)

    return {"status": "received", "message": "Thanks! We'll get back to you soon."}
