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

export type BlacklistProps = {
  alleged_dof_publication: string,
	final_dof_publication: string,
	rfc: string,
	taxpayers_who_distorted_sat?: string, 
	favorable_ruling_sat: string,
	id: string, 
	sat_page_publication_distorted?: string, 
	sat_page_publication_favorable_ruling?: string, 
	taxpayer_name: string,
	taxpayers_who_distorted_dof?: string, 
	favorable_ruling_dof?: string,
	taxpayer_situation: string, //Sentencia
	distorted_dof_publication?: string, 
	dof_publication_favorable_ruling?: string, 
	sat_presumption_number_date?: string,
	definitive_sat_document?: string,
	presumptive_sat_page_publication?: string, 
	final_sat_page_publication?: string,
	dof_presumption_number_date?: string, 
	definitive_dof_document?: string
};

type BlacklistTableRowProps = {
  row: BlacklistProps;
  selected: boolean;
  onSelectRow: () => void;
};

export function BlacklistTableRow({ row, selected, onSelectRow }: BlacklistTableRowProps) {
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


        <TableCell component="th" scope="row" size="small" sx={{ width: '1%' }}>
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

        <TableCell size="small" sx={{ width: '100px' }} >{row.rfc}</TableCell>
        <TableCell size="small" sx={{ width: '350px' }} >{row.taxpayer_name}</TableCell>
        <TableCell size="small" 
          sx={{ width: '150px', 
                color:
                    row.taxpayer_situation === 'Definitivo'
                      ? 'red'
                      : row.taxpayer_situation === 'Sentencia Favorable'
                      ? 'green'
                      : row.taxpayer_situation === 'Desvirtuado'
                      ? 'orange'
                      : 'black',
                fontWeight: 'bold', }}>{formatSituation(row.taxpayer_situation)}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }} >{row.dof_presumption_number_date}</TableCell>
        <TableCell size="small" sx={{ width: '200px' }}>{row.presumptive_sat_page_publication}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.definitive_dof_document}</TableCell>
        <TableCell size="small" sx={{ width: '200px' }}>{row.alleged_dof_publication}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.taxpayers_who_distorted_sat}</TableCell>
        <TableCell size="small" sx={{ width: '200px' }}>{row.sat_page_publication_distorted}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.taxpayers_who_distorted_dof}</TableCell>
        <TableCell size="small" sx={{ width: '80px' }}>{row.distorted_dof_publication}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.definitive_sat_document}</TableCell>
        <TableCell size="small" sx={{ width: '200px' }}>{row.final_sat_page_publication}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.dof_publication_favorable_ruling}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.final_dof_publication}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.favorable_ruling_sat}</TableCell>
        <TableCell size="small" sx={{ width: '200px' }}>{row.sat_page_publication_favorable_ruling}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.favorable_ruling_dof}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.sat_presumption_number_date}</TableCell>

      </TableRow>

    </>
  );
}
