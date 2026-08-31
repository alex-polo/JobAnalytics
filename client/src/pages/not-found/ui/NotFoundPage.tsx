import { Box, Button, Container, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <Container sx={{ display: 'flex', alignItems: 'center', height: '70vh' }}>
      <Box sx={{ textAlign: 'center', width: '100%' }}>
        <Typography
          variant="h1"
          sx={{ fontSize: '10rem', fontWeight: 700, color: 'primary.main' }}
        >
          404
        </Typography>
        <Typography variant="h4" sx={{ mb: 2 }}>
          Упс! Страница не найдена
        </Typography>
        <Typography variant="body1" sx={{ mb: 4, color: 'text.secondary' }}>
          Похоже, вы забрели не туда. Но не волнуйтесь, главная страница всегда
          на месте.
        </Typography>
        <Button variant="contained" size="large" onClick={() => navigate('/')}>
          Вернуться на главную
        </Button>
      </Box>
    </Container>
  );
};
