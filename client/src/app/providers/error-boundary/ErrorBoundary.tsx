import { Box, Button, Typography } from '@mui/material';

import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}
interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false };

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ p: 4, textAlign: 'center', mt: 10 }}>
          <Typography variant="h4" gutterBottom>
            Что-то пошло не так
          </Typography>
          <Typography sx={{ mb: 3 }}>
            Приложение столкнулось с критической ошибкой.
          </Typography>
          <Button variant="contained" onClick={() => window.location.reload()}>
            Обновить страницу
          </Button>
        </Box>
      );
    }
    return this.props.children;
  }
}
