# app/controllers/export_file.py
print("Content-type: text/html")
from fastapi import APIRouter, HTTPException, Depends, Query, Request, Response
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime
from app.services.ExportCSV import export_CSV
from app.services.ExportXLSX import ExportXLSX

router = APIRouter(
	prefix="/export",
	tags=["Export data to files"]
)

@router.get("/export-file-csv", include_in_schema=False)
async def export_file(filename: str, schema: str, table: str):
	try:
		# Generate filename with timestamp
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		filename = f"{timestamp}_{filename}"
		
		# Create CSV export
		exporter = export_CSV(filename, schema, table)
		file_path = exporter.main()
		
		# Get file info
		file_size = Path(file_path).stat().st_size
		actual_filename = Path(file_path).name
		
		return {
			"success": True,
			"message": "CSV file created successfully",
			"filename": actual_filename,
			"download_url": f"/static/{actual_filename}",
			"full_download_url": f"http://localhost:8000/static/{actual_filename}",
			"file_size": file_size,
			"file_type": "csv",
			"path": file_path,
			"created_at": datetime.now().isoformat()
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error creating CSV file: {str(e)}")

@router.get("/export-file-xlsx", include_in_schema=False)
async def export_xlsx(filename: str, schema: str, table: str):
	try:
		# Generate filename with timestamp
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		filename = f"{timestamp}_{filename}"
		#filename = '20250623_222907_joel'
		
		# Create Excel export
		exporter = ExportXLSX(filename, schema, table)
		file_path = exporter.main()
		
		# Get file info
		file_size = Path(file_path).stat().st_size
		actual_filename = Path(file_path).name
		
		return {
			"success": True,
			"message": "Excel file created successfully",
			"filename": actual_filename,
			"download_url": f"/static/{actual_filename}",
			"full_download_url": f"http://localhost:8000/static/{actual_filename}",
			"file_size": file_size,
			"file_type": "xlsx",
			"path": file_path,
			"created_at": datetime.now().isoformat()
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error creating Excel file: {str(e)}")
