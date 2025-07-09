import React from 'react';

import Dialog from '@mui/material/Dialog';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

import GenericCatalogForm from './GenericCatalogForm';

import type { CatalogDataTypes } from '../../api/catalog.config';

type CatalogKey = keyof CatalogDataTypes;

interface CatalogModalProps<K extends CatalogKey> {
  open: boolean;
  onClose: () => void;
  catalogKey: K;
  title: string;
  onSuccess?: (item: CatalogDataTypes[K]) => void;
  initialData?: CatalogDataTypes[K];
  idField?: string;
}

function CatalogModal<K extends CatalogKey>({
  open,
  onClose,
  catalogKey,
  title,
  onSuccess,
  initialData,
  idField,
}: CatalogModalProps<K>) {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        {title}
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        <GenericCatalogForm<CatalogDataTypes[K]>
          catalogKey={catalogKey}
          initialData={initialData}
          idField={idField}
          onSuccess={(item) => {
            if (onSuccess) onSuccess(item);
            onClose();
          }}
        />
      </DialogContent>
    </Dialog>
  );
}

export default CatalogModal;



