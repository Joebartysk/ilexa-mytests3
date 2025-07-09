# app/models/CMeses.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Meses(Base):
	__tablename__ = "c_meses"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	c_month = Column(Integer, nullable=True)  # Mapeo de int4
	description = Column(String(50), nullable=True)
	effective_start_date = Column(String(50), nullable=True)
	effective_end_date = Column(String(50), nullable=True)
