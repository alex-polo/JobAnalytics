import type { ResumeMatchLevel } from '@/entities/resume-match';
import { fetchResumeMatchList } from '@/entities/resume-match';
import { useResumeMatchFilters } from '@/features/resume-match-filters';
import { ROUTE_PATHS } from '@/shared/config';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import { Box, Button } from '@mui/material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const LEVEL_LABELS: Record<ResumeMatchLevel, string> = {
  perfect: 'Идеально',
  strong: 'Сильное',
  moderate: 'Среднее',
  weak: 'Слабое',
  mismatch: 'Не подходит',
};

// const LOCATION_LABELS: Record<LocationItems, string> = {
//   remote: 'Удалённо',
//   office: 'Офис',
//   gibrid: 'Гибрид',
// };

const columns: GridColDef[] = [
  {
    field: 'id',
    headerName: 'ID',
    width: 70,
    valueFormatter: (value: number) => `${value}`,
  },
  { field: 'vacancyTitle', headerName: 'Вакансия', flex: 1, minWidth: 240 },
  { field: 'resumeTitle', headerName: 'Резюме', flex: 1, minWidth: 140 },
  { field: 'keyword', headerName: 'Ключ', minWidth: 100 },
  {
    field: 'matchScore',
    headerName: '%',
    width: 70,
    valueFormatter: (value: number) => `${value}%`,
  },
  {
    field: 'matchLevel',
    headerName: 'Уровень',
    width: 100,
    valueFormatter: (value: ResumeMatchLevel) => LEVEL_LABELS[value] ?? value,
  },
  {
    field: 'salary',
    headerName: 'Зарплата',
    width: 100,
  },
  // {
  //   field: 'location',
  //   headerName: 'Формат',
  //   width: 100,
  //   valueFormatter: (value: LocationItems) => LOCATION_LABELS[value] ?? value,
  // },
  {
    field: 'locationMatch',
    headerName: 'Локация',
    width: 80,
    type: 'boolean',
  },
  {
    field: 'actions',
    headerName: '',
    width: 120,
    sortable: false,
    filterable: false,
    disableColumnMenu: true,
    renderCell: params => (
      <Button
        size="small"
        variant="outlined"
        component={Link}
        to={ROUTE_PATHS.MATCH_DETAILS(String(params.row.id))}
      >
        Подробнее
      </Button>
    ),
  },
  {
    field: 'url',
    headerName: '',
    width: 120,
    sortable: false,
    filterable: false,
    disableColumnMenu: true,
    renderCell: params => (
      <Button
        size="small"
        variant="outlined"
        endIcon={<OpenInNewIcon fontSize="small" />}
        href={params.row.url}
        target="_blank"
        rel="noopener noreferrer"
      >
        Перейти
      </Button>
    ),
  },
];

export const ResumeMatchTable = () => {
  const { filters } = useResumeMatchFilters();
  const [paginationModel, setPaginationModel] = useState({
    page: 0,
    pageSize: 10,
  });

  const { data, isPending, isError } = useQuery({
    queryKey: ['resume-match-list', filters],
    queryFn: ({ signal }) =>
      fetchResumeMatchList(
        {
          q: filters.search,
          matchLevel: filters.matchLevel,
          date: filters.date,
          location: filters.location,
        },
        signal
      ),
    refetchInterval: 30_000,
    refetchIntervalInBackground: true,
  });

  if (isPending) return <div>Загрузка…</div>;
  if (isError) return <div>Ошибка загрузки</div>;
  if (!data.length) return <div>Ничего не найдено</div>;

  return (
    <Box
      sx={{
        width: '100%',
        flexGrow: 1,
        minHeight: 0,
        overflow: 'hidden',
      }}
    >
      <DataGrid
        density="compact"
        rows={data ?? []}
        columns={columns}
        getRowId={row => row.id}
        paginationModel={paginationModel}
        onPaginationModelChange={setPaginationModel}
        pageSizeOptions={[10, 15, 25]}
        disableRowSelectionOnClick
        sx={{ border: 0, maxHeight: 'calc(100vh - 280px)' }}
      />
    </Box>
  );
};
