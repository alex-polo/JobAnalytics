import { useQuery } from '@tanstack/react-query';
import { queryClient } from './queryClient';

export interface SessionData {
  isAuth: boolean;
  isInitialized: boolean;
}

export const useSession = () => {
  return useQuery<SessionData>({
    queryKey: ['session'],
    queryFn: () =>
      queryClient.getQueryData<SessionData>(['session']) ?? {
        isAuth: false,
        isInitialized: false,
      },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnMount: false,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  });
};
