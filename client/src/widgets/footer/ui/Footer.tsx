import { PUBLIC_NAVIGATION, SITE_CONFIG } from '@/shared/config';
import { Box, Container, Link, Stack, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

export const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 1.1,
        px: { xs: 2, md: 4 },
        mt: 'auto',
        borderTop: '1px solid',
        borderColor: 'divider',
        backgroundColor: 'background.paper',
      }}
    >
      <Container maxWidth={false} disableGutters>
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          justifyContent="space-between"
          alignItems="center"
          spacing={2}
        >
          <Stack direction="row" spacing={3} alignItems="center">
            {PUBLIC_NAVIGATION.map(page => (
              <Link
                key={page.name}
                component={page.isExternal ? 'a' : RouterLink}
                to={!page.isExternal ? page.path : undefined}
                href={page.isExternal ? page.path : undefined}
                target={page.isExternal ? '_blank' : undefined}
                variant="body2"
                color="text.secondary"
                underline="hover"
                sx={{ fontSize: '0.85rem' }}
              >
                {page.name}
              </Link>
            ))}
          </Stack>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ fontSize: '0.85rem' }}
          >
            © {new Date().getFullYear()} {SITE_CONFIG.NAME}
          </Typography>
        </Stack>
      </Container>
    </Box>
  );
};
