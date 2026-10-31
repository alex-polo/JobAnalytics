import { API_ENDPOINTS, apiClient } from '@/shared/api';
import type { ResumeMatchDetails } from '../model';

export async function fetchResumeMatchDetails(
  matchId: number,
  signal?: AbortSignal
): Promise<ResumeMatchDetails> {
  const { data } = await apiClient.get<ResumeMatchDetails>(
    API_ENDPOINTS.MATCHES.DETAILS(String(matchId)),
    { signal }
  );
  return data;
}
