# app/controllers/inbursa.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from app.core.CRUD import CRUD
from app.models.Inbursa import InbursaRecord, UploadResponse
import pandas as pd
import io
from datetime import datetime
from typing import Optional, List
import logging
from sqlalchemy.orm import Session

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/inbursa",
    tags=["Inbursa Files"]
)

def clean_numeric_value(value):
    """Limpia valores numéricos, convierte strings vacíos a None"""
    if pd.isna(value) or value == '' or value == '""':
        return None
    if isinstance(value, str):
        # Remover comillas, espacios, y comas de miles
        value = value.strip().replace('"', '').replace(',', '')
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

def parse_date(date_str):
    """Parsea fecha en formato DD/MM/YYYY"""
    if pd.isna(date_str) or date_str == '':
        return None
    if isinstance(date_str, str):
        try:
            # Intentar parsear fecha en formato DD/MM/YYYY
            return datetime.strptime(date_str.strip(), '%d/%m/%Y').date()
        except ValueError:
            # Intentar otros formatos comunes
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']:
                try:
                    return datetime.strptime(date_str.strip(), fmt).date()
                except ValueError:
                    continue
            logger.warning(f"No se pudo parsear la fecha: {date_str}")
            return None
    return date_str

def extract_account_number_from_header(file_contents):
    """Extrae el número de cuenta del header del archivo Excel"""
    try:
        # Leer las primeras 3 filas que contienen el header
        header_df = pd.read_excel(io.BytesIO(file_contents), engine='openpyxl', nrows=3)
        
        # Buscar el número de cuenta en las primeras filas
        for col in header_df.columns:
            for row in header_df.iterrows():
                cell_value = str(row[1][col])
                if 'cuenta' in cell_value.lower() or 'account' in cell_value.lower():
                    # Extraer número de cuenta usando regex
                    import re
                    match = re.search(r'\d{10,}', cell_value)
                    if match:
                        return match.group()
        return None
    except Exception as e:
        logger.warning(f"Error extrayendo número de cuenta: {str(e)}")
        return None

@router.post("/upload-excel", response_model=UploadResponse)
async def upload_excel(file: UploadFile = File(...)):
    """Endpoint para cargar archivo Excel de Inbursa"""
    
    # Validar que sea un archivo XLSX
    if not file.filename or not file.filename.lower().endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400, 
            detail="El archivo debe ser un Excel válido (.xlsx o .xls)"
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
        
        # Leer archivo Excel
        try:
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl', skiprows=3)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al leer el archivo Excel: {str(e)}"
            )
        
        # Validar que el DataFrame no esté vacío
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="El archivo Excel no contiene datos"
            )
        
        logger.info(f"Archivo recibido: {file.filename}, Filas: {len(df)}")
        logger.info(f"Columnas encontradas: {list(df.columns)}")
        
        # Mapeo de columnas Excel a modelo (basado en la imagen)
        column_mapping = {
            'Fecha': 'movement_date',
            'Referencia': 'reference',
            'Referencia Ext.': 'ext_reference',
            'Referencia Leyenda': 'legend_reference',
            'Referencia Numérica': 'numeric_reference',
            'Concepto': 'concept',
            'Movimiento': 'motion',
            'Cargo': 'charge',
            'Abono': 'payment',
            'Saldo': 'balance',
            'Ordenante': 'payer',
            'RFC Ordenante': 'rfc_payer',
        }
        
        # Columnas numéricas
        numeric_columns = {
            'numeric_reference', 'charge', 'payment', 'balance'
        }
        
        # Columnas de texto
        text_columns = {
            'reference', 'ext_reference', 'legend_reference', 'concept', 'motion', 'payer', 'rfc_payer'
        }
        
        # Columnas de fecha
        date_columns = {
            'movement_date'
        }
        
        # Validar columnas requeridas
        required_columns = ['Fecha']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Columnas requeridas faltantes: {', '.join(missing_columns)}"
            )
        
        # Extraer número de cuenta del header
        account_number = extract_account_number_from_header(contents)
        
        # Inicializar CRUD
        model = InbursaRecord
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
                for excel_col, db_col in column_mapping.items():
                    if excel_col in df.columns:
                        if db_col in numeric_columns:
                            record_data[db_col] = clean_numeric_value(row[excel_col])
                        elif db_col in text_columns:
                            record_data[db_col] = clean_string_value(row[excel_col])
                        elif db_col in date_columns:
                            record_data[db_col] = parse_date(row[excel_col])
                
                # Agregar número de cuenta si está disponible
                if account_number:
                    record_data['account_number'] = account_number
                
                # Validar que al menos tengamos fecha
                if not record_data.get('movement_date'):
                    errors.append(f"Fila {index + 1}: Fecha requerida")
                    continue
                
                # Crear instancia del modelo
                inbursa_record = InbursaRecord(**record_data)
                
                # Agregar a la base de datos
                db.add(inbursa_record)
                records_inserted += 1
                
                # Commit cada 100 registros para optimizar
                if records_inserted % 100 == 0:
                    db.commit()
                    logger.info(f"Procesados {records_inserted} registros")
                    
            except Exception as e:
                error_msg = f"Error procesando fila {index + 1}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                # No hacer rollback aquí para no perder los registros anteriores
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
        if db:
            db.rollback()
        raise
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error procesando archivo: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )
    finally:
        if db:
            db.close()

