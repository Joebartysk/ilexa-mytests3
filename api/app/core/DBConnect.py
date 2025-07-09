from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

class DatabaseConfig:
	DB_USER = "postgres.kwfieujmxyojnozdgrwk"
	DB_PASSWORD = "LsrLBYib7GtxhLCk"
	DB_HOST = "aws-0-us-west-1.pooler.supabase.com"
	DB_PORT = 6543
	DB_NAME = "postgres"

	@classmethod
	def get_connection_string(cls):
		return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

class SessionManager:
	def __init__(self, db_config):
		# self.engine = create_engine(db_config.get_connection_string())
		self.engine = create_engine(
			db_config.get_connection_string(),
			pool_size=20,
			max_overflow=0,
			# pool_size=20,  # Número máximo de conexiones en el pool
			# max_overflow=30,  # Cuántas conexiones adicionales se permiten si hay demanda alta
			pool_recycle=3600,  # Reciclar conexiones después de un tiempo (segundos), -1 para desactivar
			echo=False  # Deshabilitar el eco de SQL (útil para depuración)
		)

	def get_session(self):
		session = Session(self.engine)
		return session

	def close_session(self, session):
		session.close()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from sqlalchemy.pool import QueuePool
# import time

# class DatabaseConfig:
# 	DB_USER = "postgres.kwfieujmxyojnozdgrwk"
# 	DB_PASSWORD = "LsrLBYib7GtxhLCk"
# 	DB_HOST = "aws-0-us-west-1.pooler.supabase.com"
# 	DB_PORT = 5432
# 	DB_NAME = "postgres"

# 	@classmethod
# 	def get_connection_string(cls):
# 		return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

# class SessionManager:
# 	def __init__(self, db_config):
# 		self.engine = create_engine(
# 			db_config.get_connection_string(),
# 			pool_size=20,
# 			max_overflow=10,
# 			echo=False,
# 		)

# 	def get_session(self):
# 		session = None
# 		retries = 5  # Número de intentos
# 		for _ in range(retries):
# 			try:
# 				session = Session(self.engine)
# 				break
# 			except Exception as e:
# 				print(f"Error al obtener conexión: {str(e)}")
# 				time.sleep(1)  # Esperar antes de reintentar
# 		return session

# 	def close_session(self, session):
# 		if session is not None:
# 			session.close()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from sqlalchemy.pool import NullPool

# class DatabaseConfig:
# 	DB_USER = "postgres.kwfieujmxyojnozdgrwk"
# 	DB_PASSWORD = "LsrLBYib7GtxhLCk"
# 	DB_HOST = "aws-0-us-west-1.pooler.supabase.com"
# 	DB_PORT = 5432
# 	DB_NAME = "postgres"

# 	@classmethod
# 	def get_connection_string(cls):
# 		return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

# class SessionManager:
# 	def __init__(self, db_config):
# 		# Configurar un pool de conexiones con reciclado automático
# 		self.engine = create_engine(
# 			db_config.get_connection_string(),
# 			pool_size=20,
# 			max_overflow=10,
# 			pool_recycle=3600,  # Reciclar conexiones cada hora (3600 segundos)
# 			echo=False,
# 		)

# 	def get_session(self):
# 		session = Session(self.engine)
# 		return session

# 	def close_session(self, session):
# 		if session is not None:
# 			session.close()
