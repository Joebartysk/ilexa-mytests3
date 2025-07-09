import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

import { Button } from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';

type ColumnDefinition = {
  header: string;
  key: string;
};

type ExportPDFProps = {
  data: any[];
  filename: string;
  columns: ColumnDefinition[];
};

export default function ExportPDFButton({ data, filename, columns }: ExportPDFProps) {
  const exportPDF = () => {
    const doc = new jsPDF();
    const headers = columns.map((col) => col.header);
    const body = data.map((row) => columns.map((col) => row[col.key] ?? ''));

    autoTable(doc, {
      head: [headers],
      body,
    });

    doc.save(`${filename}.pdf`);
  };

  return (
    <Button
      variant="outlined"
      color="primary"
      startIcon={<PictureAsPdfIcon />}
      onClick={exportPDF}
    >
      Exportar PDF
    </Button>
  );
}

