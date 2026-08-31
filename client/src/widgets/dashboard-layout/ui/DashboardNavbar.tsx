import { UserChip } from '@/entities/user';
import { ROUTE_PATHS, SITE_CONFIG } from '@/shared/config';
import { ThemeToggleButton } from '@/shared/ui';
import { HeaderLogoDesktop, HeaderLogoMobile } from '@/shared/ui/logo';
import { Logout as LogoutIcon, Menu as MenuIcon } from '@mui/icons-material';
import { AppBar, Box, Button, IconButton, Toolbar } from '@mui/material';

import { useLogout } from '@/features/auth';

interface NavbarProps {
  onToggleDrawer: () => void;
}

export const DashboardNavbar = ({ onToggleDrawer }: NavbarProps) => {
  const { mutate: logout, isPending: isLogoutPending } = useLogout();

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: theme => theme.zIndex.drawer + 1,
        boxShadow: theme => theme.shadows[4],
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          edge="start"
          onClick={onToggleDrawer}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
          <HeaderLogoDesktop
            headerLogoText={SITE_CONFIG.NAME}
            href={ROUTE_PATHS.DASHBOARD}
          />
          <HeaderLogoMobile
            headerLogoText={SITE_CONFIG.SHORT_NAME}
            href={ROUTE_PATHS.DASHBOARD}
          />
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <ThemeToggleButton />
          <UserChip />
          <Button
            color="inherit"
            startIcon={<LogoutIcon />}
            onClick={() => logout()}
            sx={{ textTransform: 'none' }}
          >
            {isLogoutPending ? 'Выход...' : 'Выход'}
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};
