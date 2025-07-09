# app/models/BBVA.py
from sqlalchemy import Column, Integer, String, Float, DateTime, TEXT, ForeignKey, Date, UniqueConstraint, Index, \
	Enum as SQLAlchemyEnum, Boolean, TIMESTAMP as SQLAlchemyTimestamp
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import sys
import os
from datetime import datetime
import pytz
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager

Base = declarative_base()

class BBVARecord(Base):
    __tablename__ = "bbva"
    __table_args__ = {"schema": "cfdi_system"}

    id = Column(Integer, primary_key=True, index=True)
    movement_date = Column(String)
    concept_reference = Column(String)
    charge = Column(String)
    payment = Column(String)
    balance = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class UploadResponse(BaseModel):
	success: bool
	records_inserted: int
	message: str
	filename: str

class BBVARecordResponse(BaseModel):
	id: int
	charge: float
	balance: float
	payment: float
	movement_date: str
	created_at: datetime

	class Config:
		from_attributes = True