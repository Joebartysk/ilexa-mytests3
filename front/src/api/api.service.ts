import axios, { AxiosInstance } from 'axios';

import { PeriodicidadData, DemandablesData, NolocalizableData, FirmsData, BlacklistData, RegimenFiscalData,
	     TipoComprobanteData,MetodoPagoData,FormaPagoData, SentenciasData,ImpuestoData,UsoCfdiData,
		 TipoRelacionData, TipoFactorData, ClaveUnidadData, CodigoPostalData, MesesData, PaisData,
		 PatenteAduanalData, ClaveProdServData, ExportacionData, MonedaData, ObjetoImpData, TasaOCuotaData,
		ExportFileResponse } from './api.types';

class ApiService {
	private axios: AxiosInstance;
	private baseUrl: string;

	constructor() {
		this.baseUrl = process.env.NODE_ENV === 'development'
			 ? 'http://localhost:8000'
			 : 'https://tu-URL-de-producción.com';
		this.axios = axios.create({
			baseURL: this.baseUrl,
			headers: {
				'Content-Type': 'application/json',
			},
		});

		// Configurar interceptor para errores
		this.axios.interceptors.response.use(
			(response) => response.data,
			(error) => {
				throw new Error(error.message || 'Error de servidor');
			}
		);
	}

	public async getAllPeriodicidad(): Promise<PeriodicidadData[]> {
		const response = await this.axios.get('/v1/catalogs/periodicidad/getall?page_size=30');
		return response.data;
	}

	// Puedes agregar más métodos aquí que no estén relacionados con la autenticación
	//Listas negras
	public async getAllDemandables(): Promise<DemandablesData[]> {
		const response = await this.axios.get('/v1/catalogsloadables/demandables?page_size=100');
		return response.data;
	}

	public async getAll_no_located(): Promise<NolocalizableData[]> {
		const response = await this.axios.get('/v1/catalogsloadables/nolocated?page_size=100');
		return response.data;
	}

	public async getAll_firmes(): Promise<FirmsData[]> {
		const response = await this.axios.get('/v1/catalogsloadables/firms?page_size=100');
		return response.data;
	}

	public async getAll_blacklist(): Promise<BlacklistData[]> {
		const response = await this.axios.get('/v1/catalogsloadables/satblacklist?page_size=100');
		return response.data;
	}

	public async getAll_sentences(): Promise<SentenciasData[]> {
		const response = await this.axios.get('/v1/catalogsloadables/sentences?page_size=100');
		return response.data;
	}

	//Catalogos
	public async getAllFormaPago(): Promise<FormaPagoData[]> {
		const response = await this.axios.get('/v1/catalogs/formapago/getall?page_size=30');
		return response.data;
	}

	public async getAllMetodoPago(): Promise<MetodoPagoData[]> {
		const response = await this.axios.get('/v1/catalogs/metodopago/getall?page_size=30');
		return response.data;
	}

	public async getAllRegimenFiscal(): Promise<RegimenFiscalData[]> {
		const response = await this.axios.get('/v1/catalogs/regimenfiscal/getall?page_size=30');
		return response.data;
	}

	public async getAllTipoComprobante(): Promise<TipoComprobanteData[]> {
		const response = await this.axios.get('/v1/catalogs/tipocomprobante/getall?page_size=30');
		return response.data;
	}

	public async getAllImpuesto(): Promise<ImpuestoData[]> {
		const response = await this.axios.get('/v1/catalogs/impuesto/getall?page_size=30');
		return response.data;
	}
	
	public async getAllUsoCfdi(): Promise<UsoCfdiData[]> {
		const response = await this.axios.get('/v1/catalogs/usocfdi/getall?page_size=30');
		return response.data;
	}

	public async getAllTipoRelacion(): Promise<TipoRelacionData[]> {
		const response = await this.axios.get('/v1/catalogs/tiporelacion/getall?page_size=30');
		return response.data;
	}

	public async getAll_tipofactor(): Promise<TipoFactorData[]> {
		const response = await this.axios.get('/v1/catalogs/tipofactor/getall?page_size=30');
		return response.data;
	}
	
	public async getAll_claveunidad(): Promise<ClaveUnidadData[]> {
		const response = await this.axios.get('/v1/catalogs/claveunidad/getall?page_size=30');
		return response.data;
	}

