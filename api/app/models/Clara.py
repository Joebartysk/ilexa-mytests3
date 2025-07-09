# app/models/Clara.py
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

class ClaraRecord(Base):
    __tablename__ = "clara"
    __table_args__ = {"schema": "cfdi_system"}

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String)
    transaction_date = Column(String)
    account_statement = Column(String)
    transaction = Column(String)
    original_amount = Column(String)
    original_currency = Column(String)
    mxn_amount = Column(String)
    card = Column(String)
    card_alias = Column(String)
    status = Column(String)
    approval_status = Column(String)
    approver_name = Column(String)
    approver_note = Column(String)
    authorization_code = Column(String)
    purchase_category = Column(String)
    electronic_invoice = Column(String)
    auto_vin_invoise = Column(String)
    auto_linked_invoice = Column(String)
    attached = Column(String)
    attached_files = Column(String)
    tax_folio = Column(String)
    holder = Column(String)
    groups = Column(String)
    location = Column(String)
    labels = Column(String)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class UploadResponse(BaseModel):
	success: bool
	records_inserted: int
	message: str
	filename: str

class ClaraRecordResponse(BaseModel):
	id: int
	unique_id: str
	card: str
	card_alias: str
	mxn_amount: float
	transaction_date: str
	created_at: datetime

	class Config:
		from_attributes = True