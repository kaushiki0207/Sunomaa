from sqlalchemy import Column, Integer, Boolean, Text
from database import Base

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)

    age = Column(Integer)
    hot_flashes = Column(Boolean)
    mood_swings = Column(Boolean)
    chest_pain = Column(Boolean)
    sleep_issue = Column(Boolean)
    irregular_period = Column(Boolean)

    ai_advice = Column(Text)
