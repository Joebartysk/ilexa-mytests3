# app/models/CMetodoPago.py

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()

class MetodoPago(Base):
	__tablename__ = "c_MetodoPago"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	payment_method_code = Column(String, nullable=True)  # Mapeo de text
	description = Column(TEXT, nullable=True)
	effective_start_date = Column(Date, nullable=True)  # Mapeo de date
	effective_end_date = Column(Date, nullable=True)
