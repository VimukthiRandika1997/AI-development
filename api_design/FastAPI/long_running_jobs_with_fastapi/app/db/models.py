# SQLAlchemy Job model
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, default="pending")
    result = Column(Text, nullable=True)
    callback_url = Column(String, nullable=True)
