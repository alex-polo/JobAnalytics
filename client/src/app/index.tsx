import { ErrorBoundary, router } from '@/app/providers';
import { SITE_CONFIG, theme } from '@/shared/config';
import { GlobalLoader, GlobalSnackbar } from '@/shared/ui';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Suspense, useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';

import { queryClient } from '@/shared/api';
import { QueryClientProvider } from '@tanstack/react-query';

import './styles/index.css';

export const App = () => {
  useEffect(() => {
    document.title = SITE_CONFIG.NAME;
  }, []);

  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Suspense fallback={<GlobalLoader />}>
            <RouterProvider router={router} />
            <GlobalSnackbar />
          </Suspense>
        </ThemeProvider>
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </ErrorBoundary>
  );
};
