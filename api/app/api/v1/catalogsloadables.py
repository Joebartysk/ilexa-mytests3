# app/api/v1/catalogsloadables.py
from fastapi import APIRouter, HTTPException
from typing import Optional

# from pydantic import BaseModel
# from typing import Optional
from app.core.CRUD import CRUD
from app.models.Demandables import Demandables
from app.models.Firms import Firms
from app.models.NoLocated import NoLocated
from app.models.SATBlackList import SATBlacklist
from app.models.Sentences import Sentences

router = APIRouter(
	prefix="/catalogsloadables",
	tags=["Catalogos de SAT autocargados"]
)

@router.get("/demandables")
async def getall_demandables(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		# Validar los valores de current_page y page_size
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Demandables
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/firms")
async def getall_firms(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		# Validar los valores de current_page y page_size
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Firms
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/nolocated")
async def getall_no_located(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		# Validar los valores de current_page y page_size
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = NoLocated
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/satblacklist")
async def getall_sat_black_list(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		# Validar los valores de current_page y page_size
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = SATBlacklist
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/sentences")
async def getall_sentences(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		# Validar los valores de current_page y page_size
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Sentences
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
