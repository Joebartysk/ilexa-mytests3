# app/models/CClaveUnidad.py
from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClaveUnidad(Base):
	__tablename__ = "c_clave_unidad"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	unit_code = Column(String)
	name_unit = Column(String)
	description = Column(TEXT)
	nota_unit = Column(String)
	effective_start_date = Column(String(50))
	effective_end_date = Column(String(50))
	symbol = Column(String)
