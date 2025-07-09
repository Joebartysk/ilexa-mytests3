from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime

class ValidateCer:
	def get_certificate_info(cert_path):
		try:
			with open(cert_path, "rb") as cert_file:
				cert_data = cert_file.read()

			# Cargar el certificado
			cert = x509.load_der_x509_certificate(cert_data, default_backend())

			# Obtener la fecha de expiración
			expiration_date = cert.not_valid_after_utc
			return expiration_date
		except Exception as e:
			print(f"Error al leer el archivo .cer: {e}")
			return None