@router.get("/records")
async def get_records(page_size: int = 10, current_page: int = 1, filter: Optional[str] = None):
    """Obtener registros de Inbursa con paginación"""
    try:
        # Validar parámetros
        if page_size <= 0 or page_size > 1000:
            raise HTTPException(status_code=400, detail="page_size debe estar entre 1 y 1000")
        if current_page <= 0:
            raise HTTPException(status_code=400, detail="current_page debe ser mayor a 0")
        
        model = InbursaRecord
        crud = CRUD(model)

        rows = crud.get_paginated(page_size, current_page, filter)
        
        return {
            "data": rows[0],
            "total_rows": rows[1],
            "page_size": page_size,
            "current_page": current_page,
            "total_pages": (rows[1] + page_size - 1) // page_size
        }
    except Exception as e:
        logger.error(f"Error obteniendo registros: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/records/count")
async def get_records_count():
    """Obtener el conteo total de registros"""
    try:
        model = InbursaRecord
        crud = CRUD(model)
        rows = crud.get_count()
        return {"total_rows": rows}
    except Exception as e:
        logger.error(f"Error obteniendo conteo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/records/search")
async def search_records(
    account_no: Optional[str] = None, 
    reference: Optional[str] = None,
    concept: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100
):
    """Buscar registros por diferentes criterios"""
    try:
        # Validar parámetros
        if limit <= 0 or limit > 1000:
            raise HTTPException(status_code=400, detail="limit debe estar entre 1 y 1000")
        if skip < 0:
            raise HTTPException(status_code=400, detail="skip debe ser mayor o igual a 0")
        
        model = InbursaRecord
        crud = CRUD(model)

        # Construir filtros
        filters = {}
        if account_no:
            filters['account_number'] = account_no
        if reference:
            filters['reference'] = reference
        if concept:
            filters['concept'] = concept
        if date_from:
            filters['date_from'] = date_from
        if date_to:
            filters['date_to'] = date_to

        # Implementar búsqueda en CRUD (necesitarás implementar este método)
        # results = crud.search_records(filters, skip, limit)
        
        return {
            "message": "Endpoint de búsqueda - implementar filtros específicos en CRUD",
            "params": {
                "account_no": account_no,
                "reference": reference,
                "concept": concept,
                "date_from": date_from,
                "date_to": date_to,
                "skip": skip,
                "limit": limit
            }
        }
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/records/truncate")
async def truncate_records(confirm: bool = False):
    """Eliminar todos los registros (usar con precaución)"""
    try:
        if not confirm:
            raise HTTPException(
                status_code=400, 
                detail="Para confirmar la eliminación, envíe confirm=true"
            )
        
        model = InbursaRecord
        crud = CRUD(model)
        
        # Implementar truncate en CRUD con confirmación
        # deleted_count = crud.truncate_table()
        
        return {
            "message": "Endpoint de truncate - implementar con confirmación de seguridad",
            "warning": "Esta operación eliminará TODOS los registros"
        }
    except Exception as e:
        logger.error(f"Error truncando registros: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/records/{record_id}")
async def get_record_by_id(record_id: int):
    """Obtener un registro específico por ID"""
    try:
        model = InbursaRecord
        crud = CRUD(model)
        
        record = crud.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        return record
    except Exception as e:
        logger.error(f"Error obteniendo registro {record_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/records/{record_id}")
async def delete_record(record_id: int):
    """Eliminar un registro específico"""
    try:
        model = InbursaRecord
        crud = CRUD(model)
        
        success = crud.delete_by_id(record_id)
        if not success:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        return {"message": f"Registro {record_id} eliminado exitosamente"}
    except Exception as e:
        logger.error(f"Error eliminando registro {record_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Inbursa Upload Service"
    }
