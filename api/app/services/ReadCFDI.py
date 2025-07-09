import zipfile
import os
import xml.etree.ElementTree as ET
# from ..models.CFDIDocument import CFDI_CRUD
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.CFDIDocument import CFDI_CRUD

class ReadCFDI:
	datos = {}

	def __init__(self, zip_path):
		self.zip_path = zip_path
		self.extracted_files = {}

	def unzip_file(self, pathextract, password=None):
		"""
		Abre el archivo ZIP y extrae los archivos XML.
		Si el archivo ZIP está protegido con contraseña, proporciona la contraseña.
		"""
		try:
			with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
				if password:
					zip_ref.extractall(path=pathextract, pwd=password)
				else:
					zip_ref.extractall(path=pathextract)

				# Lista todos los archivos extraídos
				self.extracted_files = {file: file for file in zip_ref.namelist()}

			return True

		except zipfile.BadZipfile:
			print(f"El archivo {self.zip_path} no es un ZIP válido o está corrupto.")
			return False
		except FileNotFoundError:
			print("El archivo ZIP no fue encontrado.")
			return False

	def list_xml_files(self, password=None):
		try:
			with zipfile.ZipFile(self.zip_path, 'r') as zip_object:
				return zip_object.namelist()
		except FileNotFoundError:
			print(f"El archivo {self.zip_path} no se encontró.")
		except zipfile.BadZipFile:
			print("El archivo no es un ZIP válido o está corrupto.")

	def read_cfdi(self, archivo_xml):
		"""Función principal para leer un CFDI 4.0."""
		self.raiz = self.cargar_cfdi(archivo_xml)
		self.extraer_datos_cfdi()

	def cargar_cfdi(self, archivo_xml):
		"""Carga el archivo XML del CFDI 4.0 y devuelve el elemento raíz."""
		try:
			tree = ET.parse(archivo_xml)
			return tree.getroot()
		except ET.ParseError as e:
			raise ValueError(f"Error al leer el XML: {e}")

	def extraer_datos_cfdi(self):
		"""Extrae información clave de un CFDI 4.0."""
		self.ns = {
			'cfdi': 'http://www.sat.gob.mx/cfd/4',
			'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
			'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
		}

	def getDataComprobante(self):
		# Obtener datos del comprobante
		self.datos['fecha'] = self.raiz.attrib.get('Fecha', '')
		self.datos['version'] = self.raiz.attrib.get('Version', '')
		self.datos['serie'] = self.raiz.attrib.get('Serie', '')	   # Nuevo: Serie del comprobante
		self.datos['folio'] = self.raiz.attrib.get('Folio', '')	   # Nuevo: Folio del comprobante
		self.datos['forma_pago'] = self.raiz.attrib.get('FormaPago', '')
		self.datos['metodo_pago'] = self.raiz.attrib.get('MetodoPago', '')
		self.datos['lugar_expedicion'] = self.raiz.attrib.get('LugarExpedicion', '')
		self.datos['total'] = self.raiz.attrib.get('Total', '')
		self.datos['subtotal'] = self.raiz.attrib.get('SubTotal', '')  # Nuevo: SubTotal
		self.datos['moneda'] = self.raiz.attrib.get('Moneda', '')	  # Si es necesario, pero no está en el XML proporcionado
		self.datos['exportacion'] = self.raiz.attrib.get('Exportacion', '')  # Nuevo: Exportación
		self.datos['tipo_comprobante'] = self.raiz.attrib.get('TipoDeComprobante', '')

	def getDataEmisor(self):
		# Obtener datos del emisor
		emisor = self.raiz.find('cfdi:Emisor', self.ns)
		if emisor is not None:
			self.datos['rfc_emisor'] = emisor.attrib.get('Rfc', '')
			self.datos['nombre_emisor'] = emisor.attrib.get('Nombre', '')
			self.datos['regimen_fiscal_emisor'] = emisor.attrib.get('RegimenFiscal', '')  # Nuevo

	def getDataReceptor(self):
		# Obtener datos del receptor
		receptor = self.raiz.find('cfdi:Receptor', self.ns)
		if receptor is not None:
			self.datos['rfc_receptor'] = receptor.attrib.get('Rfc', '')
			self.datos['nombre_receptor'] = receptor.attrib.get('Nombre', '')
			self.datos['domicilio_fiscal_receptor'] = receptor.attrib.get('DomicilioFiscalReceptor', '')  # Nuevo
			self.datos['regimen_fiscal_receptor'] = receptor.attrib.get('RegimenFiscalReceptor', '')  # Nuevo
			self.datos['uso_cfdi'] = receptor.attrib.get('UsoCFDI', '')

	def getDetailConceptos(self):
		# Obtener detalles de los conceptos
		conceptos = self.raiz.findall('cfdi:Conceptos/cfdi:Concepto', self.ns)
		if conceptos:
			detalle_conceptos = []
			for concepto in conceptos:
				item = {
					'clave_prod_serv': concepto.attrib.get('ClaveProdServ', ''),
					'cantidad': concepto.attrib.get('Cantidad', ''),
					'clave_unidad': concepto.attrib.get('ClaveUnidad', ''),
					'unidad': concepto.attrib.get('Unidad', ''),
					'descripcion': concepto.findtext('cfdi:Descripcion'),
					'valor_unitario': concepto.attrib.get('ValorUnitario', ''),
					'importe_total': concepto.attrib.get('ImporteTotal', '')
				}
				detalle_conceptos.append(item)
			self.datos['detalle_conceptos'] = detalle_conceptos

	def getTimbreFiscal(self):
		# Obtener timbre fiscal digital
		timbre_fiscal = self.raiz.find('cfdi:Complemento/tfd:TimbreFiscalDigital', self.ns)
		if timbre_fiscal is not None:
			self.datos['uuid'] = timbre_fiscal.attrib.get('UUID', '')
			self.datos['fecha_timbrado'] = timbre_fiscal.attrib.get('FechaTimbrado', '')
			self.datos['sello_cfd'] = timbre_fiscal.attrib.get('SelloCFD', '')
			self.datos['rfc_prov_certif'] = timbre_fiscal.attrib.get('RfcProvCertif', '')

