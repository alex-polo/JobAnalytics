import { useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';

export type WorkLocation = 'any' | 'remote' | 'office' | 'gibrid';
export type MatchLevel =
  | 'perfect'
  | 'strong'
  | 'moderate'
  | 'weak'
  | 'mismatch';

export interface MatchFilters {
  search: string;
  date: 'all' | '1d' | '2d' | '3d' | '7d' | '30d';
  location: WorkLocation;
  matchLevel: MatchLevel | 'any';
  page: number;
}

const DEFAULT_VALUES_FILTERS: MatchFilters = {
  search: '',
  date: 'all',
  location: 'any',
  matchLevel: 'any',
  page: 1,
};

export function useResumeMatchFilters() {
  const [params, setParams] = useSearchParams();

  const filters = useMemo<MatchFilters>(
    () => ({
      search: params.get('q') ?? DEFAULT_VALUES_FILTERS.search,
      date:
        (params.get('date') as MatchFilters['date']) ??
        DEFAULT_VALUES_FILTERS.date,
      location:
        (params.get('location') as WorkLocation) ??
        DEFAULT_VALUES_FILTERS.location,
      matchLevel:
        (params.get('match_level') as MatchFilters['matchLevel']) ??
        DEFAULT_VALUES_FILTERS.matchLevel,
      page: Number(params.get('page') ?? DEFAULT_VALUES_FILTERS.page),
    }),
    [params]
  );

  const setFilters = useCallback(
    (next: Partial<MatchFilters>) => {
      setParams(
        prev => {
          const p = new URLSearchParams(prev);

          const isPageChange = Object.keys(next).length === 1 && 'page' in next;
          if (!isPageChange) p.delete('page');

          if ('search' in next) {
            if (next.search) p.set('q', next.search);
            else p.delete('q');
          }
          if ('date' in next) {
            if (next.date && next.date !== DEFAULT_VALUES_FILTERS.date)
              p.set('date', next.date);
            else p.delete('date');
          }
          if ('location' in next) {
            if (
              next.location &&
              next.location !== DEFAULT_VALUES_FILTERS.location
            )
              p.set('location', next.location);
            else p.delete('location');
          }
          if ('matchLevel' in next) {
            if (
              next.matchLevel &&
              next.matchLevel !== DEFAULT_VALUES_FILTERS.matchLevel
            )
              p.set('match_level', next.matchLevel);
            else p.delete('match_level');
          }

          return p;
        },
        { replace: true }
      );
    },
    [setParams]
  );

  const resetFilters = useCallback(() => {
    setParams(new URLSearchParams(), { replace: true });
  }, [setParams]);

  return { filters, setFilters, resetFilters };
}
