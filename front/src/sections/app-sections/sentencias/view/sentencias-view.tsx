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

// API
import ApiService from '../../../../api/api.service';
import { TableNoData } from '../../sentencias/table-no-data';
import { TableEmptyRows } from '../../sentencias/table-empty-rows';
import { SentenciasTableRow } from '../../sentencias/sentencias-table-row';
import { SentenciasTableHead } from '../../sentencias/sentencias-table-head';
import { emptyRows, applyFilter, getComparator } from '../../sentencias/utils';
import { SentenciasTableToolbar } from '../../sentencias/sentencias-table-toolbar';

import type { SentenciasProps } from '../../sentencias/sentencias-table-row';

// ----------------------------------------------------------------------

export function SentenciasView() {
  const table = useTable();

  const [filterName, setFilterName] = useState('');

  const [_sentencias, setSentencias] = useState<SentenciasProps[]>([]);

  const apiService = new ApiService();

  useEffect(() => {
    const fetchsentencias = async () => {
      try {
        const data = await apiService.getAll_sentences();
        setSentencias(data);
      } catch (error) {
        console.error('Error al recuperar lista de RFCs sentencias:', error);
        // Puedes manejar el error de manera más específica si es necesario
      }
    };

    fetchsentencias();
  }, [apiService]);

  const dataFiltered: SentenciasProps[] = applyFilter({
    inputData: _sentencias,
    comparator: getComparator(table.order, table.orderBy),
    filterName,
  });

  const notFound = !dataFiltered.length && !!filterName;

  return (
    <DashboardContent maxWidth={false}>
            
          <Box
            sx={{
              mb: 1,
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
            }}
          >
            <ExportMenu filename="sentences" schema="cfdi_system" table="sentences" />
    
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
              <SentenciasTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_sentencias.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _sentencias.map((sentencias) => sentencias.rfc)
                  )
                }
                headLabel={[
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
                    <SentenciasTableRow
                      key={row.rfc}
                      row={row}
                      selected={table.selected.includes(row.rfc)}
                      onSelectRow={() => table.onSelectRow(row.rfc)}
                    />
                  ))}

                <TableEmptyRows
                  height={68}
                  emptyRows={emptyRows(table.page, table.rowsPerPage, _sentencias.length)}
                />

                {notFound && <TableNoData searchQuery={filterName} />}
              </TableBody>
            </Table>
          </TableContainer>
        </Scrollbar>

        <TablePagination
          component="div"
          page={table.page}
          count={_sentencias.length}
          rowsPerPage={table.rowsPerPage}
          onPageChange={table.onChangePage}
          rowsPerPageOptions={[5, 10, 25]}
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
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [selected, setSelected] = useState<string[]>([]);
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');

  const onSort = useCallback(
    (id: string) => {
      const isAsc = orderBy === id && order === 'asc';
      setOrder(isAsc ? 'desc' : 'asc');
      setOrderBy(id);
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
