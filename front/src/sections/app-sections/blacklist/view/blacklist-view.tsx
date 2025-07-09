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
// Importaciones de componentes de tabla
import { TableNoData } from '../../blacklist/table-no-data';
import { TableEmptyRows } from '../../blacklist/table-empty-rows';
import { BlacklistTableRow } from '../../blacklist/blacklist-table-row';
import { BlacklistTableHead } from '../../blacklist/blacklist-table-head';
import { emptyRows, applyFilter, getComparator } from '../../blacklist/utils';//Importación de utilidades
import { BlacklistTableToolbar } from '../../blacklist/blacklist-table-toolbar';

import type { BlacklistProps } from '../../blacklist/blacklist-table-row';

export function BlacklistView() {
  const table = useTable();

  const [filterName, setFilterName] = useState('');

  const [_blacklist, setBlacklist] = useState<BlacklistProps[]>([]);

  const apiService = new ApiService();

  useEffect(() => {
    const fetchBlacklist = async () => {
      try {
        const data = await apiService.getAll_blacklist();
        setBlacklist(data);
      } catch (error) {
        console.error('Error al recuperar listas negras:', error);
      }
    };

    fetchBlacklist();
  }, [apiService]);

  const dataFiltered: BlacklistProps[] = applyFilter({
    inputData: _blacklist,
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
        <ExportMenu filename="sat_blacklist" schema="cfdi_system" table="sat_blacklist" />

      </Box>

      
     <Card>
        <Scrollbar>
          <TableContainer component={Paper} sx={{ width: '100%', overflowX: 'auto' }} >
            <Table sx={{ borderCollapse: 'collapse',
                    '& td, & th': {
                        borderBottom: '1px solid rgba(224, 224, 224, 1)',
                        paddingTop: 0,
                        paddingBottom: 0,
                    }, width: '4000px' }} // Para que se ajuste a los px asignados por columna
                    size="small" aria-label="a dense table">
              <BlacklistTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_blacklist.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _blacklist.map((blacklist) => blacklist.rfc)
                  )
                }
                headLabel={[
                  { id: 'id' , label: 'Id' },
                  { id: 'rfc' , label: 'RFC' },
                  { id: 'taxpayer_name' , label: 'Contribuyente' },
                  { id: 'taxpayer_situation' , label: 'Situación del contribuyente' },
                  { id: 'dof_presumption_number_date' , label: 'Número y fecha de oficio global de presunción SAT' },
                  { id: 'presumptive_sat_page_publication' , label: 'Publicación página SAT presuntos' },
                  { id: 'definitive_dof_document' , label: 'Número y fecha de oficio global de presunción DOF' },
                  { id: 'alleged_dof_publication' , label: 'Publicación DOF presuntos' },
                  { id: 'taxpayers_who_distorted_sat' , label: 'Número y fecha de oficio global de contribuyentes que desvirtuaron SAT' },
                  { id: 'sat_page_publication_distorted' , label: 'Publicación página SAT desvirtuados' },
                  { id: 'taxpayers_who_distorted_dof' , label: 'Número y fecha de oficio global de contribuyentes que desvirtuaron DOF' },
                  { id: 'distorted_dof_publication' , label: 'Publicación DOF desvirtuados' },
                  { id: 'definitive_sat_document' , label: 'Número y fecha de oficio global de definitivos SAT' },
                  { id: 'final_sat_page_publication' , label: 'Publicación página SAT definitivos' },
                  { id: 'dof_publication_favorable_ruling' , label: 'Número y fecha de oficio global de definitivos DOF' },
                  { id: 'final_dof_publication' , label: 'Publicación DOF definitivos' },
                  { id: 'favorable_ruling_sat' , label: 'Número y fecha de oficio global de sentencia favorable SAT' },
                  { id: 'sat_page_publication_favorable_ruling' , label: 'Publicación página SAT sentencia favorable' },
                  { id: 'favorable_ruling_dof' , label: 'Número y fecha de oficio global de sentencia favorable DOF' },
                  { id: 'sat_presumption_number_date' , label: 'Número y fecha de oficio global de presunción' },
                ]}
              />
              <TableBody>
                {dataFiltered
                  .slice(
                    table.page * table.rowsPerPage,
                    table.page * table.rowsPerPage + table.rowsPerPage
                  )
                  .map((row) => (
                    <BlacklistTableRow
                      key={row.rfc}
                      row={row}
                      selected={table.selected.includes(row.rfc)}
                      onSelectRow={() => table.onSelectRow(row.rfc)}
                    />
                  ))}

                <TableEmptyRows
                  height={68}
                  emptyRows={emptyRows(table.page, table.rowsPerPage, _blacklist.length)}
                />

                {notFound && <TableNoData searchQuery={filterName} />}
              </TableBody>
            </Table>
          </TableContainer>
        </Scrollbar>

        <TablePagination
          component="div"
          page={table.page}
          count={dataFiltered.length} // Cambio: usar dataFiltered.length en lugar de _blacklist.length
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
