# app/models/CExportacion.py

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager

Base = declarative_base()

class Exportacion(Base):
	__tablename__ = "c_Exportacion"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, autoincrement=True)
	export_code = Column(String, nullable=True)
	description = Column(TEXT, nullable=True)
	effective_start_date = Column(String, nullable=True)  # Se mantiene como String ya que es text en la tabla
	effective_end_date = Column(String, nullable=True)
