import axios from 'axios';
import * as XLSX from 'xlsx';
import { useState, useEffect, useCallback } from 'react';
import { Upload, Database, CheckCircle, AlertCircle, FileText, Settings, X, Eye, Trash2 } from 'lucide-react';

// Importaciones de Material UI agrupadas
import {
  Box, Card, Paper, Table, Button, TableBody, Typography, TableContainer, TablePagination
} from '@mui/material';

// Importaciones del layout
import { DashboardContent } from 'src/layouts/dashboard';

// Importaciones de componentes
import { Iconify } from 'src/components/iconify';
import { Scrollbar } from 'src/components/scrollbar';

// API
import ApiService from '../../../../api/api.service';

// ----------------------------------------------------------------------

interface Info {
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
}

interface UploadHistoryItem {
  id: number;
  filename: string;
  timestamp: string;
  records: number;
  status: 'success' | 'error' | 'processing';
}

interface UploadResponse {
  records_inserted: number;
  detail?: string;
}

export function InbursaView() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<Info | null>(null);
  const [previewData, setPreviewData] = useState<string[][]>([]);
  const [showPreview, setShowPreview] = useState(false);
  const [uploadHistory, setUploadHistory] = useState<UploadHistoryItem[]>([]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      // Validar que sea un archivo Excel
      const validExtensions = ['.xlsx', '.xls'];
      const fileExtension = selectedFile.name.toLowerCase().slice(selectedFile.name.lastIndexOf('.'));
      
      if (validExtensions.includes(fileExtension)) {
        setFile(selectedFile);
        setUploadStatus(null);
        previewFile(selectedFile);
      } else {
        setUploadStatus({
          type: 'error',
          message: 'Por favor selecciona un archivo Excel válido (.xlsx, .xls)'
        });
      }
    }
  };

  const previewFile = useCallback((selectedFile: File) => {
    const reader = new FileReader();
    
    reader.onload = (e: ProgressEvent<FileReader>) => {
      try {
        const data = e.target?.result;
        if (!data) return;

        // Leer el archivo Excel
        const workbook = XLSX.read(data, { type: 'array' });
        
        // Obtener la primera hoja
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        
        // Convertir a array de arrays
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { 
          header: 1, 
          raw: false,
          defval: '' 
        }) as string[][];
        
        // Tomar solo las primeras 6 filas (header + 5 filas de datos)
        const previewRows = jsonData.slice(0, 6);
        
        // Filtrar filas completamente vacías
        const filteredRows = previewRows.filter(row => 
          row.some(cell => cell && cell.toString().trim() !== '')
        );
        
        setPreviewData(filteredRows);
        
      } catch (error) {
        console.error('Error reading Excel file:', error);
        setUploadStatus({
          type: 'error',
          message: 'Error al leer el archivo Excel. Verifica que el archivo no esté corrupto.'
        });
      }
    };
    
    reader.onerror = (error) => {
      console.error('Error reading file:', error);
      setUploadStatus({
        type: 'error',
        message: 'Error al leer el archivo'
      });
    };
    
    reader.readAsArrayBuffer(selectedFile);
  }, []);

  const uploadFile = async () => {
    if (!file) return;

    setUploading(true);
    setUploadStatus(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post<UploadResponse>(
        'http://127.0.0.1:8000/v1/inbursa/upload-excel', 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 60000, // 60 segundos timeout
        }
      );

      const result = response.data;

      if (response.status === 200 && result.records_inserted !== undefined) {
        setUploadStatus({
          type: 'success',
          message: `Archivo cargado exitosamente. ${result.records_inserted} registros insertados.`
        });
        
        // Agregar al historial
        const newHistoryItem: UploadHistoryItem = {
          id: Date.now(),
          filename: file.name,
          timestamp: new Date().toLocaleString('es-MX'),
          records: result.records_inserted,
          status: 'success'
        };
        
        setUploadHistory(prev => [newHistoryItem, ...prev]);
        
        // Limpiar estado
        clearFile();
      } else {
        setUploadStatus({
          type: 'error',
          message: result.detail || 'Error al cargar el archivo'
        });
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      
      let errorMessage = 'Error de conexión con el servidor';
      
      if (axios.isAxiosError(error)) {
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response?.status) {
          errorMessage = `Error ${error.response.status}: ${error.response.statusText}`;
        } else if (error.request) {
          errorMessage = 'No se pudo conectar con el servidor';
        } else if (error.code === 'ECONNABORTED') {
          errorMessage = 'Timeout: La operación tardó demasiado tiempo';
        }
      }
      
      setUploadStatus({
        type: 'error',
        message: errorMessage
      });
    } finally {
      setUploading(false);
    }
  };

  const removeFromHistory = useCallback((id: number) => {
    setUploadHistory(prev => prev.filter(item => item.id !== id));
  }, []);

  const clearFile = useCallback(() => {
    setFile(null);
    setPreviewData([]);
    setShowPreview(false);
    setUploadStatus(null);
    
    // Limpiar el input file
    const fileInput = document.getElementById('excel-file-input') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }, []);

  const dismissStatus = useCallback(() => {
    setUploadStatus(null);
  }, []);

  return (
    <DashboardContent>
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Carga de Archivos Inbursa
        </h1>

        {/* Card de carga */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Seleccionar Archivo Excel
          </h2>
          
          <div className="mb-4">
            <input
              accept=".xlsx,.xls"
              className="hidden"
              id="excel-file-input"
              type="file"
              onChange={handleFileSelect}
              disabled={uploading}
            />
            <label htmlFor="excel-file-input">
              <div className={`inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 cursor-pointer transition-colors ${
                uploading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-50'
              }`}>
                <Upload className="w-4 h-4 mr-2" />
                Seleccionar Archivo Excel
              </div>
            </label>
            
            {file && (
              <div className="inline-flex items-center ml-4 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                <FileText className="w-4 h-4 mr-2" />
                <span className="mr-2">{file.name}</span>
                <button
                  onClick={clearFile}
                  className="text-blue-600 hover:text-blue-800 transition-colors"
                  disabled={uploading}
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>

          {previewData.length > 0 && (
            <div className="mb-4">
              <button
                onClick={() => setShowPreview(true)}
                className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm transition-colors"
                disabled={uploading}
              >
                <Eye className="w-4 h-4 mr-1" />
                Vista Previa ({Math.max(0, previewData.length - 1)} filas)
              </button>
            </div>
          )}

          <div className="flex items-center space-x-4">
            <button
              onClick={uploadFile}
              disabled={!file || uploading}
              className={`inline-flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                !file || uploading
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {uploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"/>
                  Cargando...
                </>
              ) : (
                <>
                  <Database className="w-4 h-4 mr-2" />
                  Cargar a Base de Datos
                </>
              )}
            </button>
            
            {uploading && (
              <div className="flex-1">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full animate-pulse w-3/4"/>
                </div>
              </div>
            )}
          </div>

          {uploadStatus && (
            <div className={`mt-4 p-4 rounded-md ${
              uploadStatus.type === 'success' 
                ? 'bg-green-50 text-green-800 border border-green-200' 
                : 'bg-red-50 text-red-800 border border-red-200'
            }`}>
              <div className="flex items-center">
                {uploadStatus.type === 'success' ? (
                  <CheckCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                )}
                <span className="flex-1">{uploadStatus.message}</span>
                <button
                  onClick={dismissStatus}
                  className="ml-2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Historial de cargas */}
        {uploadHistory.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Historial de Cargas
            </h2>
            
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Archivo
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fecha/Hora
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Registros
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Estado
                    </th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {uploadHistory.map((item: UploadHistoryItem) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <div className="flex items-center">
                          <FileText className="w-4 h-4 mr-2 text-gray-400" />
                          <span title={item.filename}>{item.filename}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {item.timestamp}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                        {item.records.toLocaleString('es-ES')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          item.status === 'success' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {item.status === 'success' ? (
                            <CheckCircle className="w-3 h-3 mr-1" />
                          ) : (
                            <AlertCircle className="w-3 h-3 mr-1" />
                          )}
                          {item.status === 'success' ? 'Exitoso' : 'Error'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-center">
                        <button
                          onClick={() => removeFromHistory(item.id)}
                          className="text-red-600 hover:text-red-800 p-1 rounded transition-colors"
                          title="Eliminar del historial"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Modal de vista previa */}
        {showPreview && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-hidden">
              <div className="flex items-center justify-between p-6 border-b">
                <h3 className="text-lg font-semibold">Vista Previa del Archivo Excel</h3>
                <button
                  onClick={() => setShowPreview(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              
              <div className="p-6 overflow-auto" style={{ maxHeight: 'calc(90vh - 140px)' }}>
                <div className="mb-4 text-sm text-gray-600">
                  Mostrando las primeras {Math.max(0, previewData.length - 1)} filas del archivo: <strong>{file?.name}</strong>
                </div>
                
                {previewData.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200 text-xs">
                      <thead className="bg-gray-50">
                        <tr>
                          {previewData[0]?.map((header: string, index: number) => (
                            <th key={index} className="px-3 py-2 text-left font-medium text-gray-500 uppercase tracking-wider">
                              {header || `Columna ${index + 1}`}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {previewData.slice(1).map((row: string[], rowIndex: number) => (
                          <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                            {row.map((cell: string, cellIndex: number) => (
                              <td key={cellIndex} className="px-3 py-2 whitespace-nowrap text-gray-900">
                                <div title={cell?.toString()} className="truncate max-w-xs">
                                  {cell && cell.toString().length > 30 ? `${cell.toString().substring(0, 30)}...` : cell}
                                </div>
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    No hay datos para mostrar
                  </div>
                )}
              </div>
              
              <div className="flex justify-between items-center p-6 border-t">
                <div className="text-sm text-gray-500">
                  Total de columnas: {previewData[0]?.length || 0}
                </div>
                <button
                  onClick={() => setShowPreview(false)}
                  className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardContent>
  );
}

export default InbursaView;