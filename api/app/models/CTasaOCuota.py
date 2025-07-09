# app/models/CTasaOCuota.py

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()

class TasaOCuota(Base):
	__tablename__ = "c_TasaOCuota"
	__table_args__ = {"schema": "cfdi_system"}  # Si es necesario definir el esquema

	id = Column(Integer, primary_key=True, autoincrement=True)

	ranged_or_fixed = Column(String(50), nullable=True)
	minimum_value = Column(Integer, nullable=True)
	maximum_value = Column(Integer, nullable=True)
	tax = Column(String(50), nullable=True)
	factor = Column(String(50), nullable=True)
	transfer = Column(String(50), nullable=True)
	withholding = Column(String(50), nullable=True)
	effective_start_date = Column(String(50))
	effective_end_date = Column(String(50))
