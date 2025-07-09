# app/models/CPatenteAduanal.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PatenteAduanal(Base):
	__tablename__ = "c_patenteaduanal"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	c_customs = Column(Integer, nullable=True)  # Mapeo de int4
	effective_start_date = Column(String(50), nullable=True)
	effective_end_date = Column(String(50), nullable=True)
