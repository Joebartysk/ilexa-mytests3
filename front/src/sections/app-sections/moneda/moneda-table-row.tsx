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

export type MonedaProps = {
  id: string,
  effective_start_date: string,
  effective_end_date: string,
  description: string,
  currency_code: string,
  decimal_places: string,
  variation_percentage: string,
};

type MonedaTableRowProps = {
  row: MonedaProps;
  selected: boolean;
  onSelectRow: () => void;
  onEdit: () => void;
  onDelete: () => void;
};

export function MonedaTableRow({ row, selected, onSelectRow, onEdit, onDelete, }: MonedaTableRowProps) {
  const [openPopover, setOpenPopover] = useState<HTMLButtonElement | null>(null);

  const handleOpenPopover = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
    setOpenPopover(event.currentTarget);
  }, []);

  const handleClosePopover = useCallback(() => {
    setOpenPopover(null);
  }, []);

  return (
    <>
      <TableRow hover tabIndex={-1} role="checkbox" selected={selected}>

        <TableCell component="th" scope="row" size="small" sx={{ width: '5%' }}>
          <Box
            sx={{
              gap: 2,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            {row.id}
          </Box>
        </TableCell>

        <TableCell align="center" size="small" sx={{ width: '15%' }} >{row.currency_code}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '30%' }} >{row.description}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '15%' }} >{row.decimal_places}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '25%' }} >{row.variation_percentage}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '20%' }} >{row.effective_start_date}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '20%' }} >{row.effective_end_date}</TableCell>

        <TableCell align="right">
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
