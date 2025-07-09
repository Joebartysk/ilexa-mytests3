# app/models/CImpuesto.py

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager

Base = declarative_base()

class Impuesto(Base):
	__tablename__ = "c_Impuesto"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	c_tax = Column(String, nullable=True)  # Mapeo de varchar
	description = Column(TEXT, nullable=True)
	tax_withholding = Column(String, nullable=True)
	tax_transferred = Column(String, nullable=True)
	local_federal = Column(String, nullable=True)
	effective_start_date = Column(String, nullable=True)  # Mapeo de text
	effective_end_date = Column(String, nullable=True)
