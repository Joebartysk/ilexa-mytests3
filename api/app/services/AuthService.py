# app/services/AuthService.py

import bcrypt
from fastapi import HTTPException
from app.core.config import Settings
from app.core.logger_config import setup_logger
from app.services.EmailService import EmailService, EmailSendFailed, TemplateRenderError
from datetime import datetime

logger = setup_logger()
settings = Settings()

class AuthService:
	def hash_password(self, password: str) -> bytes:
		"""Hashea una contraseña utilizando bcrypt."""
		logger.debug("Iniciando el proceso de hashing de la contraseña.")
		# Genera un salt aleatorio y hashea la contraseña
		hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		logger.info("Contraseña hasheada exitosamente.")
		return hashed_password

	def verify_password(self, plain_password: str, hashed_password: bytes) -> bool:
		"""Verifica si una contraseña en texto plano coincide con un hash."""
		logger.debug("Iniciando el proceso de verificación de la contraseña.")
		# Verifica que las contraseñas coincidan
		return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

	def send_mail_registration(self, user_data, tkn):
		print("DATA USER ")
		print(user_data)
		try:
			body_text = "Este es un mensaje de prueba en texto plano."
			subject="Prueba de Correo con HTML"
			email_service = EmailService(timeout=17)
			body_html = email_service.render_template(
				'registration_email.html',
				username=user_data.first_name,
				verification_url=f"{settings.URL_HOST}/v1/verify-email?tkn={tkn}",
				year=str(datetime.now().year),
				company_name=settings.NAME_COMPANY)
			email_service.send_email(user_data.email, subject, body_text, body_html)

			return {"message": "Correo enviado correctamente"}

		except EmailSendFailed as e:
			logger.error(f"Error al enviar correo: {e}")
			# Puedes personalizar el mensaje de error según necesites
			raise HTTPException(status_code=e.status_code, detail=str(e))

		except TemplateRenderError as e:
			logger.error(f"Error al renderizar plantilla: {e}")
			# Puedes personalizar el mensaje de error según necesites
			raise HTTPException(status_code=e.status_code, detail=str(e))

		except Exception as e:
			logger.error(f"Ocurrió un error inesperado al procesar la solicitud: {e}")
			raise HTTPException(status_code=500, detail="Ocurrió un error interno del servidor")
