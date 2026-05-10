from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_PATH: str = "models/model.pkl"   # path to your trained YOLO/TF model
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10
    CONFIDENCE_THRESHOLD: float = 0.5
    DATABASE_URL: str = "sqlite:///./ecosort.db"   # swap for PostgreSQL in prod

    class Config:
        env_file = ".env"

settings = Settings()
