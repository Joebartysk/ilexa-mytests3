# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd
import chardet
import subprocess
import re
import warnings
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.DBConnect import DatabaseConfig, SessionManager

myfile = "/home/joebart/Documentos/Proyecto_SAT/api_/app/models/estados_de_cuenta/bbva.txt"#ISO-8859-1
#myfile = "/home/joebart/Documentos/Proyecto_SAT/api_/app/models/estados_de_cuenta/hsbc.CSV"#ascii
##myfile = "/home/joebart/Documentos/Proyecto_SAT/api_/app/models/estados_de_cuenta/Clara.csv"#utf-8
##myfile = "/home/joebart/Documentos/Proyecto_SAT/api_/app/models/estados_de_cuenta/inbursa.xlsx"
##myfile = "/home/joebart/Documentos/Proyecto_SAT/api_/app/models/estados_de_cuenta/Monex.xls"#ISO-8859-1

class BankAccount:

	def __init__(self, db_config):
		self.db_config = db_config
		self.session_manager = SessionManager(db_config)
		self.engine = self.session_manager.engine
		#print("hola")

	def type_file(self, path_file, content, encoding):
		if re.search(r"Concepto / Referencia",content, re.IGNORECASE):#BBVA
			self.read_file_bbva(path_file, 'utf-8')
		elif re.search(r"ACCOUNTNO",content, re.IGNORECASE):#HSBC
			self.read_file_hsbc(path_file,encoding)
		elif re.search(r"Alias de la Tarjeta",content, re.IGNORECASE):#CLARA
			self.read_file_clara(path_file,encoding)
		elif re.search(r"PK\\x03",content, re.IGNORECASE):#INBURSA
			self.read_file_inbursa(path_file,encoding)
		elif re.search(r"Movimientos del Contrato",content, re.IGNORECASE):#Monex
			self.read_file_monex(path_file,encoding)

	def read_file_bbva(self, filename, encoding):
		try:
			df = pd.read_csv(filename, delimiter="\t", index_col=False, encoding=encoding)
			dff = df.rename(columns={'Día': 'movement_date', 'Concepto / Referencia': 'concept_reference','cargo': 'charge','Abono': 'payment','Saldo': 'balance'})
			dff.fillna(0, inplace=True)
			#df.fillna('')
			with self.engine.connect() as connection:
				dff.to_sql("bbva", schema='cfdi_system', con=connection, if_exists='replace', index=None)
			return True
		except Exception as e:
			print(f"Error al leer el archivo CSV: {str(e)}")
			return None

	def read_file_hsbc(self, filename, encoding):
		try:
			df = pd.read_csv(filename, delimiter=",", index_col=False, encoding=encoding)
			#dff = df.rename(columns={'Día': 'movement_date', 'Concepto / Referencia': 'concept_reference','cargo': 'charge','Abono': 'payment','Saldo': 'balance'})
			df.fillna(0, inplace=True)
			#print(df)
			#exit()
			with self.engine.connect() as connection:
				df.to_sql("hsbc", schema='cfdi_system', con=connection, if_exists='replace', index=None)
			return True
		except Exception as e:
			print(f"Error al leer el archivo CSV: {str(e)}")
			return None

	def read_file_clara(self, filename, encoding):
		try:
			df = pd.read_csv(filename, delimiter=",", index_col=False, encoding=encoding)
			dff = df.rename(columns={'n':'consecutive','Fecha de Transacción':'transaction_date','Estado de Cuenta':'account_statement','Transacción':'transaction','Monto original':'original_amount','Moneda original':'original_currency','Monto en MXN':'mxn_amount','Tarjeta':'card','Alias de la Tarjeta':'card_alias','Estado':'status','Estado de aprobación':'approval_status','Nombre de Aprobador':'approver_name','Nota de Aprobador':'approver_note','Código de autorización':'authorization_code','Categoría de Compra':'purchase_category','Factura Electrónica':'electronic_invoice','Factura auto-vinculada':'Factura auto-vinculada','Archivos Factura Electrónica':'auto_linked_invoice','Anexos':'attached','Archivos Anexos':'attached_files','Folio Fiscal':'Folio Fiscal','Titular':'holder','Grupos':'groups','Ubicación':'location','Etiquetas':'labels','Comentario':'comment'})
			dff.fillna(0, inplace=True)
			with self.engine.connect() as connection:
				dff.to_sql("clara", schema='cfdi_system', con=connection, if_exists='replace', index=None)
			return True
		except Exception as e:
			print(f"Error al leer el archivo CSV: {str(e)}")
			return None
		#df = pd.read_csv(myfile, sep="\t", encoding=encoding)

	def read_file_inbursa(self, filename, encoding):
		try:
			with warnings.catch_warnings():
				warnings.simplefilter("ignore")
				df = pd.read_excel(myfile, engine="openpyxl", index_col=False, skiprows=[0,1,2], header=0)
				dff = df.rename(columns={'Fecha':'movement_date','Referencia':'reference','Referencia Ext.':'ext_reference','Referencia Leyenda':'legend_reference','Referencia Numérica':'numeric_reference','Concepto':'concept','Movimiento':'motion','Cargo':'charge','Abono':'payment','Saldo':'balance','Ordenante':'payer','RFC Ordenante':'rfc_payer'})
				dff.fillna(0, inplace=True)
			with self.engine.connect() as connection:
				dff.to_sql("inbursa", schema='cfdi_system', con=connection, if_exists='replace', index=None)
			return True
		except Exception as e:
			print(f"Error al leer el archivo CSV: {str(e)}")
			return None

	def read_file_monex(self, filename, encoding):
		try:
			df = pd.read_csv(filename, delimiter="\t", index_col=False, encoding=encoding, skiprows=[0], header=0)
			dff = df.rename(columns={'Divisa': 'foreign_exchange','Fecha Operación': 'operation_date','Fecha de Liquidación': 'settlement_date','Descripción': 'description','Emisora Serie': 'serial_sattion','Referencia': 'reference','Cantidad': 'quantity','Plazo': 'term','Tasa Rend Prima Unitaria': 'unit_premium_yield_rate','Precio Strike': 'strike_price','Importe': 'amount'})
			dff.fillna(0, inplace=True)
			#df.fillna('')
			with self.engine.connect() as connection:
				dff.to_sql("monex", schema='cfdi_system', con=connection, if_exists='replace', index=None)
			return True
		except Exception as e:
			print(f"Error al leer el archivo CSV: {str(e)}")
			return None

	def detect_file_encoding(self, filename):
		with open(filename,'rb') as file:
			raw_data  = file.read()
			result = chardet.detect(raw_data)
			return result["encoding"]

def main():
	db_config = DatabaseConfig()
	loader = BankAccount(db_config)
	type_encode = loader.detect_file_encoding(myfile)
	setcommand = 'head -1 '+ myfile
	output = subprocess.check_output(setcommand, shell=True, encoding=type_encode)
	basename = os.path.basename(myfile)
	basename = basename.split('.')
	loader.type_file(myfile,str(output),type_encode)	


if __name__ == "__main__":
	main()
