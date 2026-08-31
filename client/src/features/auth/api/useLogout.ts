import { $api, API_ENDPOINTS, queryClient, tokenStore } from '@/shared/api';
import { ROUTE_PATHS } from '@/shared/config';
import { notify } from '@/shared/lib';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

export const useLogout = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: async () => {
      return await $api.post(API_ENDPOINTS.AUTH.LOGOUT);
    },
    onSettled: () => {
      tokenStore.removeAccessToken();

      queryClient.clear();

      navigate(ROUTE_PATHS.LOGIN, { replace: true });

      notify.success('Вы вышли из системы');
    },
  });
};
