import SearchIcon from '@mui/icons-material/Search';
import {
  Button,
  FormControl,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
} from '@mui/material';
import { useResumeMatchFilters } from '../model';
import type { MatchFilters } from '../model/use-match-filters';

export const ResumeMatchFiltersForm = () => {
  const { filters, setFilters, resetFilters } = useResumeMatchFilters();

  return (
    <Stack spacing={2}>
      <TextField
        size="small"
        label="Поиск"
        placeholder="Кандидат или вакансия"
        value={filters.search}
        onChange={e => setFilters({ search: e.target.value })}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />

      <FormControl size="small" fullWidth>
        <InputLabel>Дата</InputLabel>
        <Select
          label="Период"
          value={filters.date}
          onChange={e =>
            setFilters({ date: e.target.value as MatchFilters['date'] })
          }
        >
          <MenuItem value="1d">Сегодня</MenuItem>
          <MenuItem value="2d">2 дня</MenuItem>
          <MenuItem value="3d">3 дня</MenuItem>
          <MenuItem value="7d">7 дней</MenuItem>
          <MenuItem value="30d">30 дней</MenuItem>
          <MenuItem value="all">За всё время</MenuItem>
        </Select>
      </FormControl>
      <FormControl size="small" fullWidth>
        <InputLabel>Уровень</InputLabel>
        <Select
          label="Уровень"
          value={filters.matchLevel}
          onChange={e =>
            setFilters({
              matchLevel: e.target.value as MatchFilters['matchLevel'],
            })
          }
        >
          <MenuItem value="any">Все</MenuItem>
          <MenuItem value="perfect">Идеально</MenuItem>
          <MenuItem value="strong">Сильное</MenuItem>
          <MenuItem value="moderate">Среднее</MenuItem>
          <MenuItem value="weak">Слабое</MenuItem>
          <MenuItem value="mismatch">Не подходит</MenuItem>
        </Select>
      </FormControl>

      <ToggleButtonGroup
        exclusive
        value={filters.location}
        onChange={(_, value) => {
          if (value !== null) setFilters({ location: value });
        }}
        size="small"
        fullWidth
      >
        <ToggleButton value="any">Все</ToggleButton>
        <ToggleButton value="remote">Удалённо</ToggleButton>
        <ToggleButton value="office">Офис</ToggleButton>
        <ToggleButton value="gibrid">Гибрид</ToggleButton>
      </ToggleButtonGroup>

      <Button
        size="small"
        variant="outlined"
        color="inherit"
        onClick={resetFilters}
      >
        Сбросить
      </Button>
    </Stack>
  );
};
