import { API_ENDPOINTS, apiClient, tokenStore } from '@/shared/api';
import { ROUTE_PATHS } from '@/shared/config';
import { notify } from '@/shared/lib';
import { useMutation } from '@tanstack/react-query';
import { isAxiosError } from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import type { LoginFormValues } from '../model/types';

export const useLogin = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || ROUTE_PATHS.DASHBOARD;

  return useMutation({
    mutationFn: async (data: LoginFormValues) => {
      const params = new URLSearchParams();
      params.append('username', data.username);
      params.append('password', data.password);

      const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return response.data;
    },
    onSuccess: data => {
      tokenStore.setAccessToken(data.access_token);

      navigate(from, { replace: true });
    },
    onError: (error: unknown) => {
      if (!isAxiosError(error)) {
        notify.error('Произошла ошибка при входе');
        console.error('[Login Error]:', error);
        return;
      }

      const status = error.response?.status;
      const detail = error.response?.data?.detail;

      let userMessage = 'Произошла ошибка при входе';

      if (status === 401) {
        userMessage = 'Неверный логин или пароль';
      } else if (status === 400) {
        userMessage =
          typeof detail === 'string' ? detail : 'Некорректный запрос';
      }

      notify.error(userMessage);
      console.error(`[Login Error] ${status}:`, error.response?.data);
    },
  });
};
