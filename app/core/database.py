from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ── Models ──────────────────────────────────────────────
class Detection(Base):
    __tablename__ = "detections"
    id          = Column(Integer, primary_key=True, index=True)
    filename    = Column(String)
    label       = Column(String)          # e.g. "plastic", "organic", "metal"
    confidence  = Column(Float)
    category    = Column(String)          # recyclable / non-recyclable / organic
    created_at  = Column(DateTime, default=datetime.utcnow)

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String)
    email      = Column(String)
    message    = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class PickupSchedule(Base):
    __tablename__ = "pickup_schedules"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String)
    address    = Column(String)
    waste_type = Column(String)
    date       = Column(String)
    time       = Column(String)
    notes      = Column(String, default="")
    status     = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
# ── Helpers ─────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
