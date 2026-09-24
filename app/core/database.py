from sqlalchemy import Column, Integer, Float, String, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/risk_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_features = Column(JSON)
    prediction = Column(Integer)
    probability = Column(Float)
    shap_analysis = Column(JSON)
    llm_explanation = Column(JSON)

def init_db():
    # This will fail if DB is not running, which is fine for local setup script
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Database initialization skipped or failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
