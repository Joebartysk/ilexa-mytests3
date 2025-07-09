# app/models/CPais.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pais(Base):
	__tablename__ = "c_pais"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	c_country = Column(String(50), nullable=True)  # Mapeo de varchar(50)
	description = Column(String(50), nullable=True)
	postcode_format = Column(String(50), nullable=True)
	tax_identity_registration_format = Column(String(50), nullable=True)
	tax_identity_registration_validation = Column(String(50), nullable=True)
	groups = Column(String(50), nullable=True)
