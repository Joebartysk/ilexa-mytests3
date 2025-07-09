# app/models/CTIpoFactor.py

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TipoFactor(Base):
	__tablename__ = "c_TipoFactor"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	factor_type_code = Column(String)
	effective_start_date = Column(String)  # Mapeo de text
	effective_end_date = Column(String)	# Mapeo de text
