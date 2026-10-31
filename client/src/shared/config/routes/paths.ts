export const ROUTE_PATHS = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/workspace',
  SETTINGS: '/workspace/settings',
  PROFILE: '/workspace/profile',
  RESUMES: '/workspace/resumes',
  RESUME_MATCHING: '/workspace/resume-matching',
  MATCH_DETAILS: (id: string) => `/workspace/resume-matching/${id}`,
} as const;
