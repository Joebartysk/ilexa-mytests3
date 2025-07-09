// src/pages/CatalogPage.tsx
import React, { useState } from 'react';

import {
	Button,
	Dialog,
	DialogTitle,
	DialogContent,
	DialogActions
} from '@mui/material';

import GenericCatalogForm from '../../components/editcatalogs/GenericCatalogForm';

function CatalogPage() {
	const [open, setOpen] = useState(false);
	const [catalogKey, setCatalogKey] = useState<'moneda' | 'formapago' | 'impuesto'>('moneda');

	const handleOpen = (key: typeof catalogKey) => {
		setCatalogKey(key);
		setOpen(true);
	};

	const handleClose = () => setOpen(false);

	return (
		<>
			<h2>Catálogos</h2>
			<Button variant="contained" onClick={() => handleOpen('moneda')}>
				Agregar Moneda
			</Button>
			<Button variant="contained" onClick={() => handleOpen('formapago')}>
				Agregar Forma de Pago
			</Button>

			<Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
				<DialogTitle>Nuevo registro de {catalogKey}</DialogTitle>
				<DialogContent>
					<GenericCatalogForm catalogKey={catalogKey} />
				</DialogContent>
				<DialogActions>
					<Button onClick={handleClose} color="secondary">
						Cerrar
					</Button>
				</DialogActions>
			</Dialog>
		</>
	);
}

export default CatalogPage;
