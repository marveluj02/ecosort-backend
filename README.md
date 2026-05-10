# EcoSort Backend

FastAPI backend for the EcoSort waste classification system.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create a .env file (optional — defaults work out of the box)
echo "MODEL_PATH=models/your_model.pt" > .env

# 3. Initialise the database & run
python -c "from app.core.database import init_db; init_db()"
uvicorn app.main:app --reload --port 8000
```

Interactive docs → http://localhost:8000/docs

---

## API Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/api/detect/` | Upload image → get waste label + disposal advice |
| GET | `/api/stats/summary` | Total detections, breakdown by category/label |
| GET | `/api/stats/weekly` | Daily counts for last 7 days (for bar chart) |
| GET | `/api/stats/recent` | Last N detections (for dashboard feed) |
| POST | `/api/contact/` | Save contact form submission |

---

## Wiring in Your Model

Open `app/services/detection_service.py` and replace the body of `_run_model()` with your real inference code. Comments inside show YOLO and TF/Keras examples.

## Project Structure

```
ecosort-backend/
├── app/
│   ├── main.py                  # FastAPI app + CORS
│   ├── core/
│   │   ├── config.py            # Settings / env vars
│   │   └── database.py          # SQLAlchemy models + session
│   ├── api/
│   │   ├── detect.py            # /api/detect
│   │   ├── stats.py             # /api/stats
│   │   └── contact.py           # /api/contact
│   └── services/
│       └── detection_service.py # Model inference (swap stub for real model)
├── uploads/                     # Saved images
├── requirements.txt
└── README.md
```
