# app/services/UpdateStatusCFDI.py

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.CFDIDocument import CFDI_CRUD
from services.ValidationCFDI import ValidationCFDI

class UpdateStatusCFDI:

	def get_all(self):
		crud = CFDI_CRUD()
		rows = crud.get_all_cfdis()
		return rows

	def update_status(self, ids, status):
		crud = CFDI_CRUD()
		cols = {
			"status": status
		}
		crud.update_cfdi(ids, **cols)

if __name__ == "__main__":
	obj = UpdateStatusCFDI()
	rows = obj.get_all()
	validation = ValidationCFDI()
	for row in rows:
		ids = row['cfdi_id']
		uuid = row['uuid']
		rfc_of_the_issuer = row['rfc_of_the_issuer']
		rfc_of_the_receiver = row['rfc_of_the_receiver']
		total = str(row['total'])
		status = estado = validation.obtener_estado(rfc_of_the_issuer, rfc_of_the_receiver, total, uuid)
		stat = status['estado']
		print(f"Actualizando status de id : {ids} uuid: {uuid} status: {stat}")
		time.sleep(1)
		obj.update_status(ids, stat)


