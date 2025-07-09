# app/api/v1/catalogs.py
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel
from typing import Optional

from app.core.CRUD import CRUD
from app.models.CClaveProdServ import ClaveProdServ
from app.models.CExportacion import Exportacion
from app.models.CFormaPago import FormaPago
from app.models.CImpuesto import Impuesto
from app.models.CMetodoPago import MetodoPago
from app.models.CMoneda import Moneda
from app.models.CObjetoImp import ObjetoImp
from app.models.CRegimenFiscal import RegimenFiscal
from app.models.CTasaOCuota import TasaOCuota
from app.models.CTipoComprobante import TipoComprobante
from app.models.CTipoFactor import TipoFactor
from app.models.CTipoRelacion import TipoRelacion
from app.models.CUsoCFDI import UsoCFDI
from app.models.CClaveUnidad import ClaveUnidad
from app.models.CCodigoPostal import CodigoPostal
from app.models.CMeses import Meses
from app.models.CPais import Pais
from app.models.CPatenteAduanal import PatenteAduanal
from app.models.CPeriodicidad import Periodicidad

router = APIRouter(
	prefix="/catalogs",
	tags=["Catalogos de SAT"]
)

# Define los esquemas Pydantic para la validación de datos
class ClaveProdServCreate(BaseModel):
	product_service_code: Optional[str] = None
	description: str
	include_transferred_vat: Optional[str] = None
	include_transferred_ieps: Optional[str] = None
	required_complement: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None
	border_zone_stimulus: Optional[str] = None
	similar_words: Optional[str] = None

class ClaveProdServResponse(ClaveProdServCreate):
	id: int

class ClaveProdServUpdate(ClaveProdServCreate):
	id: Optional[int] = None

class ExportacionCreate(BaseModel):
	export_code: Optional[str] = None
	description: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class ExportacionUpdate(ExportacionCreate):
	pass

class FormaPagoCreate(BaseModel):
	payment_method: Optional[str] = None
	description: Optional[str] = None
	is_banked: Optional[str] = None
	operation_number: Optional[str] = None
	payer_account_rfc: Optional[str] = None
	payer_account: Optional[str] = None
	payer_account_pattern: Optional[str] = None
	beneficiary_account_rfc: Optional[str] = None
	beneficiary_account: Optional[str] = None
	beneficiary_account_pattern: Optional[str] = None
	payment_chain_type: Optional[str] = None
	payer_bank_name_if_external: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class FormaPagoUpdate(FormaPagoCreate):
	id: Optional[int] = None
	pass

class ImpuestoCreate(BaseModel):
	c_tax: Optional[str] = None
	description: Optional[str] = None
	tax_withholding: Optional[str] = None
	tax_transferred: Optional[str] = None
	local_federal: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class ImpuestoUpdate(ImpuestoCreate):
	id: Optional[int] = None

class MetodoPagoCreate(BaseModel):
	payment_method_code: Optional[str] = None
	description: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class MetodoPagoUpdate(MetodoPagoCreate):
	pass

class MonedaCreate(BaseModel):
	currency_code: Optional[str] = None
	description: Optional[str] = None
	decimal_places: Optional[str] = None
	variation_percentage: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class MonedaUpdate(MonedaCreate):
	id: Optional[int] = None

class ObjetoImpCreate(BaseModel):
	tax_object_code: Optional[str] = None
	description: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class ObjetoImpUpdate(ObjetoImpCreate):
	pass

class RegimenFiscalCreate(BaseModel):
	tax_regime_code: Optional[str] = None
	description: Optional[str] = None
	fisica: Optional[str] = None
	moral: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class RegimenFiscalUpdate(RegimenFiscalCreate):
	pass

class TasaOCuotaCreate(BaseModel):
	ranged_or_fixed: Optional[str] = None
	minimum_value: Optional[int] = None
	maximum_value: Optional[int] = None
	tax: Optional[str] = None
	factor: Optional[str] = None
	transfer: Optional[str] = None
	withholding: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class TasaOCuotaUpdate(TasaOCuotaCreate):
  id: Optional[int] = None

class TipoComprobanteCreate(BaseModel):
	voucher_type_code: Optional[str] = None
	description: Optional[str] = None
	max_value: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class TipoComprobanteUpdate(TipoComprobanteCreate):
  id: Optional[int] = None

class TipoFactorCreate(BaseModel):
	factor_type_code: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class TipoFactorUpdate(TipoFactorCreate):
  id: Optional[int] = None

