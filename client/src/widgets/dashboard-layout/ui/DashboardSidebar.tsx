import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

/**
 * Sidebar component for the Dashboard
 * Handles both mobile (temporary) and desktop (persistent) navigation
 */
interface SidebarProps {
  open: boolean;
  onClose: () => void;
  items: Array<{ text: string; icon: React.ReactNode; path: string }>;
  width: number;
}

export const DashboardSidebar = ({
  open,
  onClose,
  items,
  width,
}: SidebarProps) => {
  const navigate = useNavigate();
  const location = useLocation();

  // Reusable content for both types of Drawers
  const drawerContent = (
    <List sx={{ pt: { xs: 2, sm: '80px' } }}>
      {items.map(item => (
        <ListItem key={item.text} disablePadding>
          <ListItemButton
            selected={location.pathname === item.path}
            onClick={() => {
              navigate(item.path);
              // Auto-close sidebar on mobile devices after clicking a link
              if (window.innerWidth < 600) onClose();
            }}
          >
            <ListItemIcon
              sx={{
                color:
                  location.pathname === item.path ? 'primary.main' : 'inherit',
              }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );

  return (
    <Box
      component="nav" // Semantic HTML tag for navigation
      sx={{
        width: { sm: open ? width : 0 }, // Dynamically adjust width based on state
        flexShrink: { sm: 0 },
        transition: theme => theme.transitions.create('width'), // Smooth expansion/collapse
      }}
    >
      {/* 1. MOBILE DRAWER: Slides over the content, used on small screens */}
      <Drawer
        variant="temporary"
        open={open}
        onClose={onClose}
        ModalProps={{ keepMounted: true }} // Optimized for mobile performance
        sx={{
          display: { xs: 'block', sm: 'none' }, // Visible ONLY on mobile
          '& .MuiDrawer-paper': { width },
        }}
      >
        {drawerContent}
      </Drawer>

      {/* 2. DESKTOP DRAWER: Pushes content to the right, used on large screens */}
      <Drawer
        variant="persistent"
        anchor="left"
        open={open}
        sx={{
          display: { xs: 'none', sm: 'block' }, // Visible ONLY on desktop
          '& .MuiDrawer-paper': {
            width,
            boxShadow: theme => theme.shadows[3], // Custom shadow style
            border: 'none',
          },
        }}
      >
        {drawerContent}
      </Drawer>
    </Box>
  );
};
