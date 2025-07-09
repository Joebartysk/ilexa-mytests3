# app/models/CClaveprodServ.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClaveProdServ(Base):
	__tablename__ = "c_ClaveProdServ"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	product_service_code = Column(String, nullable=True)
	description = Column(String, nullable=True)
	include_transferred_vat = Column(String, nullable=True)
	include_transferred_ieps = Column(String, nullable=True)  # Se corrigió el nombre del campo
	required_complement = Column(String, nullable=True)  # Se corrigió el nombre del campo
	effective_start_date = Column(String, nullable=True)
	effective_end_date = Column(String, nullable=True)
	border_zone_stimulus = Column(String, nullable=True)
	similar_words = Column(String, nullable=True)
