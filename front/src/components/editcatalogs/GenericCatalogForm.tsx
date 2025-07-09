// src/components/GenericCatalogForm.tsx
import React, { useState } from 'react';

import { Box, Button, MenuItem, TextField, Typography } from '@mui/material';

import ApiService from '../../api/api.service';
import { catalogConfigs } from '../../api/catalog.config';

import type { CatalogDataTypes } from '../../api/catalog.config';

type CatalogKey = keyof CatalogDataTypes;

const api = new ApiService();

interface Props<T = Record<string, any>> {
	catalogKey: keyof typeof catalogConfigs;
	onSuccess?: (item: T) => void;
	initialData?: T;
	idField?: string;
	fieldLabels?: Record<string, string>;
}

const isDateField = (fieldName: string) =>
	fieldName.toLowerCase().includes('date');

//const isBooleanField = (fieldName: string) =>
	//fieldName === 'is_banked';

//const isNumberField = (value: any): boolean =>
	//typeof value === 'number' && !isNaN(value);

//const formatLabel = (key: string) =>
	//key.replace(/_/g, ' ').toUpperCase();
const formatLabel = (key: string, configLabels?: Record<string, string>, customLabels?: Record<string, string>) => {
	if (customLabels && customLabels[key]) {
		return customLabels[key];
	}
	
	if (configLabels && configLabels[key]) {
		return configLabels[key];
	}
	
	return key
		.replace(/_/g, ' ')
		.replace(/\b\w/g, letter => letter.toUpperCase());
};

// ✅ Formatea fechas del input (aaaa-mm-dd) → backend (dd/mm/aaaa)
const formatDateForBackend = (value: string): string => {
  if (!value) return ''; // vacía
  const parts = value.split('-');
  if (parts.length !== 3) return ''; // formato inválido

  const [year, month, day] = parts;
  if (!year || !month || !day) return ''; // algún componente faltante

  return `${day}/${month}/${year}`;
};

// ✅ Formatea fechas del backend (dd/mm/aaaa) → input (aaaa-mm-dd)
const formatDateForInput = (value: string): string => {
	if (!value) return '';
	const [day, month, year] = value.split('/');
	return `${year}-${month}-${day}`;
};

const getInputType = (key: string, _value: any) => {
	if (isDateField(key)) return 'date';
	//if (isBooleanField(key)) return 'text';
	return 'text';
};

//function GenericCatalogForm({ catalogKey, onSuccess, initialData, idField = 'id' }: Props) {
function GenericCatalogForm<T = Record<string, any>>({catalogKey, onSuccess, initialData, idField = 'id', fieldLabels}: Props<T>) {
	const { endpoint, defaultValues, fieldLabels: configLabels } = catalogConfigs[catalogKey];

	// ✅ Ajuste inicial si hay datos con fechas
	const parsedInitialData = initialData
		? Object.fromEntries(
			Object.entries(initialData).map(([key, value]) => {
				if (isDateField(key) && typeof value === 'string') {
					return [key, formatDateForInput(value)];
				}
				return [key, value];
			})
		)
		: defaultValues;

	const [formData, setFormData] = useState({ ...parsedInitialData });
	const [message, setMessage] = useState('');
	const isEditMode = !!initialData;

	const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
		const { name, value } = e.target;

		/*if (isBooleanField(name)) {
			setFormData((prev: Record<string, any>) => ({
				...prev,
				[name]: value === 'true',
			}));
		} else {*/
			setFormData((prev: Record<string, any>) => ({
				...prev,
				[name]: value,
			}));
		//}
	};

    const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		try {
			// 🔧 Convertir "" a null, y tipar explícitamente como Record<string, any>
			/*const cleanedFormData: Record<string, any> = Object.fromEntries(
				Object.entries(formData).map(([key, value]) => [
					key,
					value === '' ? null : value,
				])
			);*/
			const cleanedFormData: Record<string, any> = Object.fromEntries(
				Object.entries(formData).map(([key, value]) => {
					let val = value === '' ? null : value;

					if (isDateField(key) && typeof val === 'string') {
					val = formatDateForBackend(val);
					}

					return [key, val];
				})
			);


			if (isEditMode) {
				const id = cleanedFormData[idField];
				console.log('Actualizando registro con ID:', id);

				if (!id) {
					throw new Error('ID no encontrado para actualización');
				}

				const response = await api.updateCatalogItem(endpoint, id, cleanedFormData);
				console.log('Registro actualizado:', response);
				setMessage('✅ Registro actualizado correctamente');

				if (onSuccess) {
					onSuccess(cleanedFormData as T);
				}
			} else {
				const response = await api.createCatalogItem(endpoint, cleanedFormData);
				console.log('Respuesta completa del servidor:', response);

				const newId = response.data?.id_insertado;
				console.log('ID extraído:', newId);

				if (newId) {
					const completeRecord = {
						...cleanedFormData,
						[idField]: newId,
					};

					console.log('Registro completo con ID:', completeRecord);

					setFormData(completeRecord);
					setMessage('✅ Registro creado correctamente');

					if (onSuccess) {
						onSuccess(completeRecord as T);
					}
				} else {
					console.warn('No se pudo extraer el ID del registro creado');
					setMessage('✅ Registro creado correctamente');

					if (onSuccess) {
						onSuccess(cleanedFormData as T);
					}
				}
			}
		} catch (error: any) {
			console.error('Error en handleSubmit:', error);
			setMessage(`❌ ${error.message || 'Error al guardar el registro'}`);
		}
	};

	return (
		<form onSubmit={handleSubmit}>
			<Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
				{Object.entries(defaultValues).map(([key, defaultValue]) => {
					const value =
						formData[key] !== undefined && formData[key] !== null
							? String(formData[key])
							: '';
					const inputType = getInputType(key, defaultValue);
					const label = formatLabel(key, configLabels, fieldLabels);

					/*if (isBooleanField(key)) {
						return (
							<TextField
								key={key}
								select
								fullWidth
								name={key}
								//label={formatLabel(key)}
								label={label}
								value={value}
								onChange={handleChange}
								size="small"
							>
								<MenuItem value="true">Sí</MenuItem>
								<MenuItem value="false">No</MenuItem>
							</TextField>
						);
					}*/

					return (
						<TextField
							key={key}
							fullWidth
							name={key}
							label={label}
							type={inputType}
							value={value}
							onChange={handleChange}
							size="small"
							InputLabelProps={inputType === 'date' ? { shrink: true } : undefined}
						/>
					);
				})}

				<Button variant="contained" type="submit">
					{isEditMode ? 'Actualizar' : 'Guardar'}
				</Button>

				{message && (
					<Typography
						color={message.startsWith('✅') ? 'success.main' : 'error.main'}
						variant="body2"
					>
						{message}
					</Typography>
				)}
			</Box>
		</form>
	);
}

export default GenericCatalogForm;


