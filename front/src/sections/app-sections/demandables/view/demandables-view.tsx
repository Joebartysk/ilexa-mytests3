import { useState, useEffect, useCallback } from 'react';

// Importaciones de Material UI agrupadas
import {
  Box, Card, Paper,Table, Button, TableBody, Typography, TableContainer, TablePagination
} from '@mui/material';

// Importaciones del layout
import { DashboardContent } from 'src/layouts/dashboard';

// Importaciones de componentes
import { Iconify } from 'src/components/iconify';
import { Scrollbar } from 'src/components/scrollbar';
import ExportMenu from 'src/components/export/ExportMenu';
import ExportPDFButton from 'src/components/export//ExportPDFButton';

// API
import ApiService from '../../../../api/api.service';
// Importaciones de componentes de tabla
import { TableNoData } from '../../demandables/table-no-data';
import { TableEmptyRows } from '../../demandables/table-empty-rows';
import { DemandablesTableRow } from '../../demandables/demandables-table-row';
import { emptyRows, applyFilter, getComparator } from '../../demandables/utils';//Importación de utilidades
import { DemandablesTableHead } from '../../demandables/demandables-table-head';
import { DemandablesTableToolbar } from '../../demandables/demandables-table-toolbar';

import type { DemandablesProps } from '../../demandables/demandables-table-row';

export function DemandablesView() {
  const table = useTable();

  const [filterName, setFilterName] = useState('');

  const [_demandables, setDemandables] = useState<DemandablesProps[]>([]);
  //console.log('_demandables', _demandables.length);

  const apiService = new ApiService();

  useEffect(() => {
    const fetchDemandables = async () => {
      try {
        const data = await apiService.getAllDemandables();
        setDemandables(data);
      } catch (error) {
        console.error('Error al recuperar lista de RFCs Demandables:', error);
        // Puedes manejar el error de manera más específica si es necesario
      }
    };

    fetchDemandables();
  }, [apiService]);

  const dataFiltered: DemandablesProps[] = applyFilter({
    inputData: _demandables,
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

        <ExportMenu filename="demandables" schema="cfdi_system" table="demandables" />

      </Box>

      
     <Card>

        <Scrollbar>
          <TableContainer component={Paper} sx={{ width: '100%', overflowX: 'auto' }} >
            <Table sx={{ borderCollapse: 'collapse',
                    '& td, & th': {
                        borderBottom: '1px solid rgba(224, 224, 224, 1)',
                        paddingTop: 0,
                        paddingBottom: 0,
                    }, width: '100%' }} 
                    
                    size="small" aria-label="a dense table">
              <DemandablesTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_demandables.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _demandables.map((demandables) => demandables.rfc)
                  )
                }
                headLabel={[
                  /*{ id: 'id', label: 'id' },*/
                  { id: 'rfc', label: 'RFC' },
                  { id: 'company_name', label: 'Razón social' },
                  { id: 'type_person', label: 'Tipo persona', align: 'center' },
                  { id: 'supposed', label: 'Supuesto' },
                  { id: 'dates_of_firts_publication', label: 'Fechas de primera publicación' },
                  { id: 'federal_entity', label: 'Entidad federativa' },
                ]}
              />
              <TableBody>
                {dataFiltered
                  .slice(
                    table.page * table.rowsPerPage,
                    table.page * table.rowsPerPage + table.rowsPerPage
                  )
                  .map((row) => (
                    <DemandablesTableRow
                      key={row.rfc}
                      row={row}
                      selected={table.selected.includes(row.rfc)}
                      onSelectRow={() => table.onSelectRow(row.rfc)}
                    />
                  ))}

                <TableEmptyRows
                  height={68}
                  emptyRows={emptyRows(table.page, table.rowsPerPage, _demandables.length)}
                />

                {notFound && <TableNoData searchQuery={filterName} />}
              </TableBody>
            </Table>
          </TableContainer>
        </Scrollbar>

        <TablePagination
          component="div"
          page={table.page}
          count={dataFiltered.length} // Cambio: usar dataFiltered.length en lugar de _demandables.length
          rowsPerPage={table.rowsPerPage}
          onPageChange={table.onChangePage}
          rowsPerPageOptions={[10, 25, 50, 100]}
          onRowsPerPageChange={table.onChangeRowsPerPage}
        />
      </Card>
    </DashboardContent>
  );
}

// ----------------------------------------------------------------------

export function useTable() {
  const [page, setPage] = useState(0);
  const [orderBy, setOrderBy] = useState('name');
  const [rowsPerPage, setRowsPerPage] = useState(25); //Cambia de 5 a 25 para mostrar más filas
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