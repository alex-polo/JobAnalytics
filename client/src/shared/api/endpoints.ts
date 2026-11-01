export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/v1/auth/login',
    REFRESH_TOKEN: '/v1/auth/refresh',
    LOGOUT: '/v1/auth/logout',
  },
  USER: {
    ME: '/v1/users/me',
    UPDATE: (id: string) => `v1/users/${id}`,
  },
  DASHBOARD: {
    STATS: 'v1/dashboard/stats',
  },
  MATCHES: {
    LIST: 'v1/resume-matches',
    DETAILS: (id: string) => `v1/resume-matches/${id}`,
  },
} as const;
