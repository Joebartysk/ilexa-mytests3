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

class SATBlacklist(Base):
	__tablename__ = "sat_blacklist"
	__table_args__ = {"schema": "cfdi_system"}

	id = Column(Integer, primary_key=True, nullable=True)
	rfc = Column(String, nullable=True)
	taxpayer_name = Column(String, nullable=True)
	taxpayer_situation = Column(String, nullable=True)
	sat_presumption_number_date = Column(String, nullable=True)
	presumptive_sat_page_publication = Column(String, nullable=True)
	dof_presumption_number_date = Column(String, nullable=True)
	alleged_dof_publication = Column(String, nullable=True)
	taxpayers_who_distorted_sat = Column(String, nullable=True)
	sat_page_publication_distorted = Column(String, nullable=True)
	taxpayers_who_distorted_dof = Column(String, nullable=True)
	distorted_dof_publication = Column(String, nullable=True)
	definitive_sat_document = Column(String, nullable=True)
	final_sat_page_publication = Column(String, nullable=True)
	definitive_dof_document = Column(String, nullable=True)
	final_dof_publication = Column(String, nullable=True)
	favorable_ruling_sat = Column(String, nullable=True)
	sat_page_publication_favorable_ruling = Column(String, nullable=True)
	favorable_ruling_dof = Column(String, nullable=True)
	dof_publication_favorable_ruling = Column(String, nullable=True)

class LoadSATBlackList:
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
			df = pd.read_csv(filename, header=0, index_col=False, delimiter=',', skiprows=2)
			df = df.rename(columns={
				'No': 'id',
				'RFC': 'rfc',
				'Nombre del Contribuyente': 'taxpayer_name',
				'Situación del contribuyente': 'taxpayer_situation',
				'Número y fecha de oficio global de presunción SAT': 'sat_presumption_number_date',
				'Publicación página SAT presuntos': 'presumptive_sat_page_publication',
				'Número y fecha de oficio global de presunción DOF': 'dof_presumption_number_date',
				'Publicación DOF presuntos': 'alleged_dof_publication',
				'Número y fecha de oficio global de contribuyentes que desvirtuaron SAT': 'taxpayers_who_distorted_sat',
				'Publicación página SAT desvirtuados': 'sat_page_publication_distorted',
				'Número y fecha de oficio global de contribuyentes que desvirtuaron DOF': 'taxpayers_who_distorted_dof',
				'Publicación DOF desvirtuados': 'distorted_dof_publication',
				'Número y fecha de oficio global de definitivos SAT': 'definitive_sat_document',
				'Publicación página SAT definitivos': 'final_sat_page_publication',
				'Número y fecha de oficio global de definitivos DOF': 'definitive_dof_document',
				'Publicación DOF definitivos': 'final_dof_publication',
				'Número y fecha de oficio global de sentencia favorable SAT': 'favorable_ruling_sat',
				'Publicación página SAT sentencia favorable': 'sat_page_publication_favorable_ruling',
				'Número y fecha de oficio global de sentencia favorable DOF': 'favorable_ruling_dof',
				'Publicación DOF sentencia favorable': 'dof_publication_favorable_ruling'
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
	loader = LoadSATBlackList(db_config)

	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	file_out = f"{path}/../tmp/data.csv"

	# Descargar el archivo CSV
	success_download = loader.download_csv_from_url("http://omawww.sat.gob.mx/cifras_sat/Documents/Listado_Completo_69-B.csv", file_out)
	if not success_download:
		return

	# Leer el archivo CSV
	df = loader.read_csv(file_out)
	if df is None:
		return

	# Configurar el nombre de la tabla
	table_name = 'sat_blacklist'

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
