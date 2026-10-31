import CloseIcon from '@mui/icons-material/Close';
import FilterListIcon from '@mui/icons-material/FilterList';
import {
  Badge,
  Box,
  Button,
  Divider,
  Drawer,
  IconButton,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { useState } from 'react';
import { useResumeMatchFilters } from '../model';
import { ResumeMatchFiltersForm } from './match-filters-form';

export const ResumeMatchFiltersDrawer = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [open, setOpen] = useState(false);
  const { filters } = useResumeMatchFilters();

  const activeCount = [
    filters.search !== '',
    filters.date !== 'all',
    filters.location,
  ].filter(Boolean).length;

  return (
    <>
      <Button
        variant="outlined"
        startIcon={
          <Badge badgeContent={activeCount} color="primary">
            <FilterListIcon />
          </Badge>
        }
        onClick={() => setOpen(true)}
      >
        Фильтр
      </Button>

      <Drawer
        anchor="right"
        open={open}
        onClose={() => setOpen(false)}
        {...(isMobile
          ? { fullScreen: true }
          : { PaperProps: { sx: { width: 360 } } })}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            p: 2,
          }}
        >
          <Typography variant="h6">Фильтр</Typography>
          <IconButton onClick={() => setOpen(false)}>
            <CloseIcon />
          </IconButton>
        </Box>
        <Divider />
        <Box sx={{ p: 2 }}>
          <ResumeMatchFiltersForm />
        </Box>
      </Drawer>
    </>
  );
};
