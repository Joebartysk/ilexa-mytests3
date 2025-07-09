# app/models/CPeriodicidad.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Periodicidad(Base):
	__tablename__ = "c_periodicidad"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	period = Column(String(10))
	description = Column(String(50))
	effective_start_date = Column(String(50))
	effective_end_date = Column(String(50))
