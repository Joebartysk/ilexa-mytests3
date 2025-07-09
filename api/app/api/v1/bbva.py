# app/controllers/bbva.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.core.CRUD import CRUD
from app.models.BBVA import BBVARecord, UploadResponse
import pandas as pd
import io
from datetime import datetime
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/bbva",
    tags=["Uploads Files"]
)

def clean_numeric_value(value):
    """Limpia valores numéricos, convierte strings vacíos a None"""
    if pd.isna(value) or value == '' or value == '""':
        return None
    if isinstance(value, str):
        # Remover comillas, espacios y caracteres especiales de formato mexicano
        value = value.strip().replace('"', '').replace(',', '').replace('$', '')
        if value == '' or value == '-':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    return float(value) if value is not None else None

def clean_string_value(value):
    """Limpia valores de string"""
    if pd.isna(value) or value == '':
        return None
    if isinstance(value, str):
        cleaned = value.strip().replace('"', '')
        return cleaned if cleaned else None
    return str(value) if value is not None else None

def parse_date(date_str):
    """Parsea fecha en formato español/mexicano"""
    if pd.isna(date_str) or date_str == '':
        return None
    
    try:
        # Limpiar el string
        date_str = str(date_str).strip().replace('"', '')
        
        # Intentar diferentes formatos comunes
        formats = [
            '%d/%m/%Y',  # 31/12/2024
            '%d-%m-%Y',  # 31-12-2024
            '%Y-%m-%d',  # 2024-12-31
            '%d/%m/%y',  # 31/12/24
            '%d-%m-%y',  # 31-12-24
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # Si no funciona ningún formato, retornar None
        logger.warning(f"No se pudo parsear la fecha: {date_str}")
        return None
        
    except Exception as e:
        logger.error(f"Error parseando fecha {date_str}: {str(e)}")
        return None

@router.post("/upload-txt", response_model=UploadResponse)
async def upload_txt(file: UploadFile = File(...)):
    """Endpoint para cargar archivo TXT de BBVA"""
    
    # Validar que sea un archivo TXT (case insensitive)
    if not file.filename or not file.filename.lower().endswith('.txt'):
        raise HTTPException(
            status_code=400, 
            detail="El archivo debe ser un TXT válido"
        )
    
    db = None
    try:
        # Leer contenido del archivo
        contents = await file.read()
        
        # Validar que el archivo no esté vacío
        if not contents:
            raise HTTPException(
                status_code=400,
                detail="El archivo está vacío"
            )
        
        # Convertir a DataFrame con mejor manejo de encoding
        try:
            # Intentar UTF-8 primero
            try:
                # Usar separador de tabulación para archivos TXT de BBVA
                df = pd.read_csv(
                    io.StringIO(contents.decode('utf-8')), 
                    sep='\t',  # Separador por tabulación
                    encoding='utf-8'
                )
            except UnicodeDecodeError:
                # Si falla, intentar con latin-1
                df = pd.read_csv(
                    io.StringIO(contents.decode('latin-1')), 
                    sep='\t',
                    encoding='latin-1'
                )
        except Exception as e:
            # Si falla con tabulación, intentar con coma
            try:
                df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
            except UnicodeDecodeError:
                df = pd.read_csv(io.StringIO(contents.decode('latin-1')))
        
        # Validar que el DataFrame no esté vacío
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="El archivo TXT no contiene datos"
            )
        
        logger.info(f"Archivo recibido: {file.filename}, Filas: {len(df)}")
        logger.info(f"Columnas detectadas: {list(df.columns)}")
        
        # Mapeo de columnas TXT a modelo (más flexible)
        column_mapping = {
            'Día': 'movement_date',
            'Dia': 'movement_date',
            'Fecha': 'movement_date',
            'Concepto / Referencia': 'concept_reference',
            'Concepto': 'concept_reference',
            'Referencia': 'concept_reference',
            'Cargo': 'charge',
            'cargo': 'charge',
            'Abono': 'payment',
            'abono': 'payment',
            'Saldo': 'balance',
            'saldo': 'balance',
        }
        
        # Detectar columnas automáticamente
        detected_mapping = {}
        for col in df.columns:
            if col in column_mapping:
                detected_mapping[col] = column_mapping[col]
        
        if not detected_mapping:
            raise HTTPException(
                status_code=400,
                detail=f"No se detectaron columnas válidas. Columnas encontradas: {list(df.columns)}"
            )
        
        logger.info(f"Mapeo detectado: {detected_mapping}")
        
        # Columnas numéricas
        numeric_columns = {'charge', 'payment', 'balance'}
        
        # Columnas de texto
        text_columns = {'concept_reference'}
        
        # Columnas de fecha
        date_columns = {'movement_date'}
        
        # Inicializar CRUD
        model = BBVARecord
        crud = CRUD(model)
        db = crud.session_manager.get_session()
        
        records_inserted = 0
        errors = []
        
        # Procesar cada fila
        for index, row in df.iterrows():
            try:
                # Crear diccionario con datos limpios
                record_data = {}
                
                # Procesar columnas según el mapeo detectado
                for txt_col, db_col in detected_mapping.items():
                    if txt_col in df.columns:
                        if db_col in numeric_columns:
                            record_data[db_col] = clean_numeric_value(row[txt_col])
                        elif db_col in text_columns:
                            record_data[db_col] = clean_string_value(row[txt_col])
                        elif db_col in date_columns:
                            record_data[db_col] = parse_date(row[txt_col])
                
                # Validar que tengamos al menos algunos datos
                if not any(record_data.values()):
                    logger.warning(f"Fila {index + 1} sin datos válidos, omitiendo")
                    continue
                
                # Crear instancia del modelo
                bbva_record = BBVARecord(**record_data)
                
                # Agregar a la base de datos
                db.add(bbva_record)
                records_inserted += 1
                
                # Commit cada 100 registros para optimizar
                if records_inserted % 100 == 0:
                    db.commit()
                    logger.info(f"Procesados {records_inserted} registros")
                    
            except Exception as e:
                error_msg = f"Error procesando fila {index + 1}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                # No hacer rollback aquí, solo continuar
                continue
        
        # Commit final
        if records_inserted > 0:
            db.commit()
        
        logger.info(f"Carga completada: {records_inserted} registros insertados")
        
        # Preparar mensaje de respuesta
        message = f"Archivo procesado exitosamente. {records_inserted} registros insertados."
        if errors:
            message += f" Se encontraron {len(errors)} errores en el procesamiento."
        
        return UploadResponse(
            success=True,
            records_inserted=records_inserted,
            message=message,
            filename=file.filename
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions para mantener el status code
        if db:
            db.rollback()
        raise
    except Exception as e:
        # Rollback en caso de error
        if db:
            db.rollback()
        logger.error(f"Error procesando archivo: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )
    finally:
        # Asegurar que la sesión se cierre
        if db:
            db.close()

@router.get("/records")
async def get_records(page_size: int = 10, current_page: int = 1, filter: Optional[str] = None):
    """Obtener registros de BBVA con paginación"""
    db = None
    try:
        model = BBVARecord
        crud = CRUD(model)
        db = crud.session_manager.get_session()

        rows = crud.get_paginated(page_size, current_page, filter)
        
        return {
            "data": rows[0],
            "total_rows": rows[1],
            "page_size": page_size,
            "current_page": current_page
        }
    except Exception as e:
        logger.error(f"Error obteniendo registros: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if db:
            db.close()

@router.get("/records/count")
async def get_records_count():
    """Obtener el conteo total de registros"""
    db = None
    try:
        model = BBVARecord
        crud = CRUD(model)
        db = crud.session_manager.get_session()

        rows = crud.get_count()
        return {
            "total_rows": rows
        }
    except Exception as e:
        logger.error(f"Error obteniendo conteo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if db:
            db.close()

@router.get("/records/search")
async def search_records(
    concept: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    skip: int = 0, 
    limit: int = 100
):
    """Buscar registros por concepto, fecha o monto"""
    db = None
    try:
        model = BBVARecord
        crud = CRUD(model)
        db = crud.session_manager.get_session()
        
        # Construir filtros
        filters = []
        if concept:
            filters.append(f"concept_reference LIKE '%{concept}%'")
        if date_from:
            filters.append(f"movement_date >= '{date_from}'")
        if date_to:
            filters.append(f"movement_date <= '{date_to}'")
        if min_amount is not None:
            filters.append(f"(charge >= {min_amount} OR payment >= {min_amount})")
        if max_amount is not None:
            filters.append(f"(charge <= {max_amount} OR payment <= {max_amount})")
        
        filter_str = " AND ".join(filters) if filters else None
        
        # Usar paginación con filtros
        rows = crud.get_paginated(limit, skip // limit + 1, filter_str)
        
        return {
            "data": rows[0],
            "total_rows": rows[1],
            "filters_applied": filters,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if db:
            db.close()

@router.delete("/records/truncate")
async def truncate_records():
    """Eliminar todos los registros (usar con precaución)"""
    db = None
    try:
        model = BBVARecord
        crud = CRUD(model)
        db = crud.session_manager.get_session()
        
        # Eliminar todos los registros
        count = db.query(model).count()
        db.query(model).delete()
        db.commit()
        
        return {
            "message": f"Se eliminaron {count} registros exitosamente",
            "records_deleted": count
        }
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error truncando registros: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if db:
            db.close()

@router.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "service": "BBVA Upload Service"
    }