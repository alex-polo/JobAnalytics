import { notify } from '@/shared/lib';
import { Alert, Snackbar } from '@mui/material';
import { useEffect, useState } from 'react';

export const GlobalSnackbar = () => {
  const [state, setState] = useState({
    open: false,
    message: '',
    severity: 'info' as any,
  });

  useEffect(() => {
    return notify.subscribe(({ message, severity }) => {
      setState({ open: true, message, severity });
    });
  }, []);

  const handleClose = () => setState(prev => ({ ...prev, open: false }));

  return (
    <Snackbar
      open={state.open}
      autoHideDuration={4000}
      onClose={handleClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      sx={{
        mb: 1,
        mr: 1,
      }}
    >
      <Alert
        onClose={handleClose}
        severity={state.severity}
        variant="filled"
        sx={{
          width: '100%',
          minWidth: '320px',
          fontWeight: 500,
          borderRadius: '3px',
          boxShadow: theme => theme.shadows[6],
        }}
      >
        {state.message}
      </Alert>
    </Snackbar>
  );
};
