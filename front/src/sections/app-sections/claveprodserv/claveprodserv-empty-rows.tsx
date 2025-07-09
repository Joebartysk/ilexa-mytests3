import type { TableRowProps } from '@mui/material/TableRow';

import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';

// ----------------------------------------------------------------------

type ClaveProdServRowsProps = TableRowProps & {
  emptyRows: number;
  height?: number;
};

export function ClaveProdServRows({ emptyRows, height, sx, ...other }: ClaveProdServRowsProps) {
  if (!emptyRows) {
    return null;
  }

  return (
    <TableRow
      sx={[height && { height: height * emptyRows }, ...(Array.isArray(sx) ? sx : [sx])]}
      {...other}
    >
      <TableCell colSpan={9} />
    </TableRow>
  );
}
