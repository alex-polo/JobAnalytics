import { authApi } from './axiosInstance';
import { API_ENDPOINTS } from './endpoints';
import { tokenStore } from './tokenStore';

export const initAuth = async () => {
  try {
    const { data } = await authApi.post(
      `${API_ENDPOINTS.AUTH.REFRESH_TOKEN}`,
      {},
      { withCredentials: true }
    );

    tokenStore.setAccessToken(data.access_token);
  } catch (error) {
    tokenStore.setInitialized();
  }
};
