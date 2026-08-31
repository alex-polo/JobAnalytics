export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/v1/auth/login',
    REFRESH_TOKEN: '/v1/auth/refresh',
    LOGOUT: '/v1/auth/logout',
  },
  USER: {
    ME: '/v1/users/me',
    UPDATE: (id: string) => `/users/${id}`,
  },
  DASHBOARD: {
    STATS: '/dashboard/stats',
  },
} as const;