if __name__ == "__main__":
	path_actually = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
	# Crear el directorio de destino si no existe
	path_destiny = f"{path_actually}/packages_cfdi/"
	os.makedirs(path_destiny, exist_ok=True)
	file = f"{path_actually}/packages_cfdi/2A599509-4912-4E91-85B1-B4547E862269_01.zip"
	# Instancia de la clase
	extractor = ReadCFDI(file)

	filesinzip = extractor.list_xml_files()
	extractor.unzip_file(path_destiny)

	for filex in filesinzip:
		xml_file = path_destiny+filex
		print(xml_file)
		extractor.read_cfdi(xml_file)
		extractor.getTimbreFiscal()
		extractor.getDataComprobante()
		extractor.getDataEmisor()
		extractor.getDataReceptor()
		print(extractor.datos)

		crud = CFDI_CRUD()

		# Ejemplo de creación
		new_cfdi = {
			"version": extractor.datos['version'],
			"series": extractor.datos['serie'],
			"dates": extractor.datos['fecha'],
			"form_of_payment": extractor.datos['forma_pago'],
			"subtotal": extractor.datos['subtotal'],
			"currency": extractor.datos['moneda'],
			"total": extractor.datos['total'],
			"type_of_fiscal_document": extractor.datos['tipo_comprobante'],
			"export": extractor.datos['exportacion'],
			"payment_method": extractor.datos['metodo_pago'],
			"place_of_issuance": extractor.datos['lugar_expedicion'],
			"uuid": extractor.datos['uuid'],
			"company_id": 2,
			"type_of_relationship": "",
			"rfc_of_the_issuer": extractor.datos['rfc_emisor'],
			"name_of_the_issuer": extractor.datos['nombre_emisor'],
			"tax_regime_of_the_issuer": extractor.datos['regimen_fiscal_emisor'],
			"rfc_of_the_receiver": extractor.datos['rfc_receptor'],
			"name_of_the_receiver": extractor.datos['nombre_receptor'],
			"tax_address_of_the_receiver": extractor.datos['domicilio_fiscal_receptor'],
			"tax_regime_of_the_receiver": extractor.datos['regimen_fiscal_receptor'],
			"use_of_cfdi": extractor.datos['uso_cfdi'],
			"xml_path": f"{xml_file}"
		}

		print("Creando nuevo comprobante...")
		success = crud.create_cfdi(**new_cfdi)
		if success:
			print("Comprobante creado exitosamente.")

		# Leer un archivo XML específico (si existe)
		# xml_filename = "nombre_del_archivo.xml"

		# if xml_filename in extractor.extracted_files:
		# 	print(f"\n Leyendo el archivo {xml_filename}...")
		# 	root = extractor.read_xml_file(xml_filename)
		# 	if root is not None:
		# 		print(" Contenido del XML:")
		# 		# Aquí puedes procesar el árbol XML según tus necesidades
		# 		for child in root:
		# 			print(f" - {child.tag}: {child.text}")
		# else:
		# 	print(f"El archivo {xml_filename} no se encontró en el ZIP.")
