# app/core/logger_config.py

import logging

def setup_logger():
	"""Configura y devuelve el logger."""

	# Crear un logger
	logger = logging.getLogger('api_logger')
	logger.setLevel(logging.DEBUG)

	# Si ya tiene handlers, evita duplicados
	if not logger.hasHandlers():
		# Crear una handler para escribir los logs en un archivo
		file_handler = logging.FileHandler('api.log')

		# Crear un formateador y asignarlo al handler
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		file_handler.setFormatter(formatter)

		# Agregar el handler al logger
		logger.addHandler(file_handler)

	return logger

# Configurar el logger al importar este módulo
setup_logger()