	public async getAll_cp(): Promise<CodigoPostalData[]> {
		const response = await this.axios.get('/v1/catalogs/codigopostal/getall?page_size=30');
		return response.data;
	}

	public async getAll_meses(): Promise<MesesData[]> {
		const response = await this.axios.get('/v1/catalogs/meses/getall?page_size=30');
		return response.data;
	}

	public async getAll_pais(): Promise<PaisData[]> {
		const response = await this.axios.get('/v1/catalogs/pais/getall?page_size=30');
		return response.data;
	}

	public async getAll_patenteaduanal(): Promise<PatenteAduanalData[]> {
		const response = await this.axios.get('/v1/catalogs/patenteaduanales/getall?page_size=30');
		return response.data;
	}

	public async getAllClaveProdServ(): Promise<ClaveProdServData[]> {
		const response = await this.axios.get('/v1/catalogs/claveprodserv/getall?page_size=30');
		return response.data;
	}

	public async getAllExportacion(): Promise<ExportacionData[]> {
		const response = await this.axios.get('/v1/catalogs/exportacion/getall?page_size=30');
		return response.data;
	}

	public async getAllMoneda(): Promise<MonedaData[]> {
		const response = await this.axios.get('/v1/catalogs/moneda/getall?page_size=30');
		return response.data;
	}

	public async getAllObjetoImp(): Promise<ObjetoImpData[]> {
		const response = await this.axios.get('/v1/catalogs/objetoimp/getall?page_size=30');
		return response.data;
	}

	public async getAllTasaOCuota(): Promise<TasaOCuotaData[]> {
		const response = await this.axios.get('/v1/catalogs/tasaocuota/getall?page_size=30');
		return response.data;
	}

	//MÉTODO GENÉRICO PARA AGREGAR ELEMENTO A CUALQUIER CATÁLOGO
	public async createCatalogItem(catalogName: string, data: any): Promise<any> {
		if (!data || Object.keys(data).length === 0) {
			throw new Error('Los datos son requeridos para crear un elemento del catálogo');
		}
		try {
			console.log(data);
			const response = await this.axios.post(`/v1/catalogs/${catalogName}/create`, data);
			console.log('Respuesta del servidor al crear:', response);
			return response; 
		} catch (error) {
			console.error(`Error creando elemento en catálogo ${catalogName}:`, error);
			throw error;
		}
	}

	// MÉTODO GENÉRICO PARA ACTUALIZAR CUALQUIER CATÁLOGO
	public async updateCatalogItem(catalogName: string, id: string, data: any): Promise<any> {
		if (!data || Object.keys(data).length === 0) {
			throw new Error('Los datos son requeridos para actualizar un elemento del catálogo');
		}
		
		try {
			console.log(data);
			const response = await this.axios.put(`/v1/catalogs/${catalogName}/update/${id}`, data);
			return response.data;
		} catch (error) {
			console.error(`Error actualizando elemento en catálogo ${catalogName}:`, error);
			throw error;
		}
	}

	// MÉTODO GENÉRICO PARA ELIMINAR CUALQUIER CATÁLOGO
	public async deleteCatalogItem(catalogName: string, id: string): Promise<void> {
		try {
			await this.axios.delete(`/v1/catalogs/${catalogName}/delete/${id}`);
		} catch (error) {
			console.error(`Error eliminando elemento en catálogo ${catalogName}:`, error);
			throw error;
		}
	}

	// Exporta archivos XLSX o CSV de cualquier tabla
	public async exportAndDownload(
		format: 'xlsx' | 'csv',
		filename: string,
		schema: string,
		table: string
		): Promise<void> {
		try {
			const endpoint = `/v1/export/export-file-${format}?filename=${filename}&schema=${schema}&table=${table}`;
			const response = (await this.axios.get(endpoint)) as ExportFileResponse;

			if (response.success && response.full_download_url) {
			const download = await axios.get(response.full_download_url, {
				responseType: 'blob',
			});

			const blob = new Blob([download.data]);
			const link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);
			link.download = response.filename;
			link.click();

			window.URL.revokeObjectURL(link.href);
			} else {
			console.error('Error: Respuesta inválida', response);
			}
		} catch (error) {
			console.error('Error al exportar y descargar:', error);
			throw error;
		}
	}

}

export default ApiService;