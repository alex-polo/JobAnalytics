import { ResumeMatchFiltersDrawer } from '@/features/resume-match-filters';
import { ResumeMatchTable } from '@/widgets/resume-match-table';
import { Stack } from '@mui/material';

export const ResumeMatchingPage = () => (
  <Stack spacing={1} sx={{ height: '100%' }}>
    <Stack direction="row" justifyContent="flex-end">
      <ResumeMatchFiltersDrawer />
    </Stack>
    <ResumeMatchTable />
  </Stack>
);
