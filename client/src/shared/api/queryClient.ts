import { ROUTE_PATHS } from '@/shared/config';
import { MutationCache, QueryCache, QueryClient } from '@tanstack/react-query';
import { isAxiosError } from 'axios';
import { notify } from '../lib/browser';
import type { SessionData } from './hooks';
import { tokenStore } from './tokenStore';

const handleApiError = (error: unknown) => {
  if (isAxiosError(error)) {
    const status = error.response?.status;
    const message = error.response?.data?.detail || 'Ошибка запроса';

    if (status === 401) {
      if (!window.location.pathname.includes(ROUTE_PATHS.LOGIN)) {
        notify.error('Сессия истекла');
      }
    }
    if (status !== 401) {
      notify.error(message);
    }

    console.error(`[API Error] ${status}:`, error.response?.data);
  } else {
    console.error('[Unknown Error]:', error);
  }
};

export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: handleApiError,
  }),
  mutationCache: new MutationCache({
    onError: handleApiError,
  }),
  defaultOptions: {
    queries: {
      retry: (failureCount, error: any) => {
        if (error?.response?.status === 401) return false;
        return failureCount < 2;
      },
      refetchOnWindowFocus: false,
      staleTime: 1 * 60 * 1000,
    },
  },
});

queryClient.setQueryData(['session'], {
  isAuth: !!tokenStore.getAccessToken(),
  isInitialized: false,
});

tokenStore.subscribe(token => {
  queryClient.setQueryData<SessionData>(['session'], {
    isAuth: !!token,
    isInitialized: true,
  });
});
