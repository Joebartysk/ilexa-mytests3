# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import Settings
from app.api.v1 import get_routers
from app.core.logger_config import setup_logger
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
# Obtener el logger configurado
logger = setup_logger()
# Incicializamos configuracion
settings = Settings()

def create_app() -> FastAPI:
	# Crear aplicación FastAPI con configuraciones personalizadas
	app = FastAPI(
		title="Api SAT",
		description="Api Consumption Web Service SAT",
		version="0.7.0"
	)

	# Configuración CORS
	app.add_middleware(
		CORSMiddleware,
		allow_origins=[settings.ALLOW_ORIGINS], # Cambiar en produccion para especificar los origenes permitidos
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.mount("/static", StaticFiles(directory="static"), name="static")
	# Ruta base
	@app.get('/')
	def initial():
		return f"Hello World!"

	# cargar dinamicamente todos los routers
	for router in get_routers():
		app.include_router(router, prefix="/v1")
		logger.info(f"Router cargado: {router.prefix}")

	return app

# crear la instancia de la aplicacion
app = create_app()

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(settings.NAME_APP, host=settings.HOSTING, port=settings.PORT, reload=settings.RELOAD)
