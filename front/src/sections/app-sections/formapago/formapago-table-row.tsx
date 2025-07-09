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

export type FormaPagoProps = {
  id: string,
  effective_start_date: string,
  effective_end_date: string,
  payer_bank_name_if_external: string,
  payment_chain_type: string,
  beneficiary_account_pattern: string,
  beneficiary_account: string,
  beneficiary_account_rfc: string,
  payer_account_pattern: string,
  payer_account: string,
  payer_account_rfc: string,
  operation_number: string,
  is_banked: string,
  description: string,
  payment_method: string
};


type FormaPagoTableRowProps = {
  row: FormaPagoProps;
  selected: boolean;
  onSelectRow: () => void;
  onEdit: () => void; // 👈 nueva prop para abrir el modal
  onDelete: () => Promise<void>; // 👈 se mantiene para eliminar
};

export function FormaPagoTableRow({ row, selected, onSelectRow, onEdit, onDelete, }: FormaPagoTableRowProps) {
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

        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.payment_method}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.description}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.is_banked}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.operation_number}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.payer_account_rfc}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '10%' }}>{row.payer_account}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '10%' }}>{row.payer_account_pattern}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.beneficiary_account_rfc}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.beneficiary_account}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '10%' }}>{row.beneficiary_account_pattern}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.payment_chain_type}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.payer_bank_name_if_external}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '10%' }}>{row.effective_start_date}</TableCell>
        <TableCell align="center" size="small" sx={{ width: '5%' }}>{row.effective_end_date}</TableCell>

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
