# app/core/CRUD.py

from sqlalchemy import func, inspect, select, String, or_
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager
from app.core.logger_config import setup_logger

logger = setup_logger()

class CRUD:
	def __init__(self, model):
		self.model = model
		self.session_manager = SessionManager(DatabaseConfig())
		self.page_size = 10  # Tamaño por defecto de la página
		self.current_page = 1

	def create(self, **kwargs):
		"""
		Creates a new row.
		"""
		try:
			instance = self.model(**kwargs)
			session = self.session_manager.get_session()
			session.add(instance)
			session.flush()
			session.commit()
			if not instance.id:
				return {"message": "registro insertado correctamente."}
			return {
				"message": "registro insertado correctamente.",
				"id_insertado": instance.id
			}
		except Exception as e:
			logger.error(f"Error creating record: {str(e)}")
			return False
		finally:
			session.close()
			self.session_manager.close_session(session)

	def get_all(self):
		try:
			session = self.session_manager.get_session()
			rows = session.query(self.model).all()
			# Convertimos los objetos a diccionario
			result = [dict(row.__dict__) for row in rows]
			return result
		except Exception as e:
			logger.error(f"Error getting all records: {str(e)}")
			return []
		finally:
			session.close()
			self.session_manager.close_session(session)

	def get_count(self):
		try:
			session = self.session_manager.get_session()
			rows = session.query(self.model).count()
			# Convertimos los objetos a diccionario
			#result = [dict(row.__dict__) for row in rows]
			return rows
		except Exception as e:
			logger.error(f"Error getting count records: {str(e)}")
			return []
		finally:
			session.close()
			self.session_manager.close_session(session)

	def get_by_id(self, id_row):
		try:
			session = self.session_manager.get_session()
			row = session.query(self.model).get(id_row)
			if row is not None:
				return dict(row.__dict__)
			return None
		except Exception as e:
			logger.error(f"Error getting record by ID: {str(e)}")
			return None
		finally:
			session.close()
			self.session_manager.close_session(session)

	def update(self, id_row, **kwargs):
		try:
			# with self.session_manager.get_session() as session:
			session = self.session_manager.get_session()
			row = session.query(self.model).get(id_row)
			if row is not None:
				for key, value in kwargs.items():
					setattr(row, key, value)
				session.commit()
				print(row)
				if not row.id:
					return {"message": "registro actualizado correctamente."}
				return {
					"message": "registro actualizado correctamente.",
					"id_actualizado": row.id
				}
			return {
				"message": "no se realizao ningun cambio."
			}
		except Exception as e:
			logger.error(f"Error updating record: {str(e)}")
			return False
		finally:
			session.close()
			self.session_manager.close_session(session)

	def delete(self, id_row):
		try:
			session = self.session_manager.get_session()
			row = session.query(self.model).get(id_row)
			self.session_manager.close_session(session)
			if row is not None:
				session.delete(row)
				session.commit()
				return True
			return False
		except Exception as e:
			logger.error(f"Error deleting record: {str(e)}")
			return False
		finally:
			session.close()
			self.session_manager.close_session(session)

	def search(self, filters):
		"""
		Busca un registro
		"""
		try:
			session = self.session_manager.get_session()
			rows = session.query(self.model).filter_by(**filters).all()
			result = [dict(row.__dict__) for row in rows]
			self.session_manager.close_session(session)
			return result
		except Exception as e:
			logger.error(f"Error searching record: {str(e)}")
			return []
		finally:
			session.close()

	# def get_paginated(self, p_size=False, c_page=False):
	# 	try:
	# 		session = self.session_manager.get_session()
	# 		page_size = self.page_size if (p_size is False) else p_size
	# 		current_page = self.current_page if(c_page is False) else c_page
	# 		offset = (current_page - 1) * page_size
	# 		records = session.query(self.model).limit(page_size).offset(offset).all()
	# 		total_records = session.query(func.count(self.model.id)).scalar()
	# 		return (records, total_records)
	# 	finally:
	# 		session.close()

	# def get_paginated(self, p_size=False, c_page=False):
	# 	try:
	# 		session = self.session_manager.get_session()
	# 		page_size = self.page_size if (p_size is False) else p_size
	# 		current_page = self.current_page if (c_page is False) else c_page

	# 		offset = (current_page - 1) * page_size
	# 		records = session.query(self.model).limit(page_size).offset(offset).all()

	# 		columns = inspect(self.model).columns.keys()
	# 		# for column in columns:
	# 		# 	if self.model.__table__.columns[column].primary_key:
	# 		# 		primary_key_column = column
	# 		# 		break

	# 		total_records = session.query(func.count(getattr(self.model, columns[0]))).scalar()
	# 		self.session_manager.close_session(session)
	# 		return (records, total_records)
	# 	except Exception as e:
	# 		logger.error(e)
	# 	finally:
	# 		session.close()

	def get_paginated(self, p_size=False, c_page=False, search_term=None):
		try:
			session = self.session_manager.get_session()
			page_size = self.page_size if (p_size is False) else p_size
			current_page = self.current_page if (c_page is False) else c_page

			offset = (current_page - 1) * page_size

			# Obtener las columnas del modelo
			columns = inspect(self.model).columns.keys()
			total_records = session.query(func.count(getattr(self.model, columns[0]))).scalar()
			# Crear la consulta base
			query = session.query(self.model)
			filters = []
			# Agregar filtro de búsqueda si se proporciona un término de búsqueda
			if search_term:
				for column in columns:
					# Suponiendo que solo quieres buscar en columnas de tipo String
					if isinstance(getattr(self.model, column).type, String):
						filters.append(getattr(self.model, column).ilike(f"%{search_term}%"))
				query = query.filter(or_(*filters))

			# Limitar y offsetear la consulta
			records = query.limit(page_size).offset(offset).all()

			# Obtener el total de registros después de aplicar el filtro
			total_records = session.query(func.count(getattr(self.model, columns[0]))).filter(or_(*filters)).scalar()
			return (records, total_records)
		except Exception as e:
			logger.error(e)
		finally:
			session.close()
			self.session_manager.close_session(session)
