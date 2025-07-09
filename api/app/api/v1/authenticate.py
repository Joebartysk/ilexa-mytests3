# app/api/v1/authenticate.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

from app.core.logger_config import setup_logger
from app.models.Users import User
from app.services.AuthService import AuthService
from app.core.CRUD import CRUD

logger = setup_logger()

router = APIRouter(
	prefix="/auth",
	tags=["Autenticacion y registro de usuarios"]
)

class RegisterUser(BaseModel):
	email: str
	password: str  # La contraseña se almacenará hasheada
	first_name: str
	last_name: str
	phone: Optional[str] = None
	# status: Optional[str] = "pending_verification"

@router.post("/register")
async def register_usr(user_data: RegisterUser):
	try:
		# Crear una nueva instancia de usuario
		# new_user = User(email=user_data.email,
		# 				first_name=user_data.first_name,
		# 				last_name=user_data.last_name,
		# 				phone=user_data.phone,
		# 				status="pending_verification")
		auth_srv = AuthService()
		new_user = User
		crud = CRUD(new_user)

		# Hashear la contraseña (asumiendo que tienes una función para hacerlo)
		hashed_password = auth_srv.hash_password(user_data.password)  # Implementa esta función
		# hashed_password = user_data.password
		nw_usr_data = user_data.model_dump(exclude={'password'}, by_alias=True)
		nw_usr_data['password_hash'] = hashed_password

		# Crear los tokens si no están proporcionados
		nw_usr_data['verification_token'] = str(uuid.uuid4())

		print(nw_usr_data)

		# if not new_user.reset_password_token:
		# 	new_user.reset_password_token = str(uuid.uuid4())

		# rslt = crud.create(**nw_usr_data)

		auth_srv.send_mail_registration(user_data, nw_usr_data['verification_token'])

		return {"message": "Usuario creado exitosamente", "data": rslt}

	except ValueError as e:
		dtl=f"Error al procesar la solicitud: {e}"
		# Registrar el error en el logger
		logger.error(dtl)
		# Lanzar una excepción HTTP con un mensaje de error amigable para el cliente
		raise HTTPException(status_code=400, detail=dtl)

	except Exception as e:
		dtl=f"Ocurrió un error interno del servidor: {e}"
		# Registrar cualquier otro tipo de error en el logger
		logger.error(dtl)
		# Lanzar una excepción HTTP genérica para otros errores
		raise HTTPException(status_code=500, detail=dtl)
