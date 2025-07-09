# app/api/v1/__init__.py
from fastapi import APIRouter
from importlib import import_module
from pathlib import Path
from typing import List

def get_routers()->List[APIRouter]:
	"""
	Cargar dinamicamente todos los routes en el directorio v1
	"""
	routers = []
	current_dir = Path(__file__).parent
	# Excluye __init__.py y __pycache__
	for route_file in current_dir.glob('*.py'):
		if route_file.stem not in ['__init__']:
			# Convierte el path a formato de modulo
			module_path = f"app.api.v1.{route_file.stem}"
			# importa el modulo
			module = import_module(module_path)
			# busca el router en el modulo
			if hasattr(module, 'router'):
				routers.append(module.router)

	return routers
