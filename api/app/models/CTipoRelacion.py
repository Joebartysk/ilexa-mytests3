# app/models/CTipoRelacion.py

from sqlalchemy import Column, Integer, String, Sequence, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TipoRelacion(Base):
	__tablename__ = "c_TipoRelacion"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	relation_type_code = Column(String, nullable=True)  # Mapeo de varchar
	description = Column(TEXT, nullable=True)		  # Mapeo de text
	effective_start_date = Column(String, nullable=True)  # Mapeo de text
	effective_end_date = Column(String, nullable=True)	# Mapeo de text
