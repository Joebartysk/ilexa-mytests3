# app/models/CCodigoPostal.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CodigoPostal(Base):
	__tablename__ = "c_codigopostal"
	__table_args__ = {"schema": "cfdi_system"}

	# Columnas de la tabla
	id = Column(Integer, primary_key=True, autoincrement=True)
	c_codigopostal = Column(Integer, name="c_CodigoPostal")
	c_estado = Column(String(50), nullable=True, name="c_Estado")
	c_municipio = Column(Integer, nullable=True, name="c_Municipio")
	c_localidad = Column(Integer, nullable=True, name="c_Localidad")
	estimulo_franja_fronteriza = Column(Integer, nullable=True, name="Estimulo_Franja_Fronteriza")
	fecha_inicio_de_vigencia = Column(String(50), nullable=True, name="Fecha_inicio_de_vigencia")
	fecha_fin_de_vigencia = Column(String(50), nullable=True, name="Fecha_fin_de_vigencia")
	descripcion_del_huso_horario = Column(String(50), nullable=True, name="Descripcion_del_Huso_Horario")
	mes_inicio_horario_verano = Column(String(50), nullable=True, name="Mes_Inicio_Horario_Verano")
	dia_inicio_horario_verano = Column(String(50), nullable=True, name="Dia_Inicio_Horario_Verano")
	dia_inicio_horario_verano_1 = Column(String(50), nullable=True, name="Dia_Inicio_Horario_Verano_1")
	diferencia_horaria_verano = Column(Integer, nullable=True, name="Diferencia_Horaria_Verano")
	mes_inicio_horario_invierno = Column(String(50), nullable=True, name="Mes_Inicio_Horario_Invierno")
	dia_inicio_horario_invierno = Column(String(50), nullable=True, name="Dia_Inicio_Horario_Invierno")
	dia_inicio_horario_invierno_1 = Column(String(50), nullable=True, name="Dia_Inicio_Horario_Invierno_1")
	diferencia_horaria_invierno = Column(Integer, nullable=True, name="Diferencia_Horaria_Invierno")
