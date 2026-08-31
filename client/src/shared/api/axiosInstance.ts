import { ROUTE_PATHS } from '@/shared/config';
import axios from 'axios';
import { API_ENDPOINTS } from './endpoints';
import { tokenStore } from './tokenStore';

const BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const $api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authApi = axios.create({ baseURL: import.meta.env.VITE_API_URL });

$api.interceptors.request.use(config => {
  const token = tokenStore.getAccessToken();
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

$api.interceptors.response.use(
  res => res,
  async error => {
    const originalRequest = error.config;
    const isLoginRequest = originalRequest.url?.includes(
      API_ENDPOINTS.AUTH.LOGIN
    );
    if (error.response?.status === 401 && isLoginRequest) {
      return Promise.reject(error);
    }
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const response = await authApi.post(
          API_ENDPOINTS.AUTH.REFRESH_TOKEN,
          {},
          { withCredentials: true }
        );
        const { access_token } = response.data;

        tokenStore.setAccessToken(access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return $api(originalRequest);
      } catch (refreshError) {
        tokenStore.removeAccessToken();
        window.location.href = ROUTE_PATHS.LOGIN;
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);
