import { Backdrop, CircularProgress } from '@mui/material';

export const GlobalLoader = () => (
  <Backdrop
    open={true}
    sx={{ color: '#f8f8f8ff', zIndex: theme => theme.zIndex.drawer + 1 }}
  >
    <CircularProgress color="inherit" />
  </Backdrop>
);
