# app/models/CMetodoPago.py

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()

class RegimenFiscal(Base):
	__tablename__ = "c_RegimenFiscal"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	tax_regime_code = Column(String, nullable=True)  # Mapeo de varchar/text
	description = Column(TEXT, nullable=True)
	fisica = Column(String, nullable=True)
	moral = Column(String, nullable=True)
	effective_start_date = Column(String, nullable=True)  # Mapeo de text
	effective_end_date = Column(String, nullable=True)	 # Mapeo de text
