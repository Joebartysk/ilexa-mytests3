import { useState, useCallback } from 'react';

import Box from '@mui/material/Box';
import Popover from '@mui/material/Popover';
import TableRow from '@mui/material/TableRow';
import Checkbox from '@mui/material/Checkbox';
import MenuList from '@mui/material/MenuList';
import TableCell from '@mui/material/TableCell';
import IconButton from '@mui/material/IconButton';
import MenuItem, { menuItemClasses } from '@mui/material/MenuItem';

import { Iconify } from 'src/components/iconify';

// ----------------------------------------------------------------------

export type PaisProps = {
  id: string,
  c_country: string,
	description: string,
	postcode_format: string,
	tax_identity_registration_format: string,
	tax_identity_registration_validation: string,
	groups: string
};

type PaisTableRowProps = {
  row: PaisProps;
  selected: boolean;
  onSelectRow: () => void;
  onEdit: () => void;
  onDelete: () => void;
};

export function PaisTableRow({ row, selected, onSelectRow, onEdit, onDelete }: PaisTableRowProps) {
  const [openPopover, setOpenPopover] = useState<HTMLButtonElement | null>(null);

  const handleOpenPopover = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
    setOpenPopover(event.currentTarget);
  }, []);

  const handleClosePopover = useCallback(() => {
    setOpenPopover(null);
  }, []);

  // Componente para mostrar color en celda
  const formatSituation = (situation: string) => {
    switch (situation) {
      case 'Definitivo':
        return 'Definitivo';
      case 'Desvirtuado':
        return 'Desvirtuado';
      case 'Sentencia Favorable':
        return 'Sentencia Favorable';
      default:
        return 'No determinada';
    }
  };
  return (
    <>
      <TableRow hover tabIndex={-1} role="checkbox" selected={selected}>

        <TableCell component="th" scope="row" size="small" sx={{ width: '5%' }}>
          <Box
            sx={{
              gap: 2,
              display: 'flex',
              alignItems: 'center',
              width: '1%',
            }}
          >
            {row.id}
          </Box>
        </TableCell>
        <TableCell size="small" sx={{ width: '20%' }}>{row.c_country}</TableCell>
        <TableCell size="small" sx={{ width: '20%' }}>{row.description}</TableCell>
        <TableCell size="small" sx={{ width: '15%' }}>{row.postcode_format}</TableCell>
        <TableCell size="small" sx={{ width: '20%' }}>{row.tax_identity_registration_format}</TableCell>
        <TableCell size="small" sx={{ width: '20%' }}>{row.tax_identity_registration_validation}</TableCell>
        <TableCell size="small" sx={{ width: '15%' }}>{row.groups}</TableCell>
        

        <TableCell align="right" size="small" sx={{ width: '5%' }}>
          <IconButton onClick={handleOpenPopover}>
            <Iconify icon="eva:more-vertical-fill" />
          </IconButton>
        </TableCell>
      </TableRow>

      <Popover
              open={!!openPopover}
              anchorEl={openPopover}
              onClose={handleClosePopover}
              anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
              transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
              <MenuList
                disablePadding
                sx={{
                  p: 0.5,
                  gap: 0.5,
                  width: 140,
                  display: 'flex',
                  flexDirection: 'column',
                  [`& .${menuItemClasses.root}`]: {
                    px: 1,
                    gap: 2,
                    borderRadius: 0.75,
                    [`&.${menuItemClasses.selected}`]: { bgcolor: 'action.selected' },
                  },
                }}
              >
                <MenuItem
                  onClick={() => {
                    onEdit(); // ✅ ahora usa la función para abrir el modal con el item
                    handleClosePopover();
                  }}
                >
                  <Iconify icon="solar:pen-bold" />
                  Edit
                </MenuItem>
      
                <MenuItem
                  onClick={async () => {
                    await onDelete(); // ✅ función de eliminar
                    handleClosePopover();
                  }}
                  sx={{ color: 'error.main' }}
                >
                  <Iconify icon="solar:trash-bin-trash-bold" />
                  Delete
                </MenuItem>
              </MenuList>
            </Popover>
    </>
  );
}
