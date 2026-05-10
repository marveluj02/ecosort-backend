from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import detect, stats, contact, pickup
from app.core.config import settings

app = FastAPI(title="EcoSort API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router,   prefix="/api/detect",  tags=["Detection"])
app.include_router(stats.router,    prefix="/api/stats",   tags=["Stats"])
app.include_router(contact.router,  prefix="/api/contact", tags=["Contact"])
app.include_router(pickup.router,   prefix="/api/pickup",  tags=["Pickup"])

@app.get("/")
def root():
    return {"status": "EcoSort API is running"}