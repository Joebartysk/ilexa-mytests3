
import csv
import os
import sys
import psycopg2
from psycopg2 import pool
import json,typing
from pathlib import Path
import argparse
from starlette.responses import Response
from dotenv import load_dotenv

class export_CSV():
	def __init__(self,filename,nameSchema,nameTable):
		self.filename = filename
		self.nameSchema = nameSchema
		self.nameTable = nameTable

	def main(self):
		load_dotenv()
		db_config = {
			"user": os.getenv("DB_USER"),
			"password": os.getenv("DB_PASS"),
			"host": os.getenv("DB_HOST"),
			"port": os.getenv("DB_PORT"),
			"database": os.getenv("DB_NAME"),
		}
		try:
			threaded_pool = pool.ThreadedConnectionPool(
				minconn=1,
				maxconn=10,
				#options="-c search_path=cfdi_system,public",
				**db_config
			)
			if threaded_pool:
				myconn = 'ok'
		except (Exception, psycopg2.Error) as error:
			print("Error while creating connection pool", error)

		conn = threaded_pool.getconn()
		curschema = conn.cursor()
		curschema.execute(f"SET search_path TO {self.nameSchema}")
		curschema.close()

		sqlSelect = 'SELECT * FROM "'+self.nameTable+'";'

		try:
			if conn:
				print(self.filename)
				cur = conn.cursor()
				cur.execute(sqlSelect)
				results = cur.fetchall()

				headers = [i[0] for i in cur.description]
				saveroute = str(Path(__file__).parent.parent.parent) + str('/static/'+self.filename+'.csv')
				csvFile = csv.writer(open(saveroute, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

				csvFile.writerow(headers)
				csvFile.writerows(results)

				cur.close()
				return saveroute
		except(Exception) as error:
			print("Hubo un error al crear CSV", error)
		finally:
			conn.close()