class TipoRelacionCreate(BaseModel):
	relation_type_code: Optional[str] = None
	description: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class TipoRelacionUpdate(TipoRelacionCreate):
  id: Optional[int] = None

class UsoCFDICreate(BaseModel):
	cfdi_use_code: Optional[str] = None
	description: Optional[str] = None
	moral: Optional[str] = None
	fisica: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None
	recipient_tax_regime: Optional[str] = None

class UsoCFDIUpdate(UsoCFDICreate):
  id: Optional[int] = None

class ClaveUnidadCreate(BaseModel):
	unit_code: Optional[str] = None
	name_unit: Optional[str] = None
	description: Optional[str] = None
	nota_unit: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None
	symbol: Optional[str] = None

class ClaveUnidadUpdate(ClaveUnidadCreate):
  id: Optional[int] = None

class CodigoPostalCreate(BaseModel):
	c_codigopostal: Optional[int] = None
	c_estado: Optional[str] = None
	c_municipio: Optional[int] = None
	c_localidad: Optional[int] = None
	estimulo_franja_fronteriza: Optional[int] = None
	fecha_inicio_de_vigencia: Optional[str] = None
	fecha_fin_de_vigencia: Optional[str] = None
	descripcion_del_huso_horario: Optional[str] = None
	mes_inicio_horario_verano: Optional[str] = None
	dia_inicio_horario_verano: Optional[str] = None
	dia_inicio_horario_verano_1: Optional[str] = None
	diferencia_horaria_verano: Optional[int] = None
	mes_inicio_horario_invierno: Optional[str] = None
	dia_inicio_horario_invierno: Optional[str] = None
	dia_inicio_horario_invierno_1: Optional[str] = None
	diferencia_horaria_invierno: Optional[int] = None

class CodigoPostalUpdate(CodigoPostalCreate):
  id: Optional[int] = None

class MesesCreate(BaseModel):
		c_month: Optional[str] = None
		description: Optional[str] = None
		effective_start_date: Optional[str] = None
		effective_end_date: Optional[str] = None

class MesesUpdate(MesesCreate):
  id: Optional[int] = None

class PaisCreate(BaseModel):
		c_country: Optional[str] = None
		description: Optional[str] = None
		postcode_format: Optional[str] = None
		tax_identity_registration_format: Optional[str] = None
		tax_identity_registration_validation: Optional[str] = None
		groups: Optional[str] = None

class PaisUpdate(PaisCreate):
  id: Optional[int] = None

class PatenteAduanalCreate(BaseModel):
		c_customs: Optional[str] = None
		effective_start_date: Optional[str] = None
		effective_end_date: Optional[str] = None

class PatenteAduanalUpdate(PatenteAduanalCreate):
  id: Optional[int] = None

class PeriodicidadCreate(BaseModel):
	period: Optional[str] = None
	description: Optional[str] = None
	effective_start_date: Optional[str] = None
	effective_end_date: Optional[str] = None

class PeriodicidadUpdate(PeriodicidadCreate):
  id: Optional[int] = None

