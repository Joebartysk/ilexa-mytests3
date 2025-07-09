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
export const BlacklistPage = lazy(() => import('src/pages/app/blacklist'));
export const NolocalizablePage = lazy(() => import('src/pages/app/nolocalizable'));
export const DemandablesPage = lazy(() => import('src/pages/app/demandables'));
export const FirmesPage = lazy(() => import('src/pages/app/firmes'));
export const SentenciasPage = lazy(() => import('src/pages/app/sentencias'));

const TABS = [
  { label: 'Lista Negra 69-B', component: <BlacklistPage /> },
  { label: 'No localizables', component: <NolocalizablePage /> },
  { label: 'Demandables', component: <DemandablesPage /> },
  { label: 'Firmes', component: <FirmesPage /> },
  { label: 'Sentencias', component: <SentenciasPage /> },
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
            Listas de EFOs y EDOs
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
