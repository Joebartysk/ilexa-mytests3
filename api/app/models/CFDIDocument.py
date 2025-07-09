# app/models/CFDIDocument.py

from sqlalchemy import BigInteger, Column, Integer, String, Date, DateTime, func, DECIMAL, TEXT, LargeBinary, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
# from app.core.DBConnect import DatabaseConfig, SessionManager
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager

Base = declarative_base()

class CFDIModel(Base):
	__tablename__ = "cfdi_documents"
	__table_args__ = {"schema": "cfdi_system"}

	cfdi_id = Column(Integer, primary_key=True)
	version = Column(String(255), nullable=False)
	series = Column(String(255))
	number_leaf = Column(Integer)
	dates = Column(Date, nullable=False)
	stamp = Column(String(255))
	form_of_payment = Column(String(255))
	certificate_number = Column(String(255))
	certificate = Column(TEXT)
	payment_terms = Column(TEXT)
	subtotal = Column(DECIMAL(18, 2), nullable=False)
	discount = Column(DECIMAL(18, 2))
	currency = Column(String(3))
	exchange_rate = Column(DECIMAL(18, 6))
	total = Column(DECIMAL(18, 2), nullable=False)
	type_of_fiscal_document = Column(String(50), nullable=False)
	export = Column(String(2))
	payment_method = Column(String(255), nullable=False)
	place_of_issuance = Column(String(255), nullable=False)
	confirmation = Column(String(255))
	periodicity = Column(Integer)
	months = Column(Integer)
	years = Column(Integer)
	type_of_relationship = Column(String(255))
	uuid = Column(String(36), unique=True, nullable=False)
	rfc_of_the_issuer = Column(String(13), nullable=False)
	name_of_the_issuer = Column(String(255), nullable=False)
	tax_regime_of_the_issuer = Column(String(255), nullable=False)
	rfc_of_the_receiver = Column(String(13))
	name_of_the_receiver = Column(String(255))
	tax_address_of_the_receiver = Column(TEXT)
	fiscal_residence_of_the_receiver = Column(TEXT)
	tax_identification_number_of_the_receiver = Column(String(20))
	tax_regime_of_the_receiver = Column(String(255))
	use_of_cfdi = Column(String(255), nullable=False)
	concepts = Column(TEXT)
	total_retained_taxes = Column(DECIMAL(18, 2))
	total_transferred_taxes = Column(DECIMAL(18, 2))
	# company_id = Column(Integer, ForeignKey("companies.company_id"))
	company_id = Column(BigInteger)
	status = Column(String(77))
	xml_path = Column(String(255))
	created_at = Column(DateTime)
	last_check_status = Column(DateTime)

class CFDI_CRUD:
	def __init__(self):
		self.session_manager = SessionManager(DatabaseConfig())

	def create_cfdi(self, **kwargs):
		"""
		Creates a new CFDI document.
		Parámetros:
			xml_uuid: UUID del XML
			company_id: ID de la empresa
			cfdi_type: Tipo de comprobante (I, E, P, N, T)
			emission_date: Fecha de emisión
			certification_date:Fecha de certificación
			subtotal: Subtotal
			total: Total
			receiver_tax_id: RFC del receptor
			receiver_name: Nombre del receptor
			xml_content: Contenido XML en bytes
		"""
		try:
			session = self.session_manager.get_session()
			cfdi = CFDIModel(**kwargs)
			session.add(cfdi)
			session.commit()
			return True
		except Exception as e:
			print(f"Error creating CFDI document: {str(e)}")
			return False

	def get_all_cfdis(self):
		try:
			session = self.session_manager.get_session()
			cfdis = session.query(CFDIModel).all()
			# Convertimos los objetos a diccionario
			result = [dict(cfdi.__dict__) for cfdi in cfdis]
			self.session_manager.close_session(session)
			return result
		except Exception as e:
			print(f"Error getting all CFDIs: {str(e)}")
			return []

	def get_cfdi_by_id(self, cfdi_id):
		try:
			session = self.session_manager.get_session()
			cfdi = session.query(CFDIModel).get(cfdi_id)
			if cfdi is not None:
				return dict(cfdi.__dict__)
			return None
		except Exception as e:
			print(f"Error getting CFDI by ID: {str(e)}")
			return None

	def update_cfdi(self, cfdi_id, **kwargs):
		try:
			with self.session_manager.get_session() as session:
			# session = self.session_manager.get_session()
				cfdi = session.query(CFDIModel).get(cfdi_id)
				if cfdi is not None:
					for key, value in kwargs.items():
						setattr(cfdi, key, value)
					session.commit()
					self.session_manager.close_session(session)
					return True
				self.session_manager.close_session(session)
				return False
		except Exception as e:
			print(f"Error updating CFDI: {str(e)}")
			return False

	def delete_cfdi(self, cfdi_id):
		try:
			session = self.session_manager.get_session()
			cfdi = session.query(CFDIModel).get(cfdi_id)
			if cfdi is not None:
				session.delete(cfdi)
				session.commit()
				return True
			return False
		except Exception as e:
			print(f"Error deleting CFDI: {str(e)}")
			return False

	def search_cfdi(self, filters):
		"""
		Busca un comprobante fiscal según los filtros proporcionados.

		Parámetros:
			filters: Diccionario con los campos a buscar (ej. {'receiver_tax_id': 'XAXXX01', 'cfdi_type': 'I'})
		Retorna:
			Lista de diccionarios con los datos del comprobante
		"""
		try:
			session = self.session_manager.get_session()
			cfdis = session.query(CFDIModel).filter_by(**filters).all()
			result = [dict(cfdi.__dict__) for cfdi in cfdis]
			return result
		except Exception as e:
			print(f"Error searching CFDI: {str(e)}")
			return []
