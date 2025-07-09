# app/controllers/verify_email.py

from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.Users import User

router = APIRouter()

@router.get("/verify-email", include_in_schema=False)
async def verify_email(tkn: str):
	try:
		# Buscar el usuario en la base de datos utilizando el token
		# user = db.query(UserModel).filter(UserModel.verification_token == token).first()

		# if not user:
		# 	raise HTTPException(status_code=404, detail="Token no encontrado")

		# if user.is_verified:
		# 	return {"message": "La cuenta ya está verificada"}

		# # Marcar la cuenta como verificada
		# user.is_verified = True
		# db.commit()

		return {"message": "Cuenta verificada con éxito"}
	except HTTPException as e:
		logger.error(f"Error al verificar cuenta: {e.detail}")
		raise e
