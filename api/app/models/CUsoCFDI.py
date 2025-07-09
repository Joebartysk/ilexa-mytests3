# app/models/CUsoCFDI.py
from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UsoCFDI(Base):
	__tablename__ = "c_UsoCFDI"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	cfdi_use_code = Column(String)  # Mapeo de text NULL
	description = Column(TEXT)	  # Mapeo de text NULL
	fisica = Column(String)		 # Mapeo de text NULL
	moral = Column(String)		  # Mapeo de text NULL
	effective_start_date = Column(String)  # Mapeo de text NULL
	effective_end_date = Column(String)   # Mapeo de text NULL (se corrigió el nombre)
	recipient_tax_regime = Column(String)  # Mapeo de text NULL
