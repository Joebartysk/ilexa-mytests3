# app/models/CMetodoPago.py

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()

class Moneda(Base):
	__tablename__ = "c_Moneda"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	currency_code = Column(String, nullable=True)  # Mapeo de text
	description = Column(TEXT, nullable=True)
	decimal_places = Column(Integer, nullable=True)
	variation_percentage = Column(String, nullable=True)
	effective_start_date = Column(String, nullable=True)  # Mapeo de text
	effective_end_date = Column(String, nullable=True)
