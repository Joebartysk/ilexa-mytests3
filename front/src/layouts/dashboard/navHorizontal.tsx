import { Box } from '@mui/material';
import { useTheme } from '@mui/material/styles';

import { NavItemContent } from './nav-item-content';

import type { NavContentProps } from './nav';

export function NavHorizontal({ data, workspaces, slots }: NavContentProps) {
  const theme = useTheme();

  return (
    <Box
      component="nav"
      sx={{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        px: 2,
        py: 1,
        height: 64,
        position: 'relative',
        top: 0,
        left: 0,
        right: 0,
        zIndex: theme.zIndex.appBar,
        backgroundColor: theme.palette.background.neutral,
        color: '#FFFFFF',
        borderBottom: `1px solid ${theme.palette.divider}`,
      }}
    >
      <Box sx={{ display: 'flex', gap: 2, 
        backgroundColor: theme.palette.background.neutral,
        color: '#FFFFFF',
        }}
      >
        {data.map((item) => (
          <NavItemContent key={item.title} item={item} isHorizontal />
        ))}
      </Box>

      {slots?.bottomArea}
    </Box>
  );
}
