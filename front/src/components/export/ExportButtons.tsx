// ExportCSVXLSButtons.tsx
import Papa from 'papaparse';
import ExcelJS from 'exceljs';
import { useState } from 'react';
import { saveAs } from 'file-saver';

import GridOnIcon from '@mui/icons-material/GridOn';
import TableViewIcon from '@mui/icons-material/TableView';
import DownloadIcon from '@mui/icons-material/FileDownload';
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';

type ColumnDefinition = {
  header: string;
  key: string;
};

type ExportProps = {
  data: any[];
  filename: string;
  columns: ColumnDefinition[];
};

export default function ExportButtons({ data, filename, columns }: ExportProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const exportCSV = () => {
    const csvData = data.map((row) => {
      const filteredRow: Record<string, any> = {};
      columns.forEach((col) => {
        filteredRow[col.header] = row[col.key];
      });
      return filteredRow;
    });

    const csv = Papa.unparse(csvData);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `${filename}.csv`);
    handleClose();
  };

  const exportToExcel = async () => {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Export');

    worksheet.columns = columns.map((col) => ({
      header: col.header,
      key: col.key,
      width: 20,
    }));

    data.forEach((item) => {
      worksheet.addRow(item);
    });

    const buffer = await workbook.xlsx.writeBuffer();
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    saveAs(blob, `${filename}.xlsx`);
    handleClose();
  };

  return (
    <>
      <Button
        variant="contained"
        color="primary"
        startIcon={<DownloadIcon />}
        onClick={handleClick}
      >
        Exportar
      </Button>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem onClick={exportCSV}>
          <ListItemIcon>
            <TableViewIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Exportar CSV</ListItemText>
        </MenuItem>
        <MenuItem onClick={exportToExcel}>
          <ListItemIcon>
            <GridOnIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Exportar XLS</ListItemText>
        </MenuItem>
      </Menu>
    </>
  );
}
