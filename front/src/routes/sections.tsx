import type { RouteObject } from 'react-router';

import { lazy, Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import { varAlpha } from 'minimal-shared/utils';

import Box from '@mui/material/Box';
import LinearProgress, { linearProgressClasses } from '@mui/material/LinearProgress';

import { AuthLayout } from 'src/layouts/auth';
import { DashboardLayout } from 'src/layouts/dashboard';

// ----------------------------------------------------------------------

export const DashboardPage = lazy(() => import('src/pages/dashboard'));
export const BlogPage = lazy(() => import('src/pages/blog'));
export const UserPage = lazy(() => import('src/pages/user'));
export const SignInPage = lazy(() => import('src/pages/sign-in'));
export const ProductsPage = lazy(() => import('src/pages/products'));
export const Page404 = lazy(() => import('src/pages/page-not-found'));
export const RegisterPage = lazy(() => import('src/pages/app/register'));
export const BankStatementPage = lazy(() => import('src/pages/app/bankstatement'));
export const ClaraPage = lazy(() => import('src/pages/app/clara'));
export const BBVAPage = lazy(() => import('src/pages/app/bbva'));
export const InbursaPage = lazy(() => import('src/pages/app/inbursa'));
/*export const PeriodicidadesPage = lazy(() => import('src/pages/app/periodicidades'));
export const DemandablesPage = lazy(() => import('src/pages/app/demandables'));
export const NolocalizablePage = lazy(() => import('src/pages/app/nolocalizable'));
export const FirmesPage = lazy(() => import('src/pages/app/firmes'));
export const BlacklistPage = lazy(() => import('src/pages/app/blacklist'));
export const RegimenFiscalPage = lazy(() => import('src/pages/app/regimenfiscal'));
export const TipoComprobantePage = lazy(() => import('src/pages/app/tipocomprobante'));
export const MetodoPagoPage = lazy(() => import('src/pages/app/metodopago'));
export const FormaPagoPage = lazy(() => import('src/pages/app/formapago'));*/
export const TablerocatPage = lazy(() => import('src/pages/app/tablerocat'));
export const TableroblacklistPage = lazy(() => import('src/pages/app/tableroblacklist'));


const renderFallback = () => (
  <Box
    sx={{
      display: 'flex',
      flex: '1 1 auto',
      alignItems: 'center',
      justifyContent: 'center',
    }}
  >
    <LinearProgress
      sx={{
        width: 1,
        maxWidth: 320,
        bgcolor: (theme) => varAlpha(theme.vars.palette.text.primaryChannel, 0.16),
        [`& .${linearProgressClasses.bar}`]: { bgcolor: 'text.primary' },
      }}
    />
  </Box>
);

export const routesSection: RouteObject[] = [
  {
    element: (
      <DashboardLayout>
        <Suspense fallback={renderFallback()}>
          <Outlet />
        </Suspense>
      </DashboardLayout>
    ),
    children: [
      { index: true, element: <DashboardPage /> },
      /*{ path: 'periodicidad', element: <PeriodicidadesPage /> },
      { path: 'demandables', element: <DemandablesPage /> },
      { path: 'nolocalizable', element: <NolocalizablePage /> },
      { path: 'firmes', element: <FirmesPage /> },
      { path: 'blacklist', element: <BlacklistPage /> },
      { path: 'metodopago', element: <MetodoPagoPage /> },
      { path: 'formapago', element: <FormaPagoPage /> },
      { path: 'regimenfiscal', element: <RegimenFiscalPage /> },
      { path: 'tipocomprobante', element: <TipoComprobantePage /> },
      { path: 'products', element: <ProductsPage /> },
      { path: 'blog', element: <BlogPage /> },*/
      { path: 'bankstatement', element: <BankStatementPage /> },
      { path: 'clara', element: <ClaraPage /> },
      { path: 'bbva', element: <BBVAPage /> },
      { path: 'inbursa', element: <InbursaPage /> },
      { path: 'tablerocat', element: <TablerocatPage /> },
      { path: 'tableroblacklist', element: <TableroblacklistPage /> },
    ],
  },
  {
    path: 'sign-in',
    element: (
      <AuthLayout>
        <SignInPage />
      </AuthLayout>
    ),
  },
  {
    path: 'register',
    element: (
      <AuthLayout>
        <RegisterPage />
      </AuthLayout>
    ),
  },
  {
    path: '404',
    element: <Page404 />,
  },
  { path: '*', element: <Page404 /> },
];
