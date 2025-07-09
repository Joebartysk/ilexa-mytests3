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

export type CodigoPostalProps = {
  id: string,
  c_codigopostal: string,
	c_localidad: string,
	c_estado: string,
	fecha_inicio_vigencia: string,
	descripcion_del_uso_horario: string,
	dia_inicio_horario_verano: string,
	dia_inicio_horario_invierno: string,
	diferencia_horario_invierno: string,
	c_municipio: string,
	estimulo_franja_fronteriza: string,
	fecha_fin_vigencia: string,
	mes_inicio_horario_verano: string,
	dia_inicio_horario_verano_1: string,
	mes_inicio_horario_invierno: string,
	dia_inicio_horario_invierno_1: string
};

type CodigoPostalTableRowProps = {
  row: CodigoPostalProps;
  selected: boolean;
  onSelectRow: () => void;
  onEdit: () => void;
  onDelete: () => void;
};

export function CodigoPostalTableRow({ row, selected, onSelectRow, onEdit, onDelete }: CodigoPostalTableRowProps) {
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

        <TableCell size="small" sx={{ width: '300px' }}>{row.c_codigopostal}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.c_localidad}</TableCell>
        <TableCell size="small" sx={{ width: '80px' }}>{row.c_estado}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.fecha_inicio_vigencia}</TableCell>
        <TableCell size="small" sx={{ width: '80px' }}>{row.descripcion_del_uso_horario}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.dia_inicio_horario_verano}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.dia_inicio_horario_invierno}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.diferencia_horario_invierno}</TableCell>
        <TableCell size="small" sx={{ width: '80px' }}>{row.c_municipio}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.estimulo_franja_fronteriza}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.fecha_fin_vigencia}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.mes_inicio_horario_verano}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.dia_inicio_horario_verano_1}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.mes_inicio_horario_invierno}</TableCell>
        <TableCell size="small" sx={{ width: '300px' }}>{row.dia_inicio_horario_invierno_1}</TableCell>

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
