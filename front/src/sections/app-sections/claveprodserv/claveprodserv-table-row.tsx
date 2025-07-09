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

export type ClaveProdServProps = {
  id: string,
  effective_start_date: string,
  effective_end_date: string,
  description: string,
  product_service_code: string,
  include_transferred_vat: string,
  include_transferred_ieps: string,
  required_complement: string,
  border_zone_stimulus: string,
  similar_words: string,
};

type ClaveProdServTableRowProps = {
  row: ClaveProdServProps;
  selected: boolean;
  onSelectRow: () => void;
  onEdit: () => void;
  onDelete: () => void;
};

export function ClaveProdServTableRow({ row, selected, onSelectRow, onEdit, onDelete }: ClaveProdServTableRowProps) {
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

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.product_service_code}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.description}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.include_transferred_vat}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.include_transferred_ieps}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.required_complement}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.effective_start_date}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.effective_end_date}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.border_zone_stimulus}</TableCell>

        <TableCell align="center" size="small" sx={{ width: '10%' }} >{row.similar_words}</TableCell>

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
