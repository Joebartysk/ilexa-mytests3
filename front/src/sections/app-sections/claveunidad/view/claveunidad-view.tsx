import { useState, useEffect, useCallback } from 'react';

// Importaciones de Material UI agrupadas
import {
  Box, Card, Paper,Table, Button, TableBody, Typography, TableContainer, TablePagination,
  Dialog, DialogTitle, DialogContent, DialogContentText,DialogActions
} from '@mui/material';

// Importaciones del layout
import { DashboardContent } from 'src/layouts/dashboard';

// Importaciones de componentes
import { Iconify } from 'src/components/iconify';
import { Scrollbar } from 'src/components/scrollbar';
import ExportMenu from 'src/components/export/ExportMenu';
import CatalogModal from 'src/components/editcatalogs/CatalogModal';

// API
import ApiService from '../../../../api/api.service';
// Importaciones de componentes de tabla
import { TableNoData } from '../../claveunidad/table-no-data';
import { TableEmptyRows } from '../../claveunidad/table-empty-rows';
import { ClaveunidadTableRow } from '../../claveunidad/claveunidad-table-row';
import { ClaveunidadTableHead } from '../../claveunidad/claveunidad-table-head';
import { emptyRows, applyFilter, getComparator } from '../../claveunidad/utils';//Importación de utilidades
import { ClaveunidadTableToolbar } from '../../claveunidad/claveunidad-table-toolbar';

import type { ClaveunidadProps } from '../../claveunidad/claveunidad-table-row';

export function ClaveunidadView() {
  const table = useTable();

  const [filterName, setFilterName] = useState('');

  const [_claveunidad, setClaveunidad] = useState<ClaveunidadProps[]>([]);

  const apiService = new ApiService();

  const [openModal, setOpenModal] = useState(false); //Para agregar
  const [loading, setLoading] = useState(false);
  const [editItem, setEditItem] = useState<ClaveunidadProps | null>(null); //Para editar

  const [openConfirmDialog, setOpenConfirmDialog] = useState(false);//Validacion para antes de eliminar
  const [itemToDelete, setItemToDelete] = useState<ClaveunidadProps | null>(null);//Para eliminar
//===============================================

// Función para cargar datos
  const fetchClaveunidad = async () => {
    try {
      setLoading(true);
      const data = await apiService.getAll_claveunidad();
      setClaveunidad(data);
    } catch (error) {
      console.error('Error al recuperar lista de Calve Unidad:', error);
      // Aquí podrías mostrar un toast o mensaje de error
    } finally {
      setLoading(false);
    }
  };

  // Función para manejar el éxito del modal
  const handleModalSuccess = async (newItem?: ClaveunidadProps) => {
    try {
      if (newItem) {
        // Si el modal devuelve el nuevo item, agregarlo directamente
        setClaveunidad(prev => [...prev, newItem]);
      } else {
        // Si no, refrescar toda la lista
        await fetchClaveunidad();
      }
      setOpenModal(false);
    } catch (error) {
      console.error('Error al refrescar catalogo:', error);
    }
  };

  // Función para manejar actualización de elementos
  const handleItemUpdate = async (updatedItem: ClaveunidadProps) => {
    try {
      setClaveunidad(prev => 
        prev.map(item => item.id === updatedItem.id ? updatedItem : item)
      );
    } catch (error) {
      console.error('Error al actualizar elemento:', error);
    }
  };

  // Función para manejar eliminación de elementos
  const handleItemDelete = async (deletedId: string) => {
    try {
      await apiService.deleteCatalogItem('claveunidad', deletedId);
      setClaveunidad(prev => prev.filter(item => item.id !== deletedId));
    } catch (error) {
      console.error('Error al eliminar elemento:', error);
      // Aquí podrías mostrar un toast de error
    }
  };

  // Cargar datos al montar el componente
  useEffect(() => {
    fetchClaveunidad();
  }, []);


  ///=============================================

  const dataFiltered: ClaveunidadProps[] = applyFilter({
    inputData: _claveunidad,
    comparator: getComparator(table.order, table.orderBy),
    filterName,
  });

  const notFound = !dataFiltered.length && !!filterName;

  return (
    <DashboardContent maxWidth={false} >
      <Box
        sx={{
          mb: 1,
          display: 'flex',
          justifyContent: 'flex-end',
          alignItems: 'center',
        }}
      >

        <ExportMenu filename="c_clave_unidad" schema="cfdi_system" table="c_clave_unidad" />

        <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setOpenModal(true)}
                  sx={{ ml: 2 }}
                  disabled={loading}
                >
                  Agregar Clave Unidad
        </Button>
      </Box>
      
     <Card>

        <Scrollbar>
          <TableContainer component={Paper} sx={{ width: '100%', overflowX: 'auto' }} >
            <Table sx={{ borderCollapse: 'collapse',
                    '& td, & th': {
                        borderBottom: '1px solid rgba(224, 224, 224, 1)',
                        paddingTop: 0,
                        paddingBottom: 0,
                    }, width: '100%' }} // Para que se ajuste a los px asignados por columna
                    size="small" aria-label="a dense table">
              <ClaveunidadTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_claveunidad.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _claveunidad.map((claveunidad) => claveunidad.id)
                  )
                }
                headLabel={[
                  { id: 'id' , label: 'Id' },
                  { id: 'unit_code' , label: 'Clave unidad' },
                  { id: 'name' , label: 'Nombre' },
                  { id: 'description', label: 'Descripción' },
                  { id: 'nota' , label: 'Nota' },
                  { id: 'effective_start_date' , label: 'Fecha de inicio de vigencia' },
                  { id: 'effective_end_date' , label: 'Fecha de fin de vigencia' },
                  { id: 'symbol' , label: 'Símbolo' },
                  { id: 'edit', label: '', align: 'center' },
                ]}
              />
              <TableBody>
                {dataFiltered
                  .slice(
                    table.page * table.rowsPerPage,
                    table.page * table.rowsPerPage + table.rowsPerPage
                  )
                  .map((row) => (
                    <ClaveunidadTableRow
                      key={row.id}
                      row={row}
                      selected={table.selected.includes(row.id)}
                      onSelectRow={() => table.onSelectRow(row.id)}
                      onEdit={async () => {
                        setEditItem(row);      // establece el ítem actual en edición
                        setOpenModal(true);    // abre el modal con los datos precargados
                      }}
                      onDelete={async () => {
                        setItemToDelete(row);
                        setOpenConfirmDialog(true);
                      }}
                    />
                  ))}

                <TableEmptyRows
                  height={30}
                  emptyRows={emptyRows(table.page, table.rowsPerPage, _claveunidad.length)}
                />

                {notFound && <TableNoData searchQuery={filterName} />}
              </TableBody>
            </Table>
          </TableContainer>
        </Scrollbar>

        <TablePagination
          component="div"
          page={table.page}
          count={dataFiltered.length} // Cambio: usar dataFiltered.length en lugar de _exportacion.length
          rowsPerPage={table.rowsPerPage}
          onPageChange={table.onChangePage}
          rowsPerPageOptions={[10, 15, 25, 50, 100]}
          onRowsPerPageChange={table.onChangeRowsPerPage}
        />
      </Card>

      <CatalogModal
        open={openModal}
        onClose={() => {
          setOpenModal(false);
          setEditItem(null); // Limpiar estado al cerrar
        }}
        catalogKey="claveunidad"
        title={editItem ? 'Editar Calve Unidad' : 'Agregar Calve Unidad'}
        onSuccess={editItem ? handleItemUpdate : handleModalSuccess}
        initialData={editItem ?? undefined} // 👈 Nuevo
      />
      

      <Dialog
          open={openConfirmDialog}
          onClose={() => {
            setOpenConfirmDialog(false);
            setItemToDelete(null);
          }}

          
        >
          <DialogTitle>Confirmar eliminación</DialogTitle>
          <DialogContent>
            <DialogContentText>
              ¿Estás segura de que deseas eliminar el registro{' '}
              <strong>{itemToDelete?.description}</strong>?
              Esta acción no se puede deshacer.
            </DialogContentText>
          </DialogContent>

          <DialogActions>
            <Button
              onClick={() => {
                setOpenConfirmDialog(false);
                setItemToDelete(null);
              }}
            >
              Cancelar
            </Button>

            <Button
              onClick={async () => {
                if (itemToDelete) {
                  await handleItemDelete(itemToDelete.id);
                }
                setOpenConfirmDialog(false);
                setItemToDelete(null);
              }}
              color="error"
              variant="contained"
            >
              Eliminar
            </Button>
          </DialogActions>
        </Dialog>

    </DashboardContent>
  );
}

