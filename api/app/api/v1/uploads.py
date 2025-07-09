# app/controllers/uploads.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.core.CRUD import CRUD
from app.models.HSBC import HSBCRecord, UploadResponse
import pandas as pd
import io
from datetime import datetime
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/hsbc",
    tags=["Uploads Files"]
)

def clean_numeric_value(value):
    """Limpia valores numéricos, convierte strings vacíos a None"""
    if pd.isna(value) or value == '' or value == '""':
        return None
    if isinstance(value, str):
        # Remover comillas y espacios
        value = value.strip().replace('"', '')
        if value == '':
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

@router.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    """Endpoint para cargar archivo CSV de HSBC"""
    
    # Validar que sea un archivo CSV (case insensitive)
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400, 
            detail="El archivo debe ser un CSV válido"
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
                df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
            except UnicodeDecodeError:
                # Si falla, intentar con latin-1
                df = pd.read_csv(io.StringIO(contents.decode('latin-1')))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al leer el archivo CSV: {str(e)}"
            )
        
        # Validar que el DataFrame no esté vacío
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="El archivo CSV no contiene datos"
            )
        
        logger.info(f"Archivo recibido: {file.filename}, Filas: {len(df)}")
        logger.info(f"Columnas: {list(df.columns)}")
        
        # Mapeo de columnas CSV a modelo
        column_mapping = {
            'UNIQUE_ID': 'unique_id',
            'ASOFDATE': 'asofdate',
            'ASOFTIME': 'asoftime',
            'INTRAEND': 'intraend',
            'CCYCODE': 'ccycode',
            'CCYCODETYP': 'ccycodetyp',
            'ACCOUNTTYPE': 'accounttype',
            'ACCOUNTNO': 'accountno',
            'BRANCHID': 'branchid',
            'INSTTID': 'insttid',
            'USCHIPSID': 'uschipsid',
            'XITROUTNUM': 'xitroutnum',
            'ACCNAME': 'accname',
            'UKSORTCDE': 'uksortcde',
            'ENTRYDATE': 'entrydate',
            'LEDGERBALA': 'ledgerbala',
            'OPENAVLBAL': 'openavlbal',
            'OPENBAL': 'openbal',
            'CLEAREDBAL': 'clearedbal',
            'ADJUSTBAL': 'adjustbal',
            'DEPOSITBAL': 'depositbal',
            'TOTALFLOAT': 'totalfloat',
            'SAVAVAIL': 'savavail',
            'ONEDAYFLOA': 'onedayfloa',
            'TWODAYFLOA': 'twodayfloa',
            '>3DAYFLOAT': 'threedayfloa',
            'TOTAL_CRED': 'total_cred',
            'NOOFCREDIT': 'noofcredit',
            'AUTOCRCLEA': 'autocrclea',
            'TOTAL_DEBI': 'total_debi',
            'NOOFDEBITS': 'noofdebits',
            'AUTODRCLEA': 'autodrclea',
            'HOCOLLECTI': 'hocollecti',
            'CREDITFAC': 'creditfac',
            'INTACCR': 'intaccr',
            'INTRATE': 'intrate',
            'XACTTYPE': 'xacttype',
            'VAL_DATE': 'val_date',
            'XACTTIME': 'xacttime',
            'STMTDATE': 'stmtdate',
            'FIELDAMOUN': 'fieldamoun',
            'TEXTLINE1': 'textline1',
            'TEXTLINE2': 'textline2',
            'TEXTLINE3': 'textline3',
            'TEXTLINE4': 'textline4',
            'TEXTLINE5': 'textline5',
            'TEXTLINE6': 'textline6',
            'TEXTLINE7': 'textline7',
            'TEXTLINE8': 'textline8',
            'TEXTLINE9': 'textline9',
            'TEXTLINE10': 'textline10',
            'TEXTLINE11': 'textline11',
            'TEXTLINE12': 'textline12',
            'TEXTLINE13': 'textline13',
            'HOLDAMT': 'holdamt'
        }
        
        # Columnas numéricas
        numeric_columns = {
            'ledgerbala', 'openavlbal', 'openbal', 'clearedbal', 'adjustbal',
            'depositbal', 'totalfloat', 'savavail', 'onedayfloa', 'twodayfloa',
            'threedayfloa', 'total_cred', 'autocrclea', 'total_debi', 'autodrclea',
            'hocollecti', 'creditfac', 'intaccr', 'intrate', 'fieldamoun', 'holdamt'
        }
        
        # Columnas de texto
        text_columns = {
            'unique_id', 'asofdate', 'asoftime', 'intraend', 'ccycode', 'ccycodetyp',
            'accounttype', 'accountno', 'branchid', 'insttid', 'uschipsid', 'xitroutnum',
            'accname', 'uksortcde', 'entrydate', 'noofcredit', 'noofdebits', 'xacttype',
            'val_date', 'xacttime', 'stmtdate', 'textline1', 'textline2', 'textline3',
            'textline4', 'textline5', 'textline6', 'textline7', 'textline8', 'textline9',
            'textline10', 'textline11', 'textline12', 'textline13'
        }
        
        # Validar columnas requeridas
        required_columns = ['UNIQUE_ID', 'ACCOUNTNO']  # Agregar las columnas que consideres obligatorias
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Columnas requeridas faltantes: {', '.join(missing_columns)}"
            )
        
        # Inicializar CRUD
        model = HSBCRecord
        crud = CRUD(model)
        db = crud.session_manager.get_session()
        
        records_inserted = 0
        errors = []
        
        # Procesar cada fila
        for index, row in df.iterrows():
            try:
                # Crear diccionario con datos limpios
                record_data = {}
                
                # Procesar columnas según el mapeo
                for csv_col, db_col in column_mapping.items():
                    if csv_col in df.columns:
                        if db_col in numeric_columns:
                            record_data[db_col] = clean_numeric_value(row[csv_col])
                        elif db_col in text_columns:
                            record_data[db_col] = clean_string_value(row[csv_col])
                
                # Crear instancia del modelo
                hsbc_record = HSBCRecord(**record_data)  # Usar ** para desempaquetar
                
                # Agregar a la base de datos
                db.add(hsbc_record)
                records_inserted += 1
                
                # Commit cada 100 registros para optimizar
                if records_inserted % 100 == 0:
                    db.commit()
                    logger.info(f"Procesados {records_inserted} registros")
                    
            except Exception as e:
                error_msg = f"Error procesando fila {index + 1}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                db.rollback()  # Rollback solo de la transacción actual
                continue
        
        # Commit final
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
    """Obtener registros de HSBC con paginación"""
    try:
        model = HSBCRecord
        crud = CRUD(model)

        rows = crud.get_paginated(page_size, current_page, filter)
        print(rows)

        return {
            "data": rows[0],
            "total_rows": rows[1],
            "page_size": page_size,
            "current_page": current_page
        }
    except Exception as e:
        logger.error(f"Error obteniendo registros: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/records/count")
