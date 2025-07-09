import { useState } from 'react';

import { Menu, MenuItem, Button } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

import ApiService from '../../api/api.service';

interface ExportMenuProps {
  filename: string;
  schema: string;
  table: string;
}

function ExportMenu({ filename, schema, table }: ExportMenuProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const apiService = new ApiService();

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => setAnchorEl(null);

  const handleExport = async (format: 'xlsx' | 'csv') => {
    handleClose();
    try {
      await apiService.exportAndDownload(format, filename, schema, table);
    } catch (error) {
      console.error(`Error al exportar ${format.toUpperCase()}:`, error);
    }
  };

  return (
    <>
      <Button
        variant="contained"
        color="primary"
        onClick={handleClick}
        startIcon={<DownloadIcon />}
      >
        Exportar
      </Button>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem onClick={() => handleExport('xlsx')}>Exportar Excel</MenuItem>
        <MenuItem onClick={() => handleExport('csv')}>Exportar CSV</MenuItem>
      </Menu>
    </>
  );
}

export default ExportMenu;