// ----------------------------------------------------------------------

export function useTable() {
  const [page, setPage] = useState(0);
  const [orderBy, setOrderBy] = useState('name');
  const [rowsPerPage, setRowsPerPage] = useState(15); //Cambia de 5 a 15 para mostrar más filas
  const [selected, setSelected] = useState<string[]>([]);
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');

  const onSort = useCallback(
    (rfc: string) => {
      const isAsc = orderBy === rfc && order === 'asc';
      setOrder(isAsc ? 'desc' : 'asc');
      setOrderBy(rfc);
    },
    [order, orderBy]
  );

  const onSelectAllRows = useCallback((checked: boolean, newSelecteds: string[]) => {
    if (checked) {
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  }, []);

  const onSelectRow = useCallback(
    (inputValue: string) => {
      const newSelected = selected.includes(inputValue)
        ? selected.filter((value) => value !== inputValue)
        : [...selected, inputValue];

      setSelected(newSelected);
    },
    [selected]
  );

  const onResetPage = useCallback(() => {
    setPage(0);
  }, []);

  const onChangePage = useCallback((event: unknown, newPage: number) => {
    setPage(newPage);
  }, []);

  const onChangeRowsPerPage = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setRowsPerPage(parseInt(event.target.value, 10));
      onResetPage();
    },
    [onResetPage]
  );

  return {
    page,
    order,
    onSort,
    orderBy,
    selected,
    rowsPerPage,
    onSelectRow,
    onResetPage,
    onChangePage,
    onSelectAllRows,
    onChangeRowsPerPage,
  };
}
