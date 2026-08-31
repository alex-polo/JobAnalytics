import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',

    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  colorSchemes: {
    light: {
      palette: {
        background: {
          default: '#f4f6f8',
          paper: '#ffffff',
        },
      },
    },
    dark: {
      palette: {
        background: {
          default: '#222222',
          paper: '#151515',
        },
      },
    },
  },
});
