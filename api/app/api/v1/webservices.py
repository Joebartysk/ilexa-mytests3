# app/api/v1/webservices.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from pydantic import BaseModel, Field
import datetime
import base64
from typing import List
import os
from app.core.config import Settings
import hvac
import hashlib
from app.services.Fiel import Fiel
from app.services.Authentication import Authentication
from app.services.RequestDownload import RequestDownload
from app.services.CheckRequestDownload import CheckRequestDownload
from app.services.MassiveDownload import MassiveDownload
from app.services.ValidationCFDI import ValidationCFDI
from app.services.ValidateCer import ValidateCer

router = APIRouter(
	prefix="/webservices",
	tags=["webservices"]
)

class SolicitudCFDIRequest(BaseModel):
	token: str
	rfc: str
	fecha_inicial: str
	fecha_final: str
	tipo_descarga: str = 'EMITIDOS'
	secret: str

class VerifyDownloadRequest(BaseModel):
	token: str
	id_solicitud: str
	rfc: str
	secret: str

class DownloadPackage(BaseModel):
	token: str
	rfc: str
	paquetes: List[str] = Field(
		...,
		description="Lista de identificadores de paquetes para descargar",
		example=["9C12C22C-A8EE-4E58-9A9F-47D09107D8EE_01"]
	)
	secret: str

class StatusCFDI(BaseModel):
	rfc_emisor: str
	rfc_receptor: str
	total: str
	uuid: str

@router.post("/savecerts")
async def savecerts(
	cer_file: UploadFile = File(...),
	key_file: UploadFile = File(...),
	password: str = Form(...)
):
	try:
		settings = Settings()

		idusr = 2 # id de usuario de la sesion
		bytes_numero = idusr.to_bytes(4, byteorder='big')
		hash_object = hashlib.sha256()
		hash_object.update(bytes_numero)
		path_vault = hash_object.hexdigest()

		cer_path = f"{settings.APP_PATH}/tmp/{cer_file.filename}"
		key_path = f"{settings.APP_PATH}/tmp/{key_file.filename}"

		os.makedirs("tmp", exist_ok=True)

		with open(cer_path, "wb") as f:
			f.write(await cer_file.read())
			os.rename(cer_path, f"{settings.APP_PATH}/tmp/cer1.cer")
			cer_path = f"{settings.APP_PATH}/tmp/cer1.cer"
		with open(key_path, "wb") as f:
			f.write(await key_file.read())
			os.rename(key_path, f"{settings.APP_PATH}/tmp/key1.key")
			key_path = f"{settings.APP_PATH}/tmp/key1.key"

		expiration_date = ValidateCer.get_certificate_info(cer_path)
		print(expiration_date)
		cer = open(cer_path, 'rb').read()
		key = open(key_path, 'rb').read()

		clienthvac = hvac.Client(url=f'{settings.VAULT_ADDR}', token=f'{settings.VAULT_TOKEN}')
		clienthvac.secrets.kv.v2.create_or_update_secret(
			path=path_vault,
			secret={
				'cer': cer.decode('latin1'),  # Convertimos a string compatible
				'key': key.decode('latin1'),
				'passphrase': password
			}
		)
		secret = path_vault
		os.remove(cer_path)
		os.remove(key_path)
		return {"secret": secret}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/authenticate")
async def authenticate(
	secret: str = None
):
	try:
		settings = Settings()

		if secret:
			path_vault = secret
		else:
			idusr = 2
			bytes_numero = idusr.to_bytes(4, byteorder='big')
			hash_object = hashlib.sha256()
			hash_object.update(bytes_numero)
			path_vault = hash_object.hexdigest()

		clienthvac = hvac.Client(url=f'{settings.VAULT_ADDR}', token=f'{settings.VAULT_TOKEN}')
		datas = clienthvac.secrets.kv.v2.read_secret_version(path=path_vault)['data']['data']
		cer = datas['cer'].encode('latin1')
		key = datas['key'].encode('latin1')
		password = datas['passphrase']

		fiel = Fiel(cer, key, password)
		auth = Authentication(fiel)
		token = ""
		token = auth.obtener_token()
		return {"token": token}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/downloadrequest")
