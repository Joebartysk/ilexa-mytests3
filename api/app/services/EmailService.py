# app/services/EmailService.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import socket

from app.core.config import Settings
from app.core.logger_config import setup_logger

logger = setup_logger()

class EmailSendFailed(Exception):
	def __init__(self, message, status_code=500):
		super().__init__(message)
		self.status_code = status_code

class TemplateRenderError(Exception):
	def __init__(self, message, status_code=500):
		super().__init__(message)
		self.status_code = status_code

class EmailService():
	def __init__(self, timeout=10):
		self.settings = Settings()
		self.smtp_server = self.settings.SMTP_SERVER
		self.smtp_port = self.settings.SMTP_PORT
		self.email_username = self.settings.EMAIL_USERNAME
		self.email_password = self.settings.EMAIL_PASSWORD
		self.timeout = timeout
		logger.info(f"EmailService inicializado con timeout: {timeout} segundos")

	def send_email(self, to: str, subject: str, body_text: str, body_html: str) -> None:
		# Crear el mensaje de correo electrónico
		msg = MIMEMultipart('alternative')
		msg['From'] = self.email_username
		msg['To'] = to
		msg['Subject'] = subject

		# Adjuntar el cuerpo del correo en formato texto y HTML
		part_text = MIMEText(body_text, 'plain')
		part_html = MIMEText(body_html, 'html')

		msg.attach(part_text)
		msg.attach(part_html)

		# Conectar al servidor SMTP y enviar el correo
		try:
			logger.info(f"Enviando correo a {to} con asunto '{subject}'")
			server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
			server.login(self.email_username, self.email_password)
			server.sendmail(self.email_username, to, msg.as_string())
		except socket.timeout:
			logger.error(f"Error: Se ha agotado el tiempo de espera al enviar el correo (timeout={self.timeout} segundos)")
			raise EmailSendFailed("Se ha agotado el tiempo de espera al enviar el correo", status_code=504)
		except smtplib.SMTPException as e:
			logger.error(f"Error SMTP al enviar el correo: {e}")
			raise EmailSendFailed(f"Error SMTP al enviar el correo: {str(e)}")
		except Exception as e:
			logger.error(f"Error inesperado al enviar el correo: {e}")
			raise EmailSendFailed(f"Error inesperado al enviar el correo: {str(e)}")
		finally:
			try:
				server.quit()
			except NameError:
				# En caso de que la variable 'server' no esté definida (por ejemplo, si se produce una excepción en la conexión)
				logger.error(f"Error inesperado: {e}")
				pass

	def render_template(self, template_name: str, **kwargs) -> str:
		# Simulación de renderizado de plantilla
		logger.debug(f"Renderizando plantilla {template_name} con datos: {kwargs}")
		# Configurar Jinja2 para cargar las plantillas desde el directorio 'templates'
		env = Environment(loader=FileSystemLoader(self.settings.APP_PATH +'/app/templates'))
		template = env.get_template(template_name)
		return template.render(**kwargs)
