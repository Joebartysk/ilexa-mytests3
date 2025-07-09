import { Label } from 'src/components/label';
import { SvgColor } from 'src/components/svg-color';

// ----------------------------------------------------------------------

const icon = (name: string) => <SvgColor src={`/assets/icons/navbar/${name}.svg`} />;

export type NavItem = {
  title: string;
  path: string;
  icon: React.ReactNode;
  info?: React.ReactNode;
  children?: NavItem[];//Se agrega para identificar hijo en el menu
};

export const navData = [
  {
    title: 'Dashboard',
    path: '/',
    icon: icon('ic-analytics'),
  },//Comienza prueba de menu desplegable
  {
    title: 'CFDIs',
    path: '#',
    icon: icon('ic-user'),
    // Ejemplo de un menú desplegable
    children: [
      {
        title: 'Emitidos',
        path: '/emitidos',
        icon: icon('ic-user'), // Puedes usar el mismo icono o uno diferente
      },
      {
        title: 'Recibidos',
        path: '/recibidos',
        icon: icon('ic-user'),
      }
    ]
  },
  {
    title: 'Conciliación Bancaria',
    path: '#',
    icon: icon('ic-user'),
    // Ejemplo de un menú desplegable
    children: [
      {
        title: 'Registro de movimientos',
        path: '/registromov',
        icon: icon('ic-user'), // Puedes usar el mismo icono o uno diferente
      },
      {
        title: 'CFDIs conciliados',
        path: '/conciliados',
        icon: icon('ic-user'),
      },
      {
        title: 'CFDIs no conciliados',
        path: '/no_conciliados',
        icon: icon('ic-user'),
      }
    ] //Termina prueba desplegable
  },
  {
    title: 'Lista de EFOs y EDOs',
    path: '/tableroblacklist',
    icon: icon('ic-user'),
  },
  {
    title: 'Catalogos',
    path: '/tablerocat',
    icon: icon('ic-user'),
  },
  {
    title: 'Estados de Cuenta-BBVA',
    path: '/bbva',
    icon: icon('ic-user'),
  },
  {
    title: 'Estados de Cuenta-Clara',
    path: '/clara',
    icon: icon('ic-user'),
  },
  {
    title: 'Estados de Cuenta-HSBC',
    path: '/bankstatement',
    icon: icon('ic-user'),
  },
  {
    title: 'Estados de Cuenta-Inbursa',
    path: '/inbursa',
    icon: icon('ic-user'),
  },
  {
    title: 'Mi suscripcion',
    path: '/sign-in',
    icon: icon('ic-lock'),
  },
  {
    title: 'Not found',
    path: '/404',
    icon: icon('ic-disabled'),
  },
];
