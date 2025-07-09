# app/core/config.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
	APP_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
	ALLOW_ORIGINS: str = "*"
	NAME_APP: str = "main:app"
	HOSTING: str = "127.0.0.1"
	PORT: int = 8000
	RELOAD: bool = True
	VAULT_ADDR: str = "VAULT_ADDR"
	VAULT_CACERT: str ="VAULT_CACERT"
	VAULT_TOKEN: str ="VAULT_TOKEN"

	# Configuración de correo electrónico
	EMAIL_USERNAME: str = "gustavo@vctra.xyz"
	EMAIL_PASSWORD: str = "batcaver07Ycaver.-7"	# Reemplaza con la contraseña real o utiliza una variable de entorno
	SMTP_SERVER: str = "mail.vctra.xyz"
	SMTP_PORT: int = 465
	NAME_COMPANY: str = "Ilexlumina"
	TIME_EXPIRE_TOKEN_REGISTER: int = 15 # Representado en minutos
	URL_HOST: str = "http://localhost:8000"

	# class Config:
	# 	env_file = ".env"
