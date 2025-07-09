# app/models/HSBC.py
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

class HSBCRecord(Base):
    __tablename__ = "hsbc"
    __table_args__ = {"schema": "cfdi_system"}

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String)
    asofdate = Column(String)
    asoftime = Column(String)
    intraend = Column(String)
    ccycode = Column(String)
    ccycodetyp = Column(String)
    accounttype = Column(String)
    accountno = Column(String)
    branchid = Column(String)
    insttid = Column(String)
    uschipsid = Column(String)
    xitroutnum = Column(String)
    accname = Column(String)
    uksortcde = Column(String)
    entrydate = Column(String)
    ledgerbala = Column(String)#Float
    openavlbal = Column(String)#Float
    openbal = Column(String)#Float
    clearedbal = Column(String)#Float
    adjustbal = Column(String)#Float
    depositbal = Column(String)#Float
    totalfloat = Column(String)#Float
    savavail = Column(String)#Float
    onedayfloa = Column(String)#Float
    twodayfloa = Column(String)#Float
    threedayfloa = Column(String)  # >3DAYFLOAT #Float
    total_cred = Column(String)#Float
    noofcredit = Column(String)
    autocrclea = Column(String)#Float
    total_debi = Column(String)#Float
    noofdebits = Column(String)
    autodrclea = Column(String)#Float
    hocollecti = Column(String)#Float
    creditfac = Column(String)#Float
    intaccr = Column(String)#Float
    intrate = Column(String)#Float
    xacttype = Column(String)
    val_date = Column(String)
    xacttime = Column(String)
    stmtdate = Column(String)
    fieldamoun = Column(String)
    textline1 = Column(String)
    textline2 = Column(String)
    textline3 = Column(String)
    textline4 = Column(String)
    textline5 = Column(String)
    textline6 = Column(String)
    textline7 = Column(String)
    textline8 = Column(String)
    textline9 = Column(String)
    textline10 = Column(String)
    textline11 = Column(String)
    textline12 = Column(String)
    textline13 = Column(String)
    holdamt = Column(String)#Float
    created_at = Column(DateTime, default=datetime.utcnow)

class UploadResponse(BaseModel):
	success: bool
	records_inserted: int
	message: str
	filename: str

class HSBCRecordResponse(BaseModel):
	id: int
	unique_id: str
	accountno: str
	accname: str
	ledgerbala: float
	asofdate: str
	created_at: datetime

	class Config:
		from_attributes = True