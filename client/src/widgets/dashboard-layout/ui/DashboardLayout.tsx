import { ROUTE_PATHS } from '@/shared/config';
import { Breadcrumbs, Footer } from '@/widgets';
import {
  Dashboard as DashIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { Box, Paper } from '@mui/material';
import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { DashboardNavbar } from './DashboardNavbar';
import { DashboardSidebar } from './DashboardSidebar';

const DRAWER_WIDTH = 240;
const NAVBAR_HEIGHT = 64;

export const DashboardLayout = () => {
  const [open, setOpen] = useState(true);

  const navItems = [
    { text: 'Dashboard', icon: <DashIcon />, path: ROUTE_PATHS.DASHBOARD },
    { text: 'Profile', icon: <PersonIcon />, path: ROUTE_PATHS.PROFILE },
    { text: 'Settings', icon: <SettingsIcon />, path: ROUTE_PATHS.SETTINGS },
  ];

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <DashboardNavbar onToggleDrawer={() => setOpen(!open)} />

      <DashboardSidebar
        open={open}
        onClose={() => setOpen(false)}
        items={navItems}
        width={DRAWER_WIDTH}
      />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          minHeight: `calc(100vh - ${NAVBAR_HEIGHT}px)`,
          marginTop: `${NAVBAR_HEIGHT}px`,
          width: { sm: open ? `calc(100% - ${DRAWER_WIDTH}px)` : '100%' },
          maxWidth: '100%',
          overflowX: 'hidden',
          backgroundColor: 'background.default',
          transition: theme => theme.transitions.create(['width', 'margin']),
        }}
      >
        <Box sx={{ p: 3, flexGrow: 1 }}>
          <Box sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
            <Breadcrumbs />
          </Box>
          <Paper
            elevation={0}
            sx={{
              p: { xs: 2, md: 4 },
              borderRadius: 1,
              border: '1px solid',
              borderColor: 'divider',
              minHeight: '40vh',
              boxShadow: '0px 2px 4px rgba(0,0,0,0.03)',
            }}
          >
            <Outlet />
          </Paper>
        </Box>
        <Footer />
      </Box>
    </Box>
  );
};
