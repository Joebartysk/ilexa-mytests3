import psycopg2
from psycopg2 import pool
#import cgi
from time import *
import datetime
import sys
import os.path
from pathlib import Path
import xlsxwriter
from xlsxwriter.workbook import Workbook
import json
import random
from dotenv import load_dotenv

#print ("Access-Control-Allow-Origin: *\r\n")

class ExportXLSX():
	def __init__(self,filename,nameSchema,nameTable):
		self.filename = filename
		self.nameSche = nameSchema
		self.nameTab = nameTable

	def main(self):
		#print(self.filename)
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
				#print("Connection pool created successfully")
		except (Exception, psycopg2.Error) as error:
			print("Error while creating connection pool", error)

		schema = self.nameSche
		nameTab =  self.nameTab
		nameFile = self.filename

		conn = threaded_pool.getconn()
		setsql = "SELECT c.table_schema, st.relname as TableName, c.column_name, pgd.description from pg_catalog.pg_statio_all_tables as st INNER JOIN information_schema.columns c on c.table_schema = st.schemaname AND c.table_name = st.relname LEFT JOIN pg_catalog.pg_description pgd on pgd.objoid=st.relid AND pgd.objsubid=c.ordinal_position WHERE st.relname like '"+nameTab+"';"

		if conn:
			cur = conn.cursor()
			cur.execute(setsql)
			esults = cur.fetchall()
			mytitles = ''
			for r, row in enumerate( esults, start = int(1) ):
				#print(r)
				for c, col in enumerate(row, start = int(1)):
					#print(c)
					if c == 3:
						getCam = col
					if c == 4:
						getTit = col
				mytitles += ' "'+getCam +'" AS '+ '"'+getTit+'",'
			mytitles = mytitles[:-1]
			cur.close()
			#print(mytitles)

		# Example usage
		query = 'SELECT '+mytitles+' FROM "'+nameTab+'";'

		saveroute = str(Path(__file__).parent.parent.parent) + '/static/'+nameFile+'.xlsx'
		
		workbook = xlsxwriter.Workbook(saveroute, {'strings_to_numbers': True})
		workbook.set_properties({'author': 'ILEXA'})
		formater = workbook.add_format({'border':1,'bold': 1})
		filaAzulclaro = workbook.add_format({'bg_color':'#DCDCDC','border':1})
		filaBlanca = workbook.add_format({'border':1})
		filaAzulclarofloat = workbook.add_format({'bg_color':'#DCDCDC','border':1,'num_format': '#,##0.00'})
		filaAzulclaroint = workbook.add_format({'bg_color':'#DCDCDC','border':1,'num_format': '#,##0'})
		filaBlancafloat = workbook.add_format({'border':1,'num_format': '#,##0.00'})
		filaBlancaint = workbook.add_format({'border':1,'num_format': '#,##0'})
		filaAzulclaroDate = workbook.add_format({'bg_color':'#DCDCDC','border':1,'num_format': 'yyyy-mm-dd'})
		filaBlancaDate = workbook.add_format({'border':1,'num_format': 'yyyy-mm-dd'})
		headers = workbook.add_format({'bold': True,'border':1,'align': 'center','bg_color':'#3D59AB','color': '#FFFFFF'})

		conn = None
		try:
			conn = threaded_pool.getconn()
			curschema = conn.cursor()
			curschema.execute(f"SET search_path TO {schema}")
			curschema.close()
			if conn:
				cur = conn.cursor()
				cur.execute(query)
				
				x = datetime.datetime.now()
				fechact = str(x.year)+'-'+str('%02d'%x.month)+'-'+str(x.day)
				worksheet = workbook.add_worksheet("Detalle")
				colors = ["red", "green", "yellow", "pink", "orange", "blue", "brown", "purple", "magenta", "cyan"]
				getColor = random.choice(colors)
				worksheet.set_tab_color(getColor)
				resumen = workbook.add_format({'bg_color':'#0070c0','font_color':'#FFFFFF','font_size':11,'text_wrap': True,'align':'center','border':1,'locked': 1})
				titulo = workbook.add_format({'bold': True,'font_size':18,'align': 'center','border':1,'locked': 1})
				datos_tit = workbook.add_format({'bold': True,'font_size':10,'text_wrap': True,'align':'center','border':1,'locked': 1})
				footer1 = '&CInformacion confidencial. La copia, revision, uso, revelacion y/o distribucion de dicha informacion sin la autorizacion por escrito de ILEXA esta prohibida. '
				footer2 = '&R&P'
				worksheet.set_footer(footer1 + footer2,{'font_size':9,'align':'center','text_wrap': True})
				worksheet.set_margins(left=0.3, right=0.3, top=0.9, bottom=0.8)
				worksheet.center_horizontally()
				worksheet.set_landscape()
				total_filas = str(cur.rowcount)
				total_columnas = str(len(cur.description))
				#print( total_filas )
				startdata = 1
				startrow = 0
				#results = cur.fetchall()
				for r, row in enumerate( cur.fetchall(), start = int(startdata) ):
					#print ( cursor.description )
					for c, col in enumerate(row, start = int(startrow)):
						tittles = cur.description
						if (c == 0 and r == 1): 
							for tittle in range(0,len(tittles)):
								worksheet.write(0,tittle,tittles[tittle][0],headers)
								myheaderwidth = len(str(tittles[tittle][0]))+10
								nCols = len(cur.description)
								ancho = [30] * int(nCols)
								worksheet.set_column(tittle,tittle,myheaderwidth)#ancho[tittle]
							genWidth = len(str(col))+2
							if myheaderwidth > genWidth:
								colWidth = myheaderwidth
							else:
								colWidth = genWidth
							#print ( colWidth )
						if r%2==0:
							if ( isinstance(col, datetime.date) ):
								#col = datetime.datetime.strptime(col, '%Y-%m-%d')
								formater=filaAzulclaroDate
							elif ( isinstance(col, (float, complex)) ):
								formater=filaAzulclarofloat
							elif ( isinstance(col, (int)) ):
								formater=filaAzulclaroint
							else :
								formater=filaAzulclaro
						else:
							if ( isinstance(col, datetime.date) ):
								formater=filaBlancaDate
							elif ( isinstance(col, (float, complex)) ):
								formater=filaBlancafloat
							elif ( isinstance(col, (int)) ):
								formater=filaBlancaint
							else :
								formater=filaBlanca
						#print(type(col))
						worksheet.write(r, c, col, formater)
				cur.close()
				workbook.close()
				return saveroute
		except (Exception, psycopg2.Error) as error:
			print("Error while executing query", error)
		finally:
			if conn:
				threaded_pool.putconn(conn)