async def downloadrequest(
	request: SolicitudCFDIRequest
):
	try:

		# Validaciones previas
		if len(request.token) <= 255:
			raise ValueError("El token debe tener más de 255 caracteres")

		format = '%Y-%m-%d'
		datetime_ini = datetime.datetime.strptime(request.fecha_inicial, format)
		datetime_fin = datetime.datetime.strptime(request.fecha_final, format)

		settings = Settings()

		if request.secret:
			path_vault = request.secret
		else:
			idusr = 2
			bytes_numero = idusr.to_bytes(4, byteorder='big')
			hash_object = hashlib.sha256()
			hash_object.update(bytes_numero)
			path_vault = hash_object.hexdigest()

		clienthvac = hvac.Client(url=f'{settings.VAULT_ADDR}', token=f'{settings.VAULT_TOKEN}')
		datas = clienthvac.secrets.kv.v2.read_secret_version(path=path_vault)['data']['data']
		cer = datas['cer'].encode('latin1')
		key = datas['key'].encode('latin1')
		password = datas['passphrase']

		fiel = Fiel(cer, key, password)

		descarga = RequestDownload(fiel)

		if request.tipo_descarga == 'EMITIDOS':
			# EMITIDOS
			solicitud = descarga.solicitar_descarga(
				request.token, request.rfc, datetime_ini, datetime_fin, rfc_emisor=request.rfc, tipo_solicitud='CFDI',
			)
		elif request.tipo_descarga == 'RECIBIDOS':
			# RECIBIDOS
			solicitud = descarga.solicitar_descarga(
				request.token, request.rfc, datetime_ini, datetime_fin, rfc_receptor=request.rfc, tipo_solicitud='CFDI',
			)

		return {"solicitude": solicitud}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/verifydownloadrequest")
async def downloadrequest(
	request: VerifyDownloadRequest
):
	try:
		settings = Settings()

		if request.secret:
			path_vault = request.secret
		else:
			idusr = 2
			bytes_numero = idusr.to_bytes(4, byteorder='big')
			hash_object = hashlib.sha256()
			hash_object.update(bytes_numero)
			path_vault = hash_object.hexdigest()

		clienthvac = hvac.Client(url=f'{settings.VAULT_ADDR}', token=f'{settings.VAULT_TOKEN}')
		datas = clienthvac.secrets.kv.v2.read_secret_version(path=path_vault)['data']['data']
		cer = datas['cer'].encode('latin1')
		key = datas['key'].encode('latin1')
		password = datas['passphrase']

		fiel = Fiel(cer, key, password)

		verificacion = CheckRequestDownload(fiel)
		verificacion = verificacion.verificar_descarga(
			request.token, request.rfc, request.id_solicitud
		)

		print( verificacion)

		return {
			"verify": verificacion,
			"satatus": {
				"0": "Token invalido.",
				"1": "Aceptada",
				"2": "En proceso",
				"3": "Terminada",
				"4": "Error",
				"5": "Rechazada",
				"6": "Vencida"
			}
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/downloadpackage")
async def downloadrequest(
	request: DownloadPackage
):
	try:
		settings = Settings()

		if request.secret:
			path_vault = request.secret
		else:
			idusr = 2
			bytes_numero = idusr.to_bytes(4, byteorder='big')
			hash_object = hashlib.sha256()
			hash_object.update(bytes_numero)
			path_vault = hash_object.hexdigest()

		clienthvac = hvac.Client(url=f'{settings.VAULT_ADDR}', token=f'{settings.VAULT_TOKEN}')
		datas = clienthvac.secrets.kv.v2.read_secret_version(path=path_vault)['data']['data']
		cer = datas['cer'].encode('latin1')
		key = datas['key'].encode('latin1')
		password = datas['passphrase']

		fiel = Fiel(cer, key, password)

		path_f = f"{settings.APP_PATH}/packages_cfdi/"

		for paquete in request.paquetes:
			descarga = MassiveDownload(fiel)
			descarga = descarga.descargar_paquete(request.token, request.rfc, paquete)

			print(f"Resultado para paquete {paquete}: {descarga}")

			if not descarga or 'paquete_b64' not in descarga:
				raise ValueError(f"No se pudo descargar el paquete {paquete}")

			with open(path_f + '{}.zip'.format(paquete), 'wb') as fp:
				fp.write(base64.b64decode(descarga['paquete_b64']))

		return {
			"status": "success",
			"path_files": path_f
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/statuscfdi")
async def downloadrequest(
	request: StatusCFDI
):
	try:
		validacion = ValidationCFDI()
		estado = validacion.obtener_estado(request.rfc_emisor, request.rfc_receptor, request.total, request.uuid)
		return {
			"status": "success",
			"status": estado
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
