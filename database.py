from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///predictions.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_score = Column(Integer)
    attendance = Column(Integer)
    submission = Column(Integer)
    study_hours = Column(Float)
    cgpa = Column(Float)
    extracurricular = Column(Integer)
    predicted_tier = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
print("✅ SQL Database architecture ready.")