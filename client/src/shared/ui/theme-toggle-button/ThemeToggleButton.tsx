import { Brightness4, Brightness7 } from '@mui/icons-material';
import { IconButton, Tooltip } from '@mui/material';
import { useColorScheme } from '@mui/material/styles';

export const ThemeToggleButton = () => {
  const { mode, setMode, systemMode } = useColorScheme();
  const isDark =
    mode === 'dark' || (mode === 'system' && systemMode === 'dark');

  if (!mode) return null;

  return (
    <Tooltip title={isDark ? 'Светлая тема' : 'Темная тема'}>
      <IconButton
        onClick={() => setMode(isDark ? 'light' : 'dark')}
        color="inherit"
        sx={{
          padding: '8px',
          transition: 'all 0.3s ease',
        }}
      >
        {isDark ? (
          <Brightness7 sx={{ color: '#ffb74d', fontSize: '1.4rem' }} />
        ) : (
          <Brightness4 sx={{ color: '#f9f9f9ff', fontSize: '1.4rem' }} />
        )}
      </IconButton>
    </Tooltip>
  );
};
