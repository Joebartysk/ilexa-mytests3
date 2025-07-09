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

export type NolocalizableProps = {
  rfc: string,
  company_name: string,
  type_person: string,
  supposed: string,
  dates_of_firts_publication?: string, //Se agrega ? para indicar que es opcional
  federal_entity: string
};

type NolocalizableTableRowProps = {
  row: NolocalizableProps;
  selected: boolean;
  onSelectRow: () => void;
};

export function NolocalizableTableRow({ row, selected, onSelectRow }: NolocalizableTableRowProps) {
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

        <TableCell component="th" scope="row">
          <Box
            sx={{
              gap: 2,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            {row.rfc}
          </Box>
        </TableCell>

        <TableCell size="small" sx={{ width: '25%' }}>{row.company_name}</TableCell>

        <TableCell size="small" sx={{ width: '10%' }}>{row.type_person}</TableCell>

        <TableCell size="small" sx={{ width: '15%' }}>{row.supposed}</TableCell>

        <TableCell size="small" sx={{ width: '15%' }}>{row.dates_of_firts_publication}</TableCell>

        <TableCell size="small" sx={{ width: '20%' }}>{row.federal_entity}</TableCell>
       
      </TableRow>
    </>
  );
}
