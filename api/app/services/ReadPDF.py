# app/services/ReadPDF.py
import PyPDF2
import camelot
import pandas as pd
import re
import pdfplumber

class ReadPDF:

	def get_number_of_pages(self, pdf_path):
		with open(pdf_path, 'rb') as f:
			reader = PyPDF2.PdfReader(f)
			return len(reader.pages)

	def extract_tables_by_page(self, pdf_path):
		try:
			num_pages = self.get_number_of_pages(pdf_path)
			tables_list = []

			for page in range(1, num_pages + 1):
				print(f"Procesando página {page} de {num_pages}...")
				# tables = camelot.read_pdf(pdf_path, flavor='stream', pages=str(page))
				tables = camelot.read_pdf(pdf_path,flavor='stream', suppress_stdout=True, pages=str(page))

				if not tables:
					print(f"No se encontraron tablas en la página {page}.")
					continue

				for table in tables:
					try:
						tables_list.append(table.df)
					except Exception as e:
						print(f"Error al procesar tabla en página {page}: {str(e)}")

			return tables_list
		except Exception as e:
			print(f"Error general al leer el archivo PDF: {str(e)}")
			return []

	def extract_by_plumber(sef, pdf_path):
		tables_list = []

		# Leer el PDF y extraer texto
		text = ""
		with pdfplumber.open(pdf_path) as pdf:
			for page in pdf.pages:
				text += page.extract_text() + "\n"

		# Limpiar el texto
		# Detectar líneas que parecen encabezados de tablera
		header_pattern = r'(?<=\n)\s*([-=]+)\s*(\w+)'
		headers = re.findall(header_pattern, text)

		# Detectar filas de la tabla
		row_pattern = r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'
		rows = re.findall(row_pattern, text)

		print(headers)
		print(rows)



if __name__ == "__main__":
	pdf_path = '/home/gothic/Descargas/IAS 6034 0125.pdf'
	obj = ReadPDF()

	# tables = obj.extract_by_plumber(pdf_path)
	# print(tables)

	tables = obj.extract_tables_by_page(pdf_path)

	filas = []
	pattern = r"\bFECHA .*REFERENCIA .*CARGOS .*ABONOS .*SALDO\b"

	for index, table_df in enumerate(tables):
		print(f"\nTabla {index + 1}:")
		table_mv = table_df.to_string()

		# print(table_mv)

		# match = re.search(pattern, table_mv, flags=re.IGNORECASE)
		if re.search(pattern, table_mv, flags=re.IGNORECASE):


			print(table_mv)

			df_tabla = table_df

			for fila in df_tabla.index:

				print("UNA LONGITUD")

				print((df_tabla.columns.stop))
				fecha = df_tabla.iloc[fila, 0]  # Suponiendo que la primera columna es "Fecha"
				referencia = df_tabla.iloc[fila, 1]  # Referencia o descripción

				descripcion = df_tabla.iloc[fila, 2]  # Descripción del movimiento
				concepto = df_tabla.iloc[fila, 3]  # Monto de débito (si es negativo)
				cargo = df_tabla.iloc[fila, 4]  # Monto de cargo
				abono = df_tabla.iloc[fila, 5]

				if int(df_tabla.columns.stop) < 7:
					saldo = ""
				else:
					saldo = df_tabla.iloc[fila, 6]

				if fecha != "FECHA" and fecha != "":
					filas.append({
						"fecha": fecha,
						"referencia": referencia,
						"descripcion": descripcion,
						"concepto": concepto,
						"cargo": cargo,
						"abono": abono,
						"saldo": saldo
					})

				# if df_tabla.iloc[fila, 6]



		else:
			print("Ninguna de las palabras clave fue encontrada.")

	print(filas)


	# columnas_a_extraer = [0]

	# for index, table_df in enumerate(tables):
	# 	print(f"\nTabla {index + 1}:")
	# 	# Seleccionar solo las columnas por índice
	# 	df_filtrado = table_df.iloc[:, columnas_a_extraer]
	# 	print(df_filtrado.to_string())

