import { $api, API_ENDPOINTS, useSession } from '@/shared/api';
import { useQuery } from '@tanstack/react-query';
import type { User } from '../model/types';

export const useMe = () => {
  const { data: session } = useSession();

  return useQuery<User>({
    queryKey: ['user', 'me'],
    queryFn: async () => {
      const { data } = await $api.get(API_ENDPOINTS.USER.ME);
      return data;
    },
    enabled: !!session?.isAuth,
    staleTime: 60 * 1000,
  });
};
