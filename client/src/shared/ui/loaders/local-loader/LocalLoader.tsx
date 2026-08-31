import { Box, CircularProgress } from '@mui/material';

export const LocalLoader = () => (
  <Box
    sx={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      p: 3,
      width: '100%',
    }}
  >
    <CircularProgress size={40} />
  </Box>
);
