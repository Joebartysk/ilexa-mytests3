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

//API
import ApiService from '../../../../api/api.service';
import { TableNoData } from '../../firmes/table-no-data';
import { TableEmptyRows } from '../../firmes/table-empty-rows';
import { FirmesTableRow } from '../../firmes/firmes-table-row';
import { FirmesTableHead } from '../../firmes/firmes-table-head';
import { FirmesTableToolbar } from '../../firmes/firmes-table-toolbar';
import { emptyRows, applyFilter, getComparator } from '../../firmes/utils';

import type { FirmesProps } from '../../firmes/firmes-table-row';


// ----------------------------------------------------------------------

export function FirmesView() {
  const table = useTable();

  const [filterName, setFilterName] = useState('');

  const [_firmes, setFirmes] = useState<FirmesProps[]>([]);

  const apiService = new ApiService();

  useEffect(() => {
    const fetchFirmes = async () => {
      try {
        const data = await apiService.getAll_firmes();
        setFirmes(data);
      } catch (error) {
        console.error('Error al recuperar lista de RFCs Firmes:', error);
        // Puedes manejar el error de manera más específica si es necesario
      }
    };

    fetchFirmes();
  }, [apiService]);

  const dataFiltered: FirmesProps[] = applyFilter({
    inputData: _firmes,
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

        <ExportMenu filename="firms" schema="cfdi_system" table="firms" />

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
              <FirmesTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_firmes.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _firmes.map((firmes) => firmes.rfc)
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
                    <FirmesTableRow
                      key={row.rfc}
                      row={row}
                      selected={table.selected.includes(row.rfc)}
                      onSelectRow={() => table.onSelectRow(row.rfc)}
                    />
                  ))}

                <TableEmptyRows
                  height={68}
                  emptyRows={emptyRows(table.page, table.rowsPerPage, _firmes.length)}
                />

                {notFound && <TableNoData searchQuery={filterName} />}
              </TableBody>
            </Table>
          </TableContainer>
        </Scrollbar>

        <TablePagination
          component="div"
          page={table.page}
          count={_firmes.length}
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
