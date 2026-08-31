import { Menu as MenuIcon } from '@mui/icons-material';
import {
  AppBar,
  Box,
  Button,
  Container,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Toolbar,
  Typography,
} from '@mui/material';
import { useState } from 'react';
import { Link } from 'react-router-dom';

import { useSession } from '@/shared/api';
import { PUBLIC_NAVIGATION, ROUTE_PATHS, SITE_CONFIG } from '@/shared/config';
import {
  HeaderLogoDesktop,
  HeaderLogoMobile,
  ThemeToggleButton,
} from '@/shared/ui';
import LoginIcon from '@mui/icons-material/ExitToApp';

export const PublicHeader = () => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const { data: session } = useSession();
  const isAuth = session?.isAuth;

  const toggleDrawer =
    (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
      if (
        event.type === 'keydown' &&
        ((event as React.KeyboardEvent).key === 'Tab' ||
          (event as React.KeyboardEvent).key === 'Shift')
      ) {
        return;
      }
      setIsDrawerOpen(open);
    };

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{ borderBottom: '1px solid', borderColor: 'divider' }}
    >
      <Container maxWidth={false} disableGutters>
        <Toolbar sx={{ px: { xs: 2, md: 4 } }}>
          {/* Logo Desktop */}
          <HeaderLogoDesktop
            headerLogoText={SITE_CONFIG.NAME}
            href={ROUTE_PATHS.HOME}
          />

          {/* Mobile Menu Trigger */}
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton onClick={toggleDrawer(true)} color="inherit">
              <MenuIcon />
            </IconButton>

            <Drawer
              anchor="left"
              open={isDrawerOpen}
              onClose={toggleDrawer(false)}
              slotProps={{
                paper: {
                  sx: { width: '70%', maxWidth: 300 },
                },
              }}
            >
              <Box
                sx={{ p: 2, height: '100%' }}
                role="presentation"
                onClick={toggleDrawer(false)}
                onKeyDown={toggleDrawer(false)}
              >
                <Typography variant="h6" sx={{ my: 2, fontWeight: 700, px: 2 }}>
                  Меню
                </Typography>
                <Divider />
                <List>
                  {PUBLIC_NAVIGATION.map(page => (
                    <ListItem key={page.name} disablePadding>
                      <ListItemButton
                        component={page.isExternal ? 'a' : Link}
                        to={!page.isExternal ? page.path : undefined}
                        href={page.isExternal ? page.path : undefined}
                        target={page.isExternal ? '_blank' : undefined}
                      >
                        <ListItemText primary={page.name} />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Drawer>
          </Box>

          {/* Logo Mobile */}
          <HeaderLogoMobile
            headerLogoText={SITE_CONFIG.SHORT_NAME}
            href={ROUTE_PATHS.HOME}
          />

          {/* Desktop menu */}
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, ml: 2 }}>
            {PUBLIC_NAVIGATION.map(page => (
              <Button
                key={page.name}
                color="inherit"
                component={page.isExternal ? 'a' : Link}
                to={!page.isExternal ? page.path : undefined}
                href={page.isExternal ? page.path : undefined}
                target={page.isExternal ? '_blank' : undefined}
                sx={{ my: 2, display: 'block', textTransform: 'none' }}
              >
                {page.name}
              </Button>
            ))}
          </Box>

          {/* Theme and login buttons */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <ThemeToggleButton />
            {isAuth ? (
              <Button
                component={Link}
                to={ROUTE_PATHS.DASHBOARD}
                variant="outlined"
                color="inherit"
                sx={{ borderRadius: 2, textTransform: 'none' }}
              >
                Панель управления
              </Button>
            ) : (
              <Button
                component={Link}
                to={ROUTE_PATHS.LOGIN}
                variant="outlined"
                color="inherit"
                startIcon={<LoginIcon />}
                sx={{ borderRadius: 2, textTransform: 'none' }}
              >
                Вход
              </Button>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
