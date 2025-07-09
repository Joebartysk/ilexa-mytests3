import type { RouteObject } from 'react-router';

import { Outlet } from 'react-router-dom';
import { varAlpha } from 'minimal-shared/utils';
import { useState, useEffect, useCallback, lazy, Suspense } from 'react';

import { Tabs, Tab, Box, Typography } from '@mui/material';
import LinearProgress, { linearProgressClasses } from '@mui/material/LinearProgress';

import { DashboardContent } from 'src/layouts/dashboard';

// ----------------------------------------------------------------------
// Importa tus vistas individuales (o separa el contenido de cada tabla en componentes)
/*import { BlacklistView } from './BlacklistView';*/
export const RegimenFiscalPage = lazy(() => import('src/pages/app/regimenfiscal'));
export const TipoComprobantePage = lazy(() => import('src/pages/app/tipocomprobante'));
export const MetodoPagoPage = lazy(() => import('src/pages/app/metodopago'));
export const FormaPagoPage = lazy(() => import('src/pages/app/formapago'));
export const PeriodicidadesPage = lazy(() => import('src/pages/app/periodicidades'));
export const ImpuestoPage = lazy(() => import('src/pages/app/impuesto'));
export const UsoCfdiPage = lazy(() => import('src/pages/app/usocfdi'));
export const TipoRelacionPage = lazy(() => import('src/pages/app/tiporelacion'));
export const TipoFactorPage = lazy(() => import('src/pages/app/tipofactor'));
export const ClaveUnidadPage = lazy(() => import('src/pages/app/claveunidad'));
export const CodigoPostalPage = lazy(() => import('src/pages/app/cp'));
export const MesesPage = lazy(() => import('src/pages/app/meses'));
export const PaisPage = lazy(() => import('src/pages/app/pais'));
export const PatenteAduanalPage = lazy(() => import('src/pages/app/patenteaduanal'));
export const ClaveProdServPage = lazy(() => import('src/pages/app/claveprodserv'));
export const ExportacionPage = lazy(() => import('src/pages/app/exportacion'));
export const MonedaPage = lazy(() => import('src/pages/app/moneda'));
export const ObjetoImpPage = lazy(() => import('src/pages/app/objetoimp'));
export const TasaOCuotaPage = lazy(() => import('src/pages/app/tasaocuota'));

const TABS = [
  { label: 'Regimen Fiscal', component: <RegimenFiscalPage /> },
  { label: 'Tipo comprobante', component: <TipoComprobantePage /> },
  { label: 'Metodo de pago', component: <MetodoPagoPage /> },
  { label: 'Forma de pago', component: <FormaPagoPage /> },
  { label: 'Periodicidades', component: <PeriodicidadesPage /> },
  { label: 'Impuesto', component: <ImpuestoPage /> },
  { label: 'Uso CFDI', component: <UsoCfdiPage /> },
  { label: 'Tipo de relación', component: <TipoRelacionPage /> },
  { label: 'Tipo Factor', component: <TipoFactorPage /> },
  { label: 'Clave Unidad', component: <ClaveUnidadPage /> },
  { label: 'Código Postal', component: <CodigoPostalPage /> },
  { label: 'Meses', component: <MesesPage /> },
  { label: 'Pais', component: <PaisPage /> },
  { label: 'Patente Aduanal', component: <PatenteAduanalPage /> },
  { label: 'Clave productos y servicios', component: <ClaveProdServPage /> },
  { label: 'Exportacion', component: <ExportacionPage /> },
  { label: 'Moneda', component: <MonedaPage /> },
  { label: 'Objeto Impuestos', component: <ObjetoImpPage /> },
  { label: 'Tasa o cuota', component: <TasaOCuotaPage /> },
  
];

export  function TablerocatView() {
  const [currentTab, setCurrentTab] = useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <DashboardContent maxWidth={false}>
      <Box sx={{ display: 'flex', flexDirection: 'column', mb: 3 }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
            Catalogos
        </Typography>
        <Tabs
          value={currentTab}
          onChange={handleChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ mb: 3 }}
        >
          {TABS.map((tab, index) => (
            <Tab key={index} label={tab.label} />
          ))}
        </Tabs>

        <Box >
          {TABS[currentTab].component}
        </Box>
      </Box>
    </DashboardContent>
  );
}