async def get_records_count():
    """Obtener el conteo total de registros"""
    try:
        model = HSBCRecord
        crud = CRUD(model)

        rows = crud.get_count()
        return {
            "total_rows": rows
        }
    except Exception as e:
        logger.error(f"Error obteniendo conteo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/records/search")
async def search_records(
    account_no: Optional[str] = None, 
    account_name: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100
):
    """Buscar registros por número de cuenta o nombre"""
    try:
        model = HSBCRecord
        crud = CRUD(model)
        
        # Aquí necesitarías implementar la búsqueda en tu clase CRUD
        # Por ahora devolvemos un placeholder
        return {
            "message": "Endpoint de búsqueda - implementar en CRUD",
            "params": {
                "account_no": account_no,
                "account_name": account_name,
                "skip": skip,
                "limit": limit
            }
        }
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/records/truncate")
async def truncate_records():
    """Eliminar todos los registros (usar con precaución)"""
    try:
        model = HSBCRecord
        crud = CRUD(model)
        
        # Implementar truncate en tu clase CRUD
        # Por ahora devolvemos un placeholder
        return {
            "message": "Endpoint de truncate - implementar en CRUD con precaución"
        }
    except Exception as e:
        logger.error(f"Error truncando registros: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "service": "HSBC Upload Service"
    }