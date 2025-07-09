# app/models/CFormaPago.py

from sqlalchemy import Column, Integer, String, TEXT, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager

Base = declarative_base()

class FormaPago(Base):
	__tablename__ = "c_FormaPago"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	payment_method = Column(Integer, nullable=True)  # Mapeo de int8
	description = Column(TEXT, nullable=True)
	is_banked = Column(String, nullable=True)
	operation_number = Column(String, nullable=True)
	payer_account_rfc = Column(String, nullable=True)
	payer_account = Column(String, nullable=True)
	payer_account_pattern = Column(String, nullable=True)
	beneficiary_account_rfc = Column(String, nullable=True)
	beneficiary_account = Column(String, nullable=True)
	beneficiary_account_pattern = Column(String, nullable=True)
	payment_chain_type = Column(String, nullable=True)
	payer_bank_name_if_external = Column(String, nullable=True)
	effective_start_date = Column(Date, nullable=True)  # Mapeo de date
	effective_end_date = Column(String, nullable=True)
