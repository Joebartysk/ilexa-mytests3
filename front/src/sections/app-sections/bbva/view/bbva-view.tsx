import axios from 'axios';
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
  type: string;
  message: string;
}

interface UploadHistoryItem {
  id: number;
  filename: string;
  timestamp: string;
  records: number;
  status: string;
}

interface UploadResponse {
  records_inserted: number;
  detail?: string;
}

export function BBVAView() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<Info | null>(null);
  const [previewData, setPreviewData] = useState<string[][]>([]);
  const [showPreview, setShowPreview] = useState(false);
  const [uploadHistory, setUploadHistory] = useState<UploadHistoryItem[]>([]);
  const [delimiter, setDelimiter] = useState<string>(','); // Delimitador configurable
  const [encoding, setEncoding] = useState<string>('UTF-8'); // Codificación configurable

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile && (selectedFile.type === 'text/plain' || selectedFile.name.endsWith('.txt'))) {
      setFile(selectedFile);
      setUploadStatus(null);
      previewTXT(selectedFile);
    } else {
      setUploadStatus({
        type: 'error',
        message: 'Por favor selecciona un archivo TXT válido'
      });
    }
  };

  const detectDelimiter = (text: string): string => {
    const firstLine = text.split('\n')[0] || '';
    const delimiters = [',', ';', '\t', '|', ' '];
    
    let bestDelimiter = ',';
    let maxColumns = 0;
    
    for (const del of delimiters) {
      const columns = firstLine.split(del).length;
      if (columns > maxColumns) {
        maxColumns = columns;
        bestDelimiter = del;
      }
    }
    
    return bestDelimiter;
  };

  const parseTXTLine = (line: string, delimiters: string): string[] => {
    // Si el delimitador es espacio, dividir por espacios múltiples
    if (delimiter === ' ') {
      return line.trim().split(/\s+/).filter(cell => cell.length > 0);
    }
    
    // Para otros delimitadores, usar lógica de CSV con comillas
    const cells: string[] = [];
    let currentCell = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      
      if (char === '"' && (i === 0 || line[i-1] === delimiter)) {
        inQuotes = true;
      } else if (char === '"' && inQuotes && (i === line.length - 1 || line[i+1] === delimiter)) {
        inQuotes = false;
      } else if (char === delimiter && !inQuotes) {
        cells.push(currentCell.trim());
        currentCell = '';
      } else if (char !== '"' || inQuotes) {
        currentCell += char;
      }
    }
    
    // Agregar la última celda
    if (currentCell || line.endsWith(delimiter)) {
      cells.push(currentCell.trim());
    }
    
    return cells;
  };

  const previewTXT = (selectedFile: File) => {
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      const text = e.target?.result as string;
      
      // Detectar automáticamente el delimitador
      const detectedDelimiter = detectDelimiter(text);
      setDelimiter(detectedDelimiter);
      
      // Dividir en líneas y tomar las primeras 6 (header + 5 filas)
      const lines = text.split('\n').slice(0, 6);
      const parsedData = lines
        .filter(line => line.trim().length > 0) // Filtrar líneas vacías
        .map((line: string) => parseTXTLine(line, detectedDelimiter));
      
      setPreviewData(parsedData);
    };
    
    // Leer con la codificación especificada
    reader.readAsText(selectedFile, encoding);
  };

  const uploadFile = async () => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('delimiter', delimiter);
    formData.append('encoding', encoding);

    try {
      const response = await axios.post<UploadResponse>(
        'http://127.0.0.1:8000/v1/bbva/upload-txt', // Cambiar endpoint para TXT
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }
      );

      const result = response.data;

      if (response.status === 200) {
        setUploadStatus({
          type: 'success',
          message: `Archivo TXT cargado exitosamente. ${result.records_inserted} registros insertados.`
        });
        
        setUploadHistory(prev => [...prev, {
          id: Date.now(),
          filename: file.name,
          timestamp: new Date().toLocaleString(),
          records: result.records_inserted,
          status: 'success'
        }]);
        
        setFile(null);
        setPreviewData([]);
        setShowPreview(false);
        
        // Limpiar el input file
        const fileInput = document.getElementById('txt-file-input') as HTMLInputElement;
        if (fileInput) {
          fileInput.value = '';
        }
      } else {
        setUploadStatus({
          type: 'error',
          message: result.detail || 'Error al cargar el archivo TXT'
        });
      }
    } catch (error) {
      console.error('Error uploading TXT file:', error);
      
      let errorMessage = 'Error de conexión con el servidor';
      
      if (axios.isAxiosError(error)) {
        if (error.response) {
          errorMessage = error.response.data?.detail || `Error ${error.response.status}: ${error.response.statusText}`;
        } else if (error.request) {
          errorMessage = 'No se pudo conectar con el servidor';
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

  const removeFromHistory = (id: number) => {
    setUploadHistory(prev => prev.filter(item => item.id !== id));
  };

  const clearFile = () => {
    setFile(null);
    setPreviewData([]);
    setShowPreview(false);
    setUploadStatus(null);
    
    // Limpiar el input file
    const fileInput = document.getElementById('txt-file-input') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        Carga de Archivos TXT - BBVA
      </h1>

      {/* Card de carga */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          Seleccionar Archivo TXT
        </h2>
        
        {/* Configuración */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          {/*<div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Delimitador
            </label>
            <select
              value={delimiter}
              onChange={(e) => setDelimiter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value=",">Coma (,)</option>
              <option value=";">Punto y coma (;)</option>
              <option value="\t">Tabulación</option>
              <option value="|">Pipe (|)</option>
              <option value=" ">Espacio</option>
            </select>
          </div> */}
          
          {/*<div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Codificación
            </label>
            <select
              value={encoding}
              onChange={(e) => setEncoding(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="UTF-8">UTF-8</option>
              <option value="UTF-16">UTF-16</option>
              <option value="ISO-8859-1">ISO-8859-1</option>
              <option value="Windows-1252">Windows-1252</option>
            </select>
          </div> */}
        </div>
        
        <div className="mb-4">
          <input
            accept=".txt"
            className="hidden"
            id="txt-file-input"
            type="file"
            onChange={handleFileSelect}
          />
          <label htmlFor="txt-file-input">
            <div className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 cursor-pointer">
              <Upload className="w-4 h-4 mr-2" />
              Seleccionar Archivo TXT
            </div>
          </label>
          
          {file && (
            <div className="inline-flex items-center ml-4 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              <FileText className="w-4 h-4 mr-2" />
              <span className="mr-2">{file.name}</span>
              <span className="text-xs text-blue-600">
                ({(file.size / 1024).toFixed(1)} KB)
              </span>
              <button
                onClick={clearFile}
                className="ml-2 text-blue-600 hover:text-blue-800"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        {previewData.length > 0 && (
          <div className="mb-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowPreview(true)}
                className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm"
              >
                <Eye className="w-4 h-4 mr-1" />
                Vista Previa ({previewData.length - 1} filas)
              </button>
              
              <div className="text-sm text-gray-600">
                Delimitador detectado: <strong>{delimiter === '\t' ? 'Tabulación' : delimiter}</strong>
              </div>
              
              <div className="text-sm text-gray-600">
                Columnas: <strong>{previewData[0]?.length || 0}</strong>
              </div>
            </div>
          </div>
        )}

        <div className="flex items-center space-x-4">
          <button
            onClick={uploadFile}
            disabled={!file || uploading}
            className={`inline-flex items-center px-4 py-2 rounded-md text-sm font-medium ${
              !file || uploading
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {uploading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"/>
                Procesando TXT...
              </>
            ) : (
              <>
                <Database className="w-4 h-4 mr-2" />
                Cargar TXT a Base de Datos
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
                <CheckCircle className="w-5 h-5 mr-2" />
              ) : (
                <AlertCircle className="w-5 h-5 mr-2" />
              )}
              <span>{uploadStatus.message}</span>
              <button
                onClick={() => setUploadStatus(null)}
                className="ml-auto text-gray-400 hover:text-gray-600"
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
            Historial de Cargas TXT
          </h2>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Archivo TXT
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
                  <tr key={item.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <FileText className="w-4 h-4 mr-2 text-gray-400" />
                        {item.filename}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {item.timestamp}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                      {item.records.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Exitoso
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <button
                        onClick={() => removeFromHistory(item.id)}
                        className="text-red-600 hover:text-red-800 p-1 rounded"
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
          <div className="bg-white rounded-lg max-w-6xl w-full max-h-full overflow-hidden">
            <div className="flex items-center justify-between p-6 border-b">
              <h3 className="text-lg font-semibold">Vista Previa del Archivo TXT</h3>
              <button
                onClick={() => setShowPreview(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-6 overflow-auto max-h-96">
              <div className="mb-4 text-sm text-gray-600 space-y-1">
                <div>Archivo: <strong>{file?.name}</strong></div>
                <div>Delimitador: <strong>{delimiter === '\t' ? 'Tabulación' : delimiter}</strong></div>
                <div>Codificación: <strong>{encoding}</strong></div>
                <div>Filas mostradas: <strong>{previewData.length - 1}</strong></div>
              </div>
              
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
                            <div title={cell} className="truncate max-w-xs">
                              {cell.length > 30 ? `${cell.substring(0, 30)}...` : cell}
                            </div>
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            
            <div className="flex justify-between items-center p-6 border-t">
              <div className="text-sm text-gray-500">
                Total de columnas: {previewData[0]?.length || 0}
              </div>
              <button
                onClick={() => setShowPreview(false)}
                className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default BBVAView;