@router.get("/claveprodserv/getall")
async def claveproductoservall(
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
		model = ClaveProdServ
		crud = CRUD(model)
		rows = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": rows[0],
			"total_rows": rows[1]
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/claveprodserv/create")
async def claveproductoservcreate(claveproductoserv_data: ClaveProdServCreate):
	try:
		model = ClaveProdServ
		crud = CRUD(model)
		# Valida si el campo 'description' está vacío
		if not claveproductoserv_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")
		new_entry = crud.create(**claveproductoserv_data.__dict__)
		if(new_entry):
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrio un error al crear el registro"
			data = False
		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/claveprodserv/{id}")
async def get_claveprodservbyid(id: int):
	try:
		model = ClaveProdServ
		crud = CRUD(model)
		entry = crud.get_by_id(id)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")
		return {
			"message": "Registro obtenido correctamente",
			"data": entry
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/claveprodserv/update/{id}")
async def update_claveprodserv(id: int, claveprodserv_data: ClaveProdServUpdate):
	try:
		model = ClaveProdServ
		crud = CRUD(model)
		entry = crud.update(id, **claveprodserv_data.__dict__)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")
		return {
			"message": "Registro actualizado correctamente.",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/claveprodserv/delete/{id}")
async def delete_claveprodserv(id: int):
	try:
		model = ClaveProdServ
		crud = CRUD(model)
		entry = crud.delete(id)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")
		return {
			"message": "Registro eliminado correctamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/exportacion/create")
async def create_exportacion(exportacion_data: ExportacionCreate):
	try:
		model = Exportacion  # Assuming this is your model class for the table Exportacion
		crud = CRUD(model)

		if not exportacion_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**exportacion_data.dict())

		return {
			"message": "Registro creado exitosamente",
			"data": new_entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/exportacion/getall")
async def get_all_exportacion(
	page_size: int = 10,
	current_page: int = 1,
	filter: Optional[str] = None
):
	try:
		model = Exportacion
		crud = CRUD(model)

		rows = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": rows[0],
			"total_rows": rows[1]
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/exportacion/{id_row}")
async def get_exportacion_by_id(id_row: int):
	try:
		model = Exportacion
		crud = CRUD(model)

		entry = crud.get_by_id(id_row)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/exportacion/update/{id_row}")
async def update_exportacion(id_row: int, exportacion_data: ExportacionUpdate):
	try:
		model = Exportacion
		crud = CRUD(model)

		entry = crud.update(id_row, **exportacion_data.dict())

		return {
			"message": "Registro actualizado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/exportacion/delete/{id_row}")
async def delete_exportacion(id_row: int):
	try:
		model = Exportacion
		crud = CRUD(model)

		entry = crud.delete(id_row)

		return {
			"message": "Registro eliminado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/formapago/create")
async def formapago_create(formapago_data: FormaPagoCreate):
	try:
		model = FormaPago
		crud = CRUD(model)

		# Valida si el campo 'payment_method' está vacío
		if not formapago_data.payment_method:
			raise HTTPException(status_code=400, detail="El campo 'payment_method' es requerido.")

		new_entry = crud.create(**formapago_data.dict())

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/formapago/getbyid/{id}")
async def formapago_getbyid(id: int):
	try:
		model = FormaPago
		crud = CRUD(model)
		entry = crud.get_by_id(id)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")
		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/formapago/update/{id}")
async def formapago_update(id: int, formapago_data: FormaPagoUpdate):
	try:
		model = FormaPago
		crud = CRUD(model)

		entry = crud.update(id)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		# Valida si el campo 'payment_method' está vacío
		if not formapago_data.payment_method:
			raise HTTPException(status_code=400, detail="El campo 'payment_method' es requerido.")

		updated_entry = crud.update(id, **formapago_data.dict())

		return {
			"message": "Registro actualizado exitosamente",
			"data": updated_entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/formapago/delete/{id}")
async def formapago_delete(id: int):
	try:
		model = FormaPago
		crud = CRUD(model)

		entry = crud.delete(id)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		deleted_entry = crud.delete(id)

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/formapago/getall")
async def formapago_get_paginated(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = FormaPago
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/impuesto/create")
async def create_impuesto(impuesto_data: ImpuestoCreate):
	try:
		model = Impuesto
		crud = CRUD(model)

		# Valida campos requeridos (si es necesario)
		if not impuesto_data.c_tax:
			raise HTTPException(status_code=400, detail="El campo 'tax' es requerido.")

		new_entry = crud.create(**impuesto_data.dict())
		return {
			"message": "Registro creado exitosamente",
			"data": new_entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/impuesto/getbyid/{impuesto_id}")
async def get_impuesto_by_id(impuesto_id: int):
	try:
		model = Impuesto
		crud = CRUD(model)
		entry = crud.get_by_id(impuesto_id)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")
		return {
			"message": "Registro encontrado",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/impuesto/update/{impuesto_id}")
async def update_impuesto(impuesto_id: int, impuesto_data: ImpuestoUpdate):
	try:
		model = Impuesto
		crud = CRUD(model)

		# Valida campos requeridos (si es necesario)
		if not impuesto_data.c_tax:
			raise HTTPException(status_code=400, detail="El campo 'tax' es requerido.")

		entry = crud.update(impuesto_id, **impuesto_data.dict())
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")
		return {
			"message": "Registro actualizado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/impuesto/delete/{impuesto_id}")
async def delete_impuesto(impuesto_id: int):
	try:
		model = Impuesto
		crud = CRUD(model)

		entry = crud.delete(impuesto_id)
		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")
		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/impuesto/getall")
async def get_paginated_impuesto(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Impuesto
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/metodopago/create")
async def create_metodopago(metodopago_data: MetodoPagoCreate):
	try:
		model = MetodoPago
		crud = CRUD(model)
		new_entry = crud.create(**metodopago_data.dict())
		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False
		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/metodopago/getall")
async def get_all_metodopago(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = MetodoPago
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/metodopago/getbyid/{id}")
async def get_metodopago_by_id(id: int):
	try:
		model = MetodoPago
		crud = CRUD(model)
		entry = crud.get_by_id(id)
		if entry:
			message = "Registro encontrado exitosamente"
			data = entry
		else:
			message = "No se encontró el registro"
			data = False
		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/metodopago/update/{id}")
async def update_metodopago(id: int, metodopago_data: MetodoPagoUpdate):
	try:
		model = MetodoPago
		crud = CRUD(model)
		entry = crud.update(id=id, **metodopago_data.dict())
		if entry:
			message = "Registro actualizado exitosamente"
			data = entry
		else:
			message = "No se encontró el registro para actualizar"
			data = False
		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/metodopago/delete/{id}")
async def delete_metodopago(id: int):
	try:
		model = MetodoPago
		crud = CRUD(model)
		entry = crud.delete(id)
		if entry:
			message = "Registro eliminado exitosamente"
			data = True
		else:
			message = "No se encontró el registro para eliminar"
			data = False
		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/moneda/create")
async def Moneda_create(Moneda_data: MonedaCreate):
	try:
		model = Moneda
		crud = CRUD(model)

		# Valida campos específicos si es necesario (similar al ejemplo de claveproductoserv)
		if not Moneda_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**Moneda_data.dict())
		print(new_entry)  # Puedes eliminar el print si no lo necesitas

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/moneda/getall")
async def Moneda_get_all(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Moneda
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/moneda/getbyid/{id}")
async def Moneda_get_by_id(id: int):
	try:
		model = Moneda
		crud = CRUD(model)

		entry = crud.get_by_id(id)
		print(entry)  # Puedes eliminar el print si no lo necesitas

		if entry:
			message = "Registro encontrado exitosamente"
			data = entry
		else:
			message = "No se encontró el registro con el ID proporcionado"
			data = None

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/moneda/update/{id}")
async def Moneda_update(id: int, Moneda_data: MonedaUpdate):
	try:
		model = Moneda
		crud = CRUD(model)

		# Valida campos específicos si es necesario (similar al ejemplo de claveproductoserv)
		if not Moneda_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		entry = crud.update(id, **Moneda_data.dict())
		print(entry)  # Puedes eliminar el print si no lo necesitas

		if entry:
			message = "Registro actualizado exitosamente"
			data = entry
		else:
			message = "No se pudo actualizar el registro con el ID proporcionado"
			data = False

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/moneda/delete/{id}")
async def Moneda_delete(id: int):
	try:
		model = Moneda
		crud = CRUD(model)

		entry = crud.delete(id)
		print(entry)  # Puedes eliminar el print si no lo necesitas

		if entry:
			message = "Registro eliminado exitosamente"
			data = True
		else:
			message = "No se pudo eliminar el registro con el ID proporcionado"
			data = False

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/objetoimp/create")
async def create_objetoimp(objetoimp_data: ObjetoImpCreate):
	try:
		model = ObjetoImp
		crud = CRUD(model)

		# Valida si el campo 'description' está vacío
		if not objetoimp_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**objetoimp_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/objetoimp/getbyid/{id}")
async def get_objetoimp_by_id(id: int):
	try:
		model = ObjetoImp
		crud = CRUD(model)
		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/objetoimp/update/{id}")
async def update_objetoimp(id: int, objetoimp_data: ObjetoImpUpdate):
	try:
		model = ObjetoImp
		crud = CRUD(model)

		# Valida si el campo 'description' está vacío
		if not objetoimp_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		entry = crud.update(id, **objetoimp_data.dict())

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado para actualizar.")

		return {
			"message": "Registro actualizado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/objetoimp/delete/{id}")
async def delete_objetoimp(id: int):
	try:
		model = ObjetoImp
		crud = CRUD(model)

		entry = crud.delete(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado para eliminar.")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/objetoimp/getall")
async def get_objetoimp_paginated(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = ObjetoImp
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/regimenfiscal/create")
async def create_regimen_fiscal(regimen_fiscal_data: RegimenFiscalCreate):
	try:
		model = RegimenFiscal  # Asegúrate de que esta clase esté correctamente definida
		crud = CRUD(model)

		# Valida si el campo obligatorio está vacío (si hay campos obligatorios)
		if not regimen_fiscal_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**regimen_fiscal_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/regimenfiscal/getall")
async def get_all_regimen_fiscal(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = RegimenFiscal
		crud = CRUD(model)
		# Obtener todos los registros
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/regimenfiscal/getbyid/{id}")
async def get_regimen_fiscal_by_id(id: int):
	try:
		model = RegimenFiscal
		crud = CRUD(model)

		# Obtener un registro por su ID
		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/regimenfiscal/update/{id}")
async def update_regimen_fiscal(id: int, regimen_fiscal_data: RegimenFiscalUpdate):
	try:
		model = RegimenFiscal
		crud = CRUD(model)

		# Buscar el registro por ID
		entry = crud.update(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		# Actualizar el registro
		updated_entry = crud.update(id, **regimen_fiscal_data.dict())

		return {
			"message": "Registro actualizado exitosamente",
			"data": updated_entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/regimenfiscal/delete/{id}")
async def delete_regimen_fiscal(id: int):
	try:
		model = RegimenFiscal
		crud = CRUD(model)

		# Buscar el registro por ID
		entry = crud.delete(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		# Eliminar el registro
		crud.delete(id)

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasaocuota/create")
async def tasaocuota_create(tasaocuota_data: TasaOCuotaCreate):
	try:
		model = TasaOCuota
		crud = CRUD(model)

		# Valida si el campo 'ranged_or_fixed' está vacío
		if not tasaocuota_data.ranged_or_fixed:
			raise HTTPException(status_code=400, detail="El campo 'ranged_or_fixed' es requerido.")

		new_entry = crud.create(**tasaocuota_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasaocuota/getall")
async def tasaocuota_getall(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = TasaOCuota
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasaocuota/getbyid/{id}")
async def tasaocuota_getbyid(id: int):
	try:
		model = TasaOCuota
		crud = CRUD(model)
		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/tasaocuota/update/{id}")
async def tasaocuota_update(id: int, tasaocuota_data: TasaOCuotaUpdate):
	try:
		model = TasaOCuota
		crud = CRUD(model)

		# Valida si el campo 'id' está proporcionado
		if not hasattr(tasaocuota_data, "id"):
			raise HTTPException(status_code=400, detail="El campo 'id' es requerido para actualizar")

		entry = crud.update(id, **tasaocuota_data.dict())

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado para actualizar")

		return {
			"message": "Registro actualizado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasaocuota/delete/{id}")
async def tasaocuota_delete(id: int):
	try:
		model = TasaOCuota
		crud = CRUD(model)

		entry = crud.delete(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado para eliminar")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/tipocomprobante/create")
async def create_tipo_comprobante(tipo_comprobante_data: TipoComprobanteCreate):
	try:
		model = TipoComprobante
		crud = CRUD(model)

		# Valida si el campo 'description' está vacío
		if not tipo_comprobante_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**tipo_comprobante_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tipocomprobante/getbyid/{id}")
async def get_tipo_comprobante_by_id(id: int):
	try:
		model = TipoComprobante
		crud = CRUD(model)
		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/tipocomprobante/update/{id}")
async def update_tipo_comprobante(id: int, tipo_comprobante_data: TipoComprobanteUpdate):
	try:
		model = TipoComprobante
		crud = CRUD(model)

		# Actualiza los campos necesarios
		updated_entry = crud.update(id, **tipo_comprobante_data.dict())

		if not updated_entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro actualizado exitosamente",
			"data": updated_entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tipocomprobante/delete/{id}")
async def delete_tipo_comprobante(id: int):
	try:
		model = TipoComprobante
		crud = CRUD(model)

		deleted = crud.delete(id)

		if not deleted:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tipocomprobante/getall")
async def get_tipo_comprobante_paginated(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = TipoComprobante
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/tipofactor/create")
async def create_tipo_factor(tipo_factor_data: TipoFactorCreate):
	try:
		model = TipoFactor
		crud = CRUD(model)
		if not tipo_factor_data.factor_type_code:
			raise HTTPException(status_code=400, detail="El campo 'factor_type_code' es requerido.")

		new_entry = crud.create(**tipo_factor_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tipofactor/get/{id}")
async def get_single_tipo_factor(id: int):
	try:
		model = TipoFactor
		crud = CRUD(model)

		record = crud.get_by_id(id)

		if not record:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro obtenido exitosamente",
			"data": record
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/tipofactor/update/{id}")
async def update_tipo_factor(id: int, tipo_factor_data: TipoFactorUpdate):
	try:
		model = TipoFactor
		crud = CRUD(model)

		record = crud.update(id, **tipo_factor_data.dict())

		if not record:
			raise HTTPException(status_code=404, detail="Registro no encontrado para actualizar")

		return {
			"message": "Registro actualizado exitosamente",
			"data": record
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tipofactor/delete/{id}")
async def delete_tipo_factor(id: int):
	try:
		model = TipoFactor
		crud = CRUD(model)

		deleted = crud.delete(id)

		if not deleted:
			raise HTTPException(status_code=404, detail="Registro no encontrado para eliminar")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tipofactor/getall")
async def get_paginated_tipo_factors(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = TipoFactor
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/tiporelacion/create")
async def create_tipo_relacion(tipo_relacion_data: TipoRelacionCreate):
	try:
		model = TipoRelacion
		crud = CRUD(model)

		# Example validation (adjust as needed)
		if not tipo_relacion_data.relation_type_code:
			raise HTTPException(status_code=400,
							  detail="El campo 'relation_type_code' es requerido.")

		new_entry = crud.create(**tipo_relacion_data.dict())
		print(new_entry)  # For debugging purposes

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tiporelacion/getall")
async def get_all_tipo_relacion(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = TipoRelacion
		crud = CRUD(model)

		# Example: Get all records with pagination
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/tiporelacion/getbyid/{id}")
async def get_tipo_relacion_by_id(id: int):
	try:
		model = TipoRelacion
		crud = CRUD(model)

		result = crud.get_by_id(id)

		if not result:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		return {
			"message": "Registro obtenido exitosamente",
			"data": result
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/tiporelacion/update/{id}")
async def update_tipo_relacion(id: int, tipo_relacion_data: TipoRelacionUpdate):
	try:
		model = TipoRelacion
		crud = CRUD(model)

		# Example validation (adjust as needed)
		if not tipo_relacion_data.description:
			raise HTTPException(status_code=400,
							  detail="El campo 'description' es requerido.")

		updated_entry = crud.update(id, **tipo_relacion_data.dict())
		print(updated_entry)  # For debugging purposes

		if updated_entry:
			message = "Registro actualizado exitosamente"
			data = updated_entry
		else:
			message = "Ocurrió un error al actualizar el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tiporelacion/delete/{id}")
async def delete_tipo_relacion(id: int):
	try:
		model = TipoRelacion
		crud = CRUD(model)

		deleted_entry = crud.delete(id)

		if not deleted_entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True  # Optional: You can include a confirmation flag
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/usocfdi/create")
async def create_usocfdi(usocfdi_data: UsoCFDICreate):
	try:
		model = UsoCFDI
		crud = CRUD(model)

		# Valida campos requeridos (puedes modificar según tus necesidades)
		required_fields = ["cfdi_use_code", "description"]
		for field in required_fields:
			if not getattr(usocfdi_data, field, None):
				raise HTTPException(
					status_code=400,
					detail=f"El campo '{field}' es requerido."
				)

		new_entry = crud.create(**usocfdi_data.dict())

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/usocfdi/getall")
async def get_all_usocfdi(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = UsoCFDI
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/usocfdi/getbyid/{id}")
async def get_usocfdi_by_id(id: int):
	try:
		model = UsoCFDI()
		crud = CRUD(model)

		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(
				status_code=404,
				detail="Registro no encontrado"
			)

		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/usocfdi/update/{id}")
async def update_usocfdi(id: int, usocfdi_data: UsoCFDIUpdate):
	try:
		model = UsoCFDI
		crud = CRUD(model)

		# Valida campos requeridos (puedes modificar según tus necesidades)
		required_fields = ["cfdi_use_code", "description"]
		for field in required_fields:
			if not getattr(usocfdi_data, field, None):
				raise HTTPException(
					status_code=400,
					detail=f"El campo '{field}' es requerido."
				)

		updated_entry = crud.update(id, **usocfdi_data.dict())

		if not updated_entry:
			raise HTTPException(
				status_code=404,
				detail="Registro no encontrado"
			)

		return {
			"message": "Registro actualizado exitosamente",
			"data": updated_entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/usocfdi/delete/{id}")
async def delete_usocfdi(id: int):
	try:
		model = UsoCFDI
		crud = CRUD(model)

		deleted_entry = crud.delete(id)

		if not deleted_entry:
			raise HTTPException(
				status_code=404,
				detail="Registro no encontrado"
			)

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/claveunidad/create")
async def claveunidadcreate(claveunidad_data: ClaveUnidadCreate):
	try:
		model = ClaveUnidad  # Asegúrate de que esta clase existe
		crud = CRUD(model)

		# Realiza validaciones si es necesario, por ejemplo:
		if not claveunidad_data.name_unit:
			raise HTTPException(status_code=400, detail="El campo 'name_unit' es requerido.")

		new_entry = crud.create(**claveunidad_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/claveunidad/getall")
async def claveunidadgetall(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = ClaveUnidad  # Asegúrate de que esta clase existe
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/claveunidad/{id}")
async def claveunidadgetbyid(id: int):
	try:
		model = ClaveUnidad  # Asegúrate de que esta clase existe
		crud = CRUD(model)

		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro obtenido exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/claveunidad/update/{id}")
async def claveunidadupdate(id: int, claveunidad_data: ClaveUnidadUpdate):
	try:
		model = ClaveUnidad  # Asegúrate de que esta clase existe
		crud = CRUD(model)

		entry = crud.update(id, **claveunidad_data.dict())

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro actualizado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/claveunidad/delete/{id}")
async def claveunidaddelete(id: int):
	try:
		model = ClaveUnidad
		crud = CRUD(model)

		entry = crud.delete(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True  # O puedes devolver el registro antes de eliminarlo
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/codigopostal/create")
async def codigopostal_create(codigopostal_data: CodigoPostalCreate):
	try:
		model = CodigoPostal
		crud = CRUD(model)

		# Valida si el campo obligatorio está vacío
		if not codigopostal_data.c_codigopostal:
			raise HTTPException(status_code=400, detail="El campo 'c_CodigoPostal' es requerido.")

		new_dict = codigopostal_data.__dict__
		new_entry = crud.create(**new_dict)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/codigopostal/getbyid/{id}")
async def codigopostal_get_by_id(id: int):
	try:
		model = CodigoPostal
		crud = CRUD(model)

		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		return {
			"message": "Registro encontrado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/codigopostal/update/{id}")
async def codigopostal_update(id: int, codigopostal_data: CodigoPostalUpdate):
	try:
		model = CodigoPostal
		crud = CRUD(model)

		entry = crud.update(id, **codigopostal_data.dict())

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		return {
			"message": "Registro actualizado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/codigopostal/delete/{id}")
async def codigopostal_delete(id: int):
	try:
		model = CodigoPostal
		crud = CRUD(model)

		entry = crud.delete(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado.")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/codigopostal/getall")
async def codigopostal_get_all(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = CodigoPostal
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		print(e)
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/meses/create")
async def create_month(month_data: MesesCreate):
	try:
		model = Meses
		crud = CRUD(model)

		# Validación personalizada si es necesario
		if not month_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**month_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/meses/getbyid{id}")
async def get_month_by_id(id: int):
	try:
		model = Meses
		crud = CRUD(model)

		month = crud.get_by_id(id)

		if not month:
			raise HTTPException(status_code=404, detail="El mes no existe.")

		return {
			"message": "Registro encontrado exitosamente",
			"data": month
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/meses/update/{id}")
async def update_month(id: int, month_data: MesesUpdate):
	try:
		model = Meses
		crud = CRUD(model)

		# Validación personalizada si es necesario
		if not month_data.description and id == 0:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido para actualizar.")

		updated_month = crud.update(id, **month_data.dict())

		if not updated_month:
			raise HTTPException(status_code=404, detail="No se pudo actualizar el mes.")

		return {
			"message": "Registro actualizado exitosamente",
			"data": updated_month
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/meses/delete/{id}")
async def delete_month(id: int):
	try:
		model = Meses
		crud = CRUD(model)

		deleted = crud.delete(id)

		if not deleted:
			raise HTTPException(status_code=404, detail="No se pudo eliminar el mes.")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/meses/getall")
async def get_all_months(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Meses
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/pais/create")
async def pais_create(pais_data: PaisCreate):
	try:
		model = Pais
		crud = CRUD(model)

		# Valida si el campo 'description' está vacío
		if not pais_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**pais_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/pais/getall")
async def pais_get_all(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Pais
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/pais/getbyid")
async def pais_get_by_id(id_row: int):
	try:
		model = Pais
		crud = CRUD(model)

		result = crud.get_by_id(id_row=id_row)

		if result:
			message = "Registro obtenido exitosamente"
			data = result
		else:
			message = "No se encontró el registro"
			data = None

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/pais/update/{id_row}")
async def pais_update(id_row: int, pais_data: PaisUpdate):
	try:
		model = Pais
		crud = CRUD(model)

		result = crud.update(id_row=id_row, **pais_data.dict())

		if result:
			message = "Registro actualizado exitosamente"
			data = result
		else:
			message = "No se pudo actualizar el registro"
			data = False

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/pais/delete/{id_row}")
async def pais_delete(id_row: int):
	try:
		model = Pais
		crud = CRUD(model)

		result = crud.delete(id_row=id_row)

		if result:
			message = "Registro eliminado exitosamente"
			data = True
		else:
			message = "No se pudo eliminar el registro"
			data = False

		return {
			"message": message,
			"data": data
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/patenteaduanales/create")
async def patenteaduanal_create(patenteAduanal_data: PatenteAduanalCreate):
	try:
		model = PatenteAduanal
		crud = CRUD(model)

		# Valida si el campo requerido está presente
		required_fields = ["c_customs"]
		for field in required_fields:
			if not getattr(patenteAduanal_data, field, None):
				raise HTTPException(status_code=400, detail=f"El campo '{field}' es requerido.")

		new_entry = crud.create(**patenteAduanal_data.dict())
		print(new_entry)

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/patenteaduanales/getbyid/{id_row}")
async def patenteaduanal_get_by_id(id_row: int):
	try:
		model = PatenteAduanal
		crud = CRUD(model)

		entry = crud.get_by_id(id_row)

		if entry:
			message = "Registro encontrado exitosamente"
			data = entry
		else:
			message = "No se encontró el registro"
			data = None

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/patenteaduanales/update/{id_row}")
async def patenteaduanal_update(id_row: int, patenteAduanal_data: PatenteAduanalUpdate):
	try:
		model = PatenteAduanal
		crud = CRUD(model)

		# Valida si el campo requerido está presente
		required_fields = ["c_customs"]
		for field in required_fields:
			if not getattr(patenteAduanal_data, field, None):
				raise HTTPException(status_code=400, detail=f"El campo '{field}' es requerido.")

		entry = crud.update(id_row, **patenteAduanal_data.dict())

		if entry:
			message = "Registro actualizado exitosamente"
			data = entry
		else:
			message = "No se pudo actualizar el registro"
			data = None

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/patenteaduanales/delete/{id_row}")
async def patenteaduanal_delete(id_row: int):
	try:
		model = PatenteAduanal
		crud = CRUD(model)

		entry = crud.delete(id_row)

		if entry:
			message = "Registro eliminado exitosamente"
			data = True
		else:
			message = "No se pudo eliminar el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/patenteaduanales/getall")
async def patenteaduanal_get_all(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = PatenteAduanal
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/periodicidad/create")
async def create_periodicidad(c_periodicidad_data: PeriodicidadCreate):
	try:
		model = Periodicidad
		crud = CRUD(model)

		# Validar campos requeridos (puedes modificar según tus necesidades)
		if not c_periodicidad_data.description:
			raise HTTPException(status_code=400, detail="El campo 'description' es requerido.")

		new_entry = crud.create(**c_periodicidad_data.dict())

		if new_entry:
			message = "Registro creado exitosamente"
			data = new_entry
		else:
			message = "Ocurrió un error al crear el registro"
			data = False

		return {
			"message": message,
			"data": data
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/periodicidad/getbyid/{id}")
async def get_periodicidadbyid(id: int):
	try:
		model = Periodicidad
		crud = CRUD(model)

		entry = crud.get_by_id(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro encontrado",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/periodicidad/update/{id}")
async def update_periodicidad(id: int, c_periodicidad_data: PeriodicidadUpdate):
	try:
		model = Periodicidad
		crud = CRUD(model)

		entry = crud.update(id, **c_periodicidad_data.dict())

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro actualizado exitosamente",
			"data": entry
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.delete("/periodicidad/delete/{id}")
async def delete_periodicidad(id: int):
	try:
		model = Periodicidad
		crud = CRUD(model)

		entry = crud.delete(id)

		if not entry:
			raise HTTPException(status_code=404, detail="Registro no encontrado")

		return {
			"message": "Registro eliminado exitosamente",
			"data": True
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/periodicidad/getall")
async def get_periodicidadpaginated(
	current_page: int = 1,
	page_size: int = 10,
	filter: Optional[str] = None
):
	try:
		if current_page < 1:
			raise ValueError("current_page debe ser un valor positivo.")
		if page_size < 1 or page_size > 100:
			raise ValueError("page_size debe estar entre 1 y 100.")
		model = Periodicidad
		crud = CRUD(model)
		entries, total = crud.get_paginated(page_size, current_page, filter)
		return {
			"data": entries,
			"total_rows": total
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
