# -*- coding: utf-8 -*-

import pandas as pd
import requests
import sys
import os
import subprocess
import time

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager

Base = declarative_base()

class Sentences(Base):
	__tablename__ = "sentences"
	__table_args__ = {"schema": "cfdi_system"}

	rfc = Column(String, primary_key=True, nullable=True)
	company_name = Column(String, nullable=True)
	type_person = Column(String, nullable=True)
	supposed = Column(String, nullable=True)
	dates_of_firts_publication = Column(String, nullable=True)
	federal_entity = Column(String, nullable=True)

#RFC,RAZÓN SOCIAL,TIPO PERSONA,SUPUESTO,FECHAS DE PRIMERA PUBLICACION,ENTIDAD FEDERATIVA
#45KB
class LoadSentences:
	def __init__(self, db_config):
		self.db_config = db_config
		self.session_manager = SessionManager(db_config)
		self.engine = self.session_manager.engine

	def download_csv_from_url(self, url, filename='data.csv'):
		"""Descargar archivo CSV desde una URL"""
		try:
			response = requests.get(url)
			if response.status_code == 200:
				with open(filename, 'wb') as f:
					f.write(response.content)
					newname = "data2.csv"

					setcommand = 'iconv -f CP1250 -t UTF-8 <'+filename+' >'+newname
					subprocess.Popen(setcommand, shell=True)

					setcommand2 = 'mv '+ newname + ' '+ filename
					subprocess.Popen(setcommand2, shell=True)
					time.sleep(2)

				return True
			else:
				print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
				return False
		except Exception as e:
			print(f"Ocurrió un error al descargar el archivo: {str(e)}")
			return False

	def read_csv(self, filename):
		"""Leer el archivo CSV en un DataFrame"""
		try:
			df = pd.read_csv(filename, header=0, index_col=False, delimiter=',')
			df = df.rename(columns={
				'RFC': 'rfc',
				'RAZÓN SOCIAL': 'company_name',
				'TIPO PERSONA': 'type_person',
				'SUPUESTO': 'supposed',
				'FECHAS DE PRIMERA PUBLICACION': 'dates_of_firts_publication',
				'ENTIDAD FEDERATIVA': 'federal_entity'
			})
			df = df.fillna('')
			return df
		except Exception as e:
			print(f"Error al leer el archivo CSV: {str(e)}")
			return None

	def create_table_if_not_exists(self, df, table_name, file):
		"""Crear tabla en la base de datos si no existe"""
		try:
			# Eliminar el archivo temporal después de usarlo
			if os.path.exists(file):
				os.remove(file)

			with self.engine.connect() as connection:
				# Usar pandas para crear la sentencia SQL
				df.head(0).to_sql(table_name, connection, if_exists='replace', index=False)
			return True
		except Exception as e:
			print(f"Error al crear tabla: {str(e)}")
			return False

	def load_csv_to_db(self, df, table_name):
		"""Cargar DataFrame a la base de datos"""
		try:
			# Eliminar el archivo temporal después de usarlo
			#if os.path.exists('data.csv'):
			#	os.remove('data.csv')

			with self.engine.connect() as connection:

				# Usar la copia directa para insertar los datos
				##df = df.drop(df.columns[0], axis=1)
				#print(df)
				df.to_sql(table_name, schema='cfdi_system', con=connection, if_exists='replace', index=None)
			return True
		except Exception as e:
			print(f"Error al cargar los datos: {str(e)}")
			return False

	def close_connection(self):
		"""Cerrar la conexión a la base de datos"""
		self.session_manager.close_session()

# Ejemplo de uso:

def main():
	db_config = DatabaseConfig()

	loader = LoadSentences(db_config)

	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	file_out = f"{path}/../tmp/data.csv"

	# Descargar el archivo CSV
	success_download = loader.download_csv_from_url("http://omawww.sat.gob.mx/cifras_sat/Documents/Sentencias.csv", file_out)
	if not success_download:
		return

	# Leer el archivo CSV
	df = loader.read_csv(file_out)
	if df is None:
		return

	# Configurar el nombre de la tabla
	table_name = 'sentences'

	## Crear la tabla si no existe
	#success_create_table = loader.create_table_if_not_exists(df, table_name)
	#if not success_create_table:
		#return

	# Cargar los datos en la base de datos
	success_load = loader.load_csv_to_db(df, table_name)
	if success_load:
		print("Datos cargados exitosamente!")
		os.remove(file_out)

	# Cerrar la conexión
	#loader.close_connection()

if __name__ == "__main__":
	main()
