# app/models/CTipoComprobante.py

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()

class TipoComprobante(Base):
	__tablename__ = "c_TipoComprobante"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True)
	voucher_type_code = Column(String)
	description = Column(TEXT)
	max_value = Column(String)
	effective_start_date = Column(String)
	effective_end_date = Column(String)
