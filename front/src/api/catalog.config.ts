// src/services/catalog.config.ts

import {
	RegimenFiscalData,
	FormaPagoData,
	PeriodicidadData,
	ImpuestoData,
	MonedaData,
	ExportacionData,
	TipoComprobanteData,
	MetodoPagoData, 
	UsoCfdiData,
	TipoRelacionData, 
	TipoFactorData, 
	ClaveUnidadData, 
	CodigoPostalData, 
	MesesData, 
	PaisData,
	PatenteAduanalData, 
	ClaveProdServData,  
	ObjetoImpData, 
	TasaOCuotaData
} from './api.types';

interface CatalogConfig<T> {
	endpoint: string;
	defaultValues: T;
	fieldLabels: T;
}

export const catalogConfigs: Record<string, CatalogConfig<any>> = {
	regimenfiscal: {
		endpoint: 'regimenfiscal',
		defaultValues: {
			tax_regime_code: '',
			description: '',
			fisica: '',
			moral: '',
			effective_start_date: '',
			effective_end_date: '',
		} as RegimenFiscalData,
		fieldLabels: {
			tax_regime_code: 'Código Regimen Fiscal',
			description: 'Descripción',
			fisica: 'Física',
			moral: 'Moral',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	exportacion: {
		endpoint: 'exportacion',
		defaultValues: {
			export_code: '',
			description: '',
			effective_start_date: '',
			effective_end_date: '',
		} as ExportacionData,
		fieldLabels: {
			export_code: 'Código de exportación',
			description: 'Descripción',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	formapago: {
		endpoint: 'formapago',
		defaultValues: {
			payment_method: '',
			description: '',
			is_banked: '',                                  
			operation_number: '',                
			payer_account_rfc: '',                
			payer_account: '',                        
			payer_account_pattern: '',         
			beneficiary_account_rfc: '',            
			beneficiary_account: '',
			beneficiary_account_pattern: '',
			payment_chain_type: '',
			payer_bank_name_if_external: '',
			effective_start_date: '',
			effective_end_date: '',
		} as FormaPagoData,
		fieldLabels: {
			payment_method: 'Forma de Pago',                         // c_FormaPago
			description: 'Descripción',                             // Descripción
			is_banked: 'Es Banco',                                  // Bancarizado
			operation_number: 'Numero de Operación',                // Número de operación
			payer_account_rfc: 'RFC Cuenta Pagador',                // RFC del Emisor de la cuenta ordenante
			payer_account: 'Cuenta Pagador',                        // Cuenta Ordenante
			payer_account_pattern: 'Patrón Cuenta Pagador',         // Patrón para cuenta ordenante
			beneficiary_account_rfc: 'RFC Beneficiario',            // RFC del Emisor Cuenta de Beneficiario
			beneficiary_account: 'Cuenta Beneficiario',             // Cuenta de Beneficiario
			beneficiary_account_pattern: 'Patrón de Cuenta Beneficiario', // Patrón para cuenta Beneficiaria
			payment_chain_type: 'Cadena de pago',                   // Tipo Cadena Pago
			payer_bank_name_if_external: 'Nombre del pago externo', // Nombre del Banco emisor de la cuenta ordenante en caso de extranjero
			effective_start_date: 'Fecha Inicio Efectiva',          // Fecha inicio de vigencia
			effective_end_date: 'Fecha Termino Efectiva' 
		}
	},
	periodicidad: {
		endpoint: 'periodicidad',
		defaultValues: {
			period: '',
			description: '',
			effective_start_date: '',
			effective_end_date: '',
		} as PeriodicidadData,
		fieldLabels: {
			period: 'Periodo',
			description: 'Descripción',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	impuesto: {
		endpoint: 'impuesto',
		defaultValues: {
			c_tax: '',
			description: '',
			tax_withholding: '',
			tax_transferred: '',
			local_federal: '',
			effective_start_date: '',
			effective_end_date: ''
		} as ImpuestoData,
		fieldLabels: {
			c_tax: 'Impuesto',
			description: 'Descripción',
			tax_withholding: 'Retención',
			tax_transferred: 'Traslados',
			local_federal: 'Local Federal',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	moneda: {
		endpoint: 'moneda',
		defaultValues: {
			currency_code: '',
			description: '',
			decimal_places: '',
			variation_percentage: '',
			effective_start_date: '',
			effective_end_date: '',
		} as MonedaData,
		fieldLabels: {
			currency_code: 'Código moneda',
			description: 'Descripción',
			decimal_places: 'Decimal',
			variation_percentage: 'Porcentaje Variación',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	// Agrega más catálogos aquí
	tipocomprobante: {
		endpoint: 'tipocomprobante',
		defaultValues: {
			voucher_type_code: '',
			description: '',
			max_value: '',
			effective_start_date: '',
			effective_end_date: '',
		} as TipoComprobanteData,
		fieldLabels: {
			voucher_type_code: 'Código tipo comprobante',
			description: 'Descripción',
			max_value: 'Valor Máximo',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	metodopago: {
		endpoint: 'metodopago',
		defaultValues: {
			payment_method_code: '',
			description: '',
			effective_start_date: '',
			effective_end_date: '',
		} as MetodoPagoData,
		fieldLabels: {
			payment_method_code: 'Código método de pago',
			description: 'Descripción',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	usocfdi: {
		endpoint: 'usocfdi',
		defaultValues: {
			cfdi_use_code: '',
			description: '',
			moral: '',
			fisica: '',
			recipient_tax_regime: '',
			effective_start_date: '',
			effective_end_date: '',
		} as UsoCfdiData,
		fieldLabels: {
			cfdi_use_code: 'Código de Uso Cfdi',
			description: 'Descripción',
			moral: 'Moral',
			fisica: 'Física',
			recipient_tax_regime: 'Regimen fiscal destinatario',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	tiporelacion: {
		endpoint: 'tiporelacion',
		defaultValues: {
			relation_type_code: '',
			description: '',
			effective_start_date: '',
			effective_end_date: '',
		} as TipoRelacionData,
		fieldLabels: {
			relation_type_code: 'Código de tipo de relación',
			description: 'Descripción',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	tipofactor: {
		endpoint: 'tipofactor',
		defaultValues: {
			factor_type_code: '',
			effective_start_date: '',
			effective_end_date: ''
		} as TipoFactorData,
		fieldLabels: {
			factor_type_code: 'Código tipo factor',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	claveunidad: {
		endpoint: 'claveunidad',
		defaultValues: {
			unit_code: '',
			name_unit: '',
			description: '',
			nota_unit: '',
			effective_start_date: '',
			effective_end_date: '',
			symbol: ''
		} as ClaveUnidadData,
		fieldLabels: {
			unit_code: 'Código de unidad',
			name_unit: 'Nombre',
			description: 'Descripción',
			nota_unit: 'Nota',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
			symbol: 'Símbolo',
		}
	},
	codigopostal: {
		endpoint: 'codigopostal',
		defaultValues: {
			c_codigopostal: '',
			c_localidad: '',
			c_estado: '',
			fecha_inicio_vigencia: '',
			descripcion_del_uso_horario: '',
			dia_inicio_horario_verano: '',
			dia_inicio_horario_invierno: '',
			diferencia_horario_invierno: '',
			c_municipio: '',
			estimulo_franja_fronteriza: '',
			fecha_fin_vigencia: '',
			mes_inicio_horario_verano: '',
			dia_inicio_horario_verano_1: '',
			mes_inicio_horario_invierno: '',
			dia_inicio_horario_invierno_1: ''
		} as CodigoPostalData,
		fieldLabels: {
			c_codigopostal :  'Codigo Postal',
			c_localidad :  'Localidad',
			c_estado :  'Estado',
			fecha_inicio_vigencia :  'Fecha inicio vigencia',
			descripcion_del_uso_horario :  'Descripcion del uso horario',
			dia_inicio_horario_verano :  'Dia inicio horario verano',
			dia_inicio_horario_invierno :  'Dia inicio horario invierno',
			diferencia_horario_invierno :  'Diferencia horario invierno',
			c_municipio :  'Municipio',
			estimulo_franja_fronteriza :  'Estimulo franja fronteriza',
			fecha_fin_vigencia :  'Fecha fin vigencia',
			mes_inicio_horario_verano :  'Mes inicio horario verano',
			dia_inicio_horario_verano_1 :  'Dia inicio horario verano1',
			mes_inicio_horario_invierno :  'Mes inicio horario invierno',
			dia_inicio_horario_invierno_1 :  'Dia inicio horario invierno1',
		}
	},
	meses: {
		endpoint: 'meses',
		defaultValues: {
			c_month: '',
			effective_start_date: '',
			description: '',
			effective_end_date: ''
		} as MesesData,
		fieldLabels: {
			c_month: 'Mes',
			effective_start_date: 'Fecha inicio vigencia',
			description: 'Descripción',
			effective_end_date: 'Fecha fin vigencia'
		}
	},
	pais: {
		endpoint: 'pais',
		defaultValues: {
			c_country: '',
			description: '',
			postcode_format: '',
			tax_identity_registration_format: '',
			tax_identity_registration_validation: '',
			groups: ''
		} as PaisData,
		fieldLabels: {
			c_country: 'Pais',
			description: 'Descripción',
			postcode_format: 'Formato de código postal',
			tax_identity_registration_format: 'Formato de registro de identificación tributaria',
			tax_identity_registration_validation: 'Validación de registro de identificación tributaria',
			groups: 'Agrupación',
		}
	},
	patenteaduanal: {
		endpoint: 'patenteaduanales',
		defaultValues: {
			c_customs: '',
			effective_start_date: '',
			effective_end_date: ''
		} as PatenteAduanalData,
		fieldLabels: {
			c_customs: 'Patente Aduanal',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},
	claveprodserv: {
		endpoint: 'claveprodserv',
		defaultValues: {
			product_service_code: '',
			description: '',
			include_transferred_vat: '',
			include_transferred_ieps: '',
			required_complement: '',
			effective_start_date: '',
			effective_end_date: '',
			border_zone_stimulus: '',
			similar_words: '',
		} as ClaveProdServData,
		fieldLabels: {
			product_service_code: 'Código de productos y servicios',
			description: 'Descripción',
			include_transferred_vat: 'Incluye VAT',
			include_transferred_ieps: 'Incluye IEPS',
			required_complement: 'Complemento requerido',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
			border_zone_stimulus: 'Estímulo zona fronteriza',
			similar_words: 'Palabras similares',
		}
	},
	objetoimp: {
		endpoint: 'objetoimp',
		defaultValues: {
			tax_object_code: '',
			description: '',
			effective_start_date: '',
			effective_end_date: ''
		} as ObjetoImpData,
		fieldLabels: {
			tax_object_code: 'Código impuesto',
			description: 'Descripción',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	},  
	tasaocuota: {
		endpoint: 'tasaocuota',
		defaultValues: {
			ranged_or_fixed: '',
			minimum_value: '',
			maximum_value: '',
			tax: '',
			factor: '',
			transfer: '',
			withholding: '',
			effective_start_date: '',
			effective_end_date: '',
		} as TasaOCuotaData,
		fieldLabels: {
			ranged_or_fixed: 'Rango o fijo',
			minimum_value: 'Valor mínimo',
			maximum_value: 'Valor máximo',
			tax: 'Impuesto',
			factor: 'Factor',
			transfer: 'Transferir',
			withholding: 'Retención',
			effective_start_date: 'Fecha Inicio Efectiva',
			effective_end_date: 'Fecha Termino Efectiva',
		}
	}	
};

export type CatalogDataTypes = {
	[K in keyof typeof catalogConfigs]: typeof catalogConfigs[K]['defaultValues'];
};