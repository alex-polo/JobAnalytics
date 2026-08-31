import { AccountCircle } from '@mui/icons-material';
import {
  Chip,
  CircularProgress,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { useMe } from '../api/userApi';

export const UserChip = () => {
  const { data: user, isLoading, isError } = useMe();
  const theme = useTheme();

  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  if (isLoading) {
    return <CircularProgress size={20} color="inherit" />;
  }

  if (isError || !user?.email) {
    return (
      <Typography variant="body2" sx={{ opacity: 0.7, fontStyle: 'italic' }}>
        unknown user
      </Typography>
    );
  }

  return (
    <Chip
      icon={<AccountCircle sx={{ color: 'inherit !important' }} />}
      label={isMobile ? '' : user.email}
      variant="outlined"
      sx={{
        color: 'inherit',
        borderColor: 'rgba(255,255,255,0.2)',
        fontWeight: 500,
        fontSize: isMobile ? 12 : 14,
        height: 32,
        minWidth: isMobile ? 32 : 'auto',
        transition: 'all 0.2s ease-in-out',
        cursor: 'pointer',
        '& .MuiChip-label': { display: { xs: 'none', sm: 'block' } },
        '& .MuiChip-icon': {
          margin: isMobile ? 0 : '0 4px 0 8px',
        },
        '&:hover': {
          backgroundColor: 'rgba(255, 255, 255, 0.08)',
          borderColor: 'rgba(255, 255, 255, 0.5)',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        },
        '&:active': {
          backgroundColor: 'rgba(255, 255, 255, 0.12)',
        },
      }}
    />
  );
};
