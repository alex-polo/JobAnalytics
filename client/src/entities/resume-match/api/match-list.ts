import { API_ENDPOINTS, apiClient } from '@/shared/api';

import type { ResumeMatch } from '../model';

export interface ResumeMatchFilters {
  q?: string;
  matchLevel?: string;
  location?: string;
  date?: string;
}

export async function fetchResumeMatchList(
  filters: ResumeMatchFilters = {},
  signal?: AbortSignal
): Promise<ResumeMatch[]> {
  const { data } = await apiClient.get<ResumeMatch[]>(
    API_ENDPOINTS.MATCHES.LIST,
    {
      params: {
        q: filters.q || undefined,
        match_level:
          filters.matchLevel && filters.matchLevel !== 'any'
            ? filters.matchLevel
            : undefined,
        location:
          filters.location && filters.location !== 'any'
            ? filters.location
            : undefined,
        date: filters.date && filters.date !== 'all' ? filters.date : undefined,
      },

      signal,
    }
  );

  return data;
}
