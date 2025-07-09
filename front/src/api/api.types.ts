// src/api/api.types.ts

export interface UserData {
	password: string;
	email: string;
	first_name: string;
	last_name: string;
	phone: string;
}

export interface PeriodicidadData {
	effective_start_date: string;
	id: string;
	effective_end_date: string;
	period: string;
	description: string;
}

export interface FormaPagoData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	payer_bank_name_if_external: string;
	payment_chain_type: string;
	beneficiary_account_pattern: string;
	beneficiary_account: string;
	beneficiary_account_rfc: string;
	payer_account_pattern: string;
	payer_account: string;
	payer_account_rfc: string;
	operation_number: string;
	is_banked: string;
	description: string;
	payment_method: string;
}

export interface MetodoPagoData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	description: string;
	payment_method_code: string;
}

export interface RegimenFiscalData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	moral: string;
	fisica: string;
	description: string;
	tax_regime_code: string;
}

export interface TipoComprobanteData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	max_value: string;
	description: string;
	voucher_type_code: string;
}

export interface ImpuestoData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	c_tax: string;
	description: string;
    tax_withholding: string;
    tax_transferred: string;
    local_federal: string;
}

export interface UsoCfdiData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	cfdi_use_code: string;
	description: string;
    moral: string;
    fisica: string;
    recipient_tax_regime: string;
}

export interface TipoRelacionData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	relation_type_code: string;
	description: string;
}

export interface DemandablesData {
	id: string;
	rfc: string;
	company_name: string;
	type_person: string;
	supposed: string;
	dates_of_first_publication: string;
	federal_entity: string;
  }

  
  export interface NolocalizableData {
	rfc: string;
	company_name: string;
	type_person: string;
	supposed: string;
	dates_of_first_publication: string;
	federal_entity: string;
  }

  export interface FirmsData {
	id: string;
	rfc: string;
	company_name: string;
	type_person: string;
	supposed: string;
	dates_of_first_publication: string;
	federal_entity: string;
  }

  export interface BlacklistData {
	alleged_dof_publication: string; 
	final_dof_publication: string; 
	rfc: string; 
	taxpayers_who_distorted_sat: string; 
	favorable_ruling_sat: string; 
	id: string; 
	sat_page_publication_distorted: string; 
	sat_page_publication_favorable_ruling: string; 
	taxpayer_name: string; 
	taxpayers_who_distorted_dof: string; 
	favorable_ruling_dof: string;
	taxpayer_situation: string; //Sentencia
	distorted_dof_publication: string; 
	dof_publication_favorable_ruling: string; 
	sat_presumption_number_date: string; 
	definitive_sat_document: string; 
	presumptive_sat_page_publication: string; 
	final_sat_page_publication: string; 
	dof_presumption_number_date: string; 
	definitive_dof_document: string; 
  }
  export interface SentenciasData {
	id: string;
	rfc: string;
	company_name: string;
	type_person: string;
	supposed: string;
	dates_of_first_publication: string;
	federal_entity: string;
  }

export interface TipoFactorData {
	id: string;
	factor_type_code: string;
	effective_start_date: string;
	effective_end_date: string;
  }

  export interface ClaveUnidadData {
	id: string;
	unit_code: string;
	name_unit: string;
	description: string;
	nota_unit: string;
	effective_start_date: string;
	effective_end_date: string;
	symbol: string;
  }

 export interface CodigoPostalData {
	id: string;
	c_codigopostal: string;
	c_localidad: string;
	c_estado: string;
	fecha_inicio_vigencia: string;
	descripcion_del_uso_horario: string;
	dia_inicio_horario_verano: string;
	dia_inicio_horario_invierno: string;
	diferencia_horario_invierno: string;
	c_municipio: string;
	estimulo_franja_fronteriza: string;
	fecha_fin_vigencia: string;
	mes_inicio_horario_verano: string;
	dia_inicio_horario_verano_1: string;
	mes_inicio_horario_invierno: string;
	dia_inicio_horario_invierno_1: string;
  }

  export interface MesesData {
	id: string;
	c_month: string;
	effective_start_date: string;
	description: string;
	effective_end_date: string;
  }

  export interface PaisData {
	id: string;
	c_country: string;
	description: string;
	postcode_format: string;
	tax_identity_registration_format: string;
	tax_identity_registration_validation: string;
	groups: string;
  }

export interface PatenteAduanalData {
	id: string;
    c_customs: string;
	effective_start_date: string;
	effective_end_date: string;
  }


  export interface TipoComprobanteData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	max_value: string;
	description: string;
	voucher_type_code: string;
}

export interface ClaveProdServData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	description: string;
	product_service_code: string;
	include_transferred_vat: string;
	include_transferred_ieps: string;
	required_complement: string;
	border_zone_stimulus: string;
	similar_words: string;
}

export interface ExportacionData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	description: string;
	export_code: string;
}

export interface MonedaData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	description: string;
	currency_code: string;
	decimal_places: string;
	variation_percentage: string;
}

export interface ObjetoImpData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	description: string;
	tax_object_code: string;
}

export interface TasaOCuotaData {
	id: string;
	effective_start_date: string;
	effective_end_date: string;
	tax: string;
	ranged_or_fixed: string;
	minimum_value: string;
	maximum_value: string;
	factor: string;
	transfer: string;
	withholding: string;
}

//Para el exportado XLS/CSV
export interface ExportFileResponse {
  success: boolean;
  message: string;
  filename: string;
  download_url: string;
  full_download_url: string;
  file_size: number;
  file_type: string;
  path: string;
  created_at: string;
}

