import type { Breakpoint } from '@mui/material/styles';

import { useTheme, useMediaQuery } from '@mui/material';

import { NavHorizontal } from './navHorizontal';
import { NavDesktop, NavContentProps } from './nav';

export function ResponsiveNav(props: NavContentProps & { layoutQuery: Breakpoint }) {
  const theme = useTheme();
  const isDesktop = useMediaQuery(theme.breakpoints.up(props.layoutQuery));

  return isDesktop ? (
    <NavDesktop {...props} layoutQuery={props.layoutQuery} />
  ) : (
    <NavHorizontal {...props} />
  );
}