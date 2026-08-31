import LiveTvIcon from '@mui/icons-material/LiveTv';
import { Typography } from '@mui/material';
import { Link } from 'react-router-dom';

interface HeaderLogoProps {
  headerLogoText: string;
  href: string;
}

export const HeaderLogoDesktop = ({
  headerLogoText,
  href,
}: HeaderLogoProps) => {
  return (
    <Typography
      variant="h6"
      noWrap
      component={Link}
      to={href}
      sx={{
        mr: 2,
        display: { xs: 'none', md: 'flex' }, // Show only on desktop
        fontFamily: 'sans-serif',
        fontWeight: 800,
        letterSpacing: '.1rem',
        color: 'inherit',
        textDecoration: 'none',
        alignItems: 'center',
      }}
    >
      <LiveTvIcon sx={{ mr: 1, fontSize: 28, transform: 'translateY(-1px)' }} />

      {headerLogoText}
    </Typography>
  );
};

export const HeaderLogoMobile = ({ headerLogoText, href }: HeaderLogoProps) => {
  return (
    <Typography
      variant="h5"
      noWrap
      component={Link}
      to={href}
      sx={{
        display: { xs: 'flex', md: 'none' }, // Show only on mobile
        flexGrow: 1,
        fontFamily: 'monospace',
        fontWeight: 700,
        letterSpacing: '.3rem',
        color: 'inherit',
        textDecoration: 'none',
        alignItems: 'center',
      }}
    >
      <LiveTvIcon sx={{ mr: 1, fontSize: 28, transform: 'translateY(-1px)' }} />
      {headerLogoText}
    </Typography>
  );
};
