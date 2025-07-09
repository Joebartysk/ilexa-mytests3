/*import type { Theme } from '@mui/material/styles';

import { useState } from 'react';

import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import Collapse from '@mui/material/Collapse';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';


import { varAlpha } from 'minimal-shared/utils';

import { usePathname } from 'src/routes/hooks';
import { RouterLink } from 'src/routes/components';

import { Iconify } from 'src/components/iconify';

import type { NavItem } from '../nav-config-dashboard';

// ----------------------------------------------------------------------

type NavItemContentProps = {
  item: NavItem;
  depth?: number;
};

export function NavItemContent({ item, depth = 0 }: NavItemContentProps) {
  // No usamos globalTheme ya que no lo necesitamos
  const pathname = usePathname();
  
  const { title, path, icon, info, children } = item;
  const [open, setOpen] = useState(false);
  
  const isActived = path === pathname;
  const hasChildren = children && children.length > 0;

  const handleToggle = () => {
    setOpen((prev) => !prev);
  };

  // Estilos para elementos activos que usamos tanto para el elemento principal como para los hijos
  const activeStyle = (theme: Theme) => ({
    fontWeight: 'fontWeightSemiBold',
    color: theme.vars.palette.primary.main,
    bgcolor: varAlpha(theme.vars.palette.primary.mainChannel, 0.08),
    '&:hover': {
      bgcolor: varAlpha(theme.vars.palette.primary.mainChannel, 0.16),
    },
  });

  // Si tiene elementos hijos, mostrar como menú desplegable
  if (hasChildren) {
    return (
      <>
        <ListItem disableGutters disablePadding>
          <ListItemButton
            disableGutters
            onClick={handleToggle}
            sx={[
              (theme: Theme) => ({
                pl: 2 + (depth * 1),  // Aumentamos el padding para subniveles
                py: 1,
                gap: 2,
                pr: 1.5,
                borderRadius: 0.75,
                typography: 'body2',
                fontWeight: 'fontWeightMedium',
                color: theme.vars.palette.text.secondary,
                minHeight: 44,
                ...(isActived && activeStyle(theme)),
              }),
            ]}
          >
            <Box component="span" sx={{ width: 24, height: 24 }}>
              {icon}
            </Box>

            <Box component="span" sx={{ flexGrow: 1 }}>
              {title}
            </Box>

            {info && info}

            <Iconify
              width={16}
              icon={open ? 'eva:arrow-ios-downward-fill' : 'eva:arrow-ios-forward-fill'}
            />
          </ListItemButton>
        </ListItem>

        <Collapse in={open} timeout="auto" unmountOnExit>
          <List disablePadding>
            {children?.map((child) => (
              <NavItemContent key={child.title} item={child} depth={depth + 1} />
            ))}
          </List>
        </Collapse>
      </>
    );
  }

  // Para elementos sin hijos (enlaces directos)
  return (
    <ListItem disableGutters disablePadding>
      <ListItemButton
        disableGutters
        component={RouterLink}
        href={path}
        sx={[
          (innerTheme: Theme) => ({
            pl: 2 + (depth * 1),  // Aumentamos el padding para subniveles
            py: 1,
            gap: 2,
            pr: 1.5,
            borderRadius: 0.75,
            typography: 'body2',
            fontWeight: 'fontWeightMedium',
            color: innerTheme.vars.palette.text.secondary,
            minHeight: 44,
            ...(isActived && activeStyle(innerTheme)),
          }),
        ]}
      >
        <Box component="span" sx={{ width: 24, height: 24 }}>
          {icon}
        </Box>

        <Box component="span" sx={{ flexGrow: 1 }}>
          {title}
        </Box>

        {info && info}
      </ListItemButton>
    </ListItem>
  );
}*/
/*import { useState } from 'react';
import { Icon } from '@iconify/react'; // O el wrapper que estés usando

import { List, Collapse, ListItemIcon, ListItemText, ListItemButton } from '@mui/material';

import type { NavItem } from '../nav-config-dashboard';

export function NavItemContent({ item }: { item: NavItem }) {
  const [open, setOpen] = useState(false);

  const handleClick = () => setOpen((prev) => !prev);

  if (item.children) {
    return (
      <>
        <ListItemButton onClick={handleClick}>
          {item.icon && <ListItemIcon>{item.icon}</ListItemIcon>}
          <ListItemText primary={item.title} />
          <Icon
            icon={open ? 'eva:arrow-ios-upward-fill' : 'eva:arrow-ios-downward-fill'}
            width={18}
            height={18}
          />
        </ListItemButton>

        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {item.children.map((child) => (
              <ListItemButton key={child.title} sx={{ pl: 4 }} href={child.path}>
                {child.icon && <ListItemIcon>{child.icon}</ListItemIcon>}
                <ListItemText primary={child.title} />
              </ListItemButton>
            ))}
          </List>
        </Collapse>
      </>
    );
  }

  return (
    <ListItemButton href={item.path}>
      {item.icon && <ListItemIcon>{item.icon}</ListItemIcon>}
      <ListItemText primary={item.title} />
    </ListItemButton>
  );
}*/

import { useState } from 'react';
import { Icon } from '@iconify/react';

import {
  List,
  Collapse,
  Menu,
  MenuItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';

import type { NavItem } from '../nav-config-dashboard';

export function NavItemContent({
  item,
  isHorizontal = false, // Prop para saber si está en layout horizontal
}: {
  item: NavItem;
  isHorizontal?: boolean;
}) {
  const [open, setOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    if (item.children) {
      if (isHorizontal) {
        setAnchorEl(event.currentTarget);
      } else {
        setOpen((prev) => !prev);
      }
    }
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  if (item.children) {
    return (
      <>
        <ListItemButton onClick={handleClick}
          sx={{
            ...(isHorizontal && {
              px: 2,
              py: 1,
              borderRadius: 1,
            }),
          }}
        >
          {item.icon && <ListItemIcon>{item.icon}</ListItemIcon>}
          <ListItemText primary={item.title} />
          <Icon
            icon={
              (isHorizontal ? Boolean(anchorEl) : open)
                ? 'eva:arrow-ios-upward-fill'
                : 'eva:arrow-ios-downward-fill'
            }
            width={18}
            height={18}
          />
        </ListItemButton>

        {isHorizontal ? (
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
            transformOrigin={{ vertical: 'top', horizontal: 'left' }}
            PaperProps={{
              sx: {
                mt: 1,
                minWidth: 180,
                borderRadius: 1,
                boxShadow: 3,
              },
            }}
          >
            {item.children.map((child) => (
              <MenuItem key={child.title} onClick={handleClose} component="a" href={child.path}>
                {child.icon && <ListItemIcon>{child.icon}</ListItemIcon>}
                <ListItemText primary={child.title} />
              </MenuItem>
            ))}
          </Menu>
        ) : (
          <Collapse in={open} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.children.map((child) => (
                <ListItemButton key={child.title} sx={{ pl: 4 }} href={child.path}>
                  {child.icon && <ListItemIcon>{child.icon}</ListItemIcon>}
                  <ListItemText primary={child.title} />
                </ListItemButton>
              ))}
            </List>
          </Collapse>
        )}
      </>
    );
  }

  return (
    <ListItemButton href={item.path}>
      {item.icon && <ListItemIcon>{item.icon}</ListItemIcon>}
      <ListItemText primary={item.title} />
    </ListItemButton>
  );
}

