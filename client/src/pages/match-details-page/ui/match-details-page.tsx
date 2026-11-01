import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CancelIcon from '@mui/icons-material/Cancel';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Stack,
  Typography,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';

import type { LocationItems, ResumeMatchLevel } from '@/entities/resume-match';
import { fetchResumeMatchDetails } from '@/entities/resume-match';
import { ROUTE_PATHS } from '@/shared/config';

const LEVEL_LABELS: Record<ResumeMatchLevel, string> = {
  perfect: 'Идеально',
  strong: 'Сильное',
  moderate: 'Среднее',
  weak: 'Слабое',
  mismatch: 'Не подходит',
};

const LEVEL_COLORS: Record<
  ResumeMatchLevel,
  'success' | 'info' | 'warning' | 'error' | 'default'
> = {
  perfect: 'success',
  strong: 'success',
  moderate: 'info',
  weak: 'warning',
  mismatch: 'error',
};

const LOCATION_LABELS: Record<LocationItems, string> = {
  remote: 'Удалённо',
  office: 'Офис',
  gibrid: 'Гибрид',
};

const BoolIcon = ({ value }: { value: boolean | null }) => {
  if (value === null)
    return <HelpOutlineIcon color="disabled" fontSize="small" />;
  return value ? (
    <CheckCircleIcon color="success" fontSize="small" />
  ) : (
    <CancelIcon color="error" fontSize="small" />
  );
};

const SkillList = ({
  title,
  items,
  color,
}: {
  title: string;
  items: string[];
  color: 'success' | 'error' | 'default';
}) => (
  <Box>
    <Typography variant="subtitle2" gutterBottom>
      {title} ({items.length})
    </Typography>
    {items.length === 0 ? (
      <Typography variant="body2" color="text.secondary">
        —
      </Typography>
    ) : (
      <Stack direction="row" flexWrap="wrap" gap={1}>
        {items.map(skill => (
          <Chip
            key={skill}
            label={skill}
            size="small"
            color={color}
            variant="outlined"
          />
        ))}
      </Stack>
    )}
  </Box>
);

export const MatchDetailsPage = () => {
  const { matchId } = useParams<{ matchId: string }>();
  const navigate = useNavigate();

  const { data, isPending, isError } = useQuery({
    queryKey: ['match-details', matchId],
    queryFn: ({ signal }) => fetchResumeMatchDetails(Number(matchId), signal),
    enabled: Boolean(matchId),
  });

  const handleBack = () => navigate(ROUTE_PATHS.RESUME_MATCHING);

  if (isPending) return <CircularProgress />;
  if (isError || !data) {
    return (
      <Box>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
          sx={{ mb: 2 }}
        >
          Назад
        </Button>
        <Alert severity="error">Не удалось загрузить детали матча</Alert>
      </Box>
    );
  }

  return (
    <Stack spacing={3}>
      <Box>
        <Button startIcon={<ArrowBackIcon />} onClick={handleBack}>
          Назад
        </Button>
      </Box>

      <Stack direction="row" alignItems="center" spacing={2} flexWrap="wrap">
        <Typography variant="h4">{data.matchScore}%</Typography>
        <Chip
          label={LEVEL_LABELS[data.matchLevel] ?? data.matchLevel}
          color={LEVEL_COLORS[data.matchLevel] ?? 'default'}
        />
        <Button
          size="small"
          variant="outlined"
          endIcon={<OpenInNewIcon fontSize="small" />}
          href={data.url}
          target="_blank"
          rel="noopener noreferrer"
          sx={{ ml: 'auto' }}
        >
          Открыть вакансию
        </Button>
      </Stack>

      <Box>
        <Typography variant="h6" gutterBottom>
          Резюме оценки
        </Typography>
        <Typography variant="body1">{data.summary}</Typography>
      </Box>

      <Divider />

      <Stack spacing={2}>
        <Typography variant="h6">Навыки</Typography>
        <SkillList
          title="Совпадающие"
          items={data.matchingSkills}
          color="success"
        />
        <SkillList
          title="Не хватает"
          items={data.missingSkills}
          color="error"
        />
        <SkillList title="Лишние" items={data.extraSkills} color="default" />
      </Stack>

      <Divider />

      <Box>
        <Typography variant="h6" gutterBottom>
          Условия
        </Typography>
        <Stack spacing={1}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <BoolIcon value={data.experienceMatch} />
            <Typography variant="body2">Опыт соответствует</Typography>
          </Stack>
          <Stack direction="row" alignItems="center" spacing={1}>
            <BoolIcon value={data.levelMatch} />
            <Typography variant="body2">Уровень соответствует</Typography>
          </Stack>
          <Stack direction="row" alignItems="center" spacing={1}>
            <BoolIcon value={data.locationMatch} />
            <Typography variant="body2">
              Локация соответствует (
              {LOCATION_LABELS[data.location] ?? data.location})
            </Typography>
          </Stack>
          <Stack direction="row" alignItems="center" spacing={1}>
            <BoolIcon value={data.salaryMatch} />
            <Typography variant="body2">
              Зарплата в рамках {data.salaryMatch === null && '(не указана)'}
            </Typography>
          </Stack>
        </Stack>
      </Box>

      <Divider />

      <Stack spacing={2}>
        <Typography variant="h6">Сильные стороны</Typography>
        {data.strengths.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            —
          </Typography>
        ) : (
          <Box component="ul" sx={{ m: 0, pl: 3 }}>
            {data.strengths.map((s, i) => (
              <li key={i}>
                <Typography variant="body2">{s}</Typography>
              </li>
            ))}
          </Box>
        )}

        <Typography variant="h6">Пробелы</Typography>
        {data.gaps.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            —
          </Typography>
        ) : (
          <Box component="ul" sx={{ m: 0, pl: 3 }}>
            {data.gaps.map((g, i) => (
              <li key={i}>
                <Typography variant="body2">{g}</Typography>
              </li>
            ))}
          </Box>
        )}
      </Stack>

      <Divider />

      <Box>
        <Typography variant="h6" gutterBottom>
          ATS рекомендация
        </Typography>
        <Typography variant="body1">{data.recommendation}</Typography>
      </Box>

      <Divider />
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle2">Анализ выполнен</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Stack spacing={0.5}>
            <Typography variant="body2">
              Промпт: {data.promptName ?? '—'} (v{data.promptVersion ?? '—'},{' '}
              {data.promptLocale ?? '—'})
            </Typography>
            <Typography variant="body2">
              Модель: {data.modelName ?? '—'}
            </Typography>
            <Typography variant="body2">
              Причина завершения: {data.finishReason ?? '—'}
            </Typography>
            <Typography variant="body2">
              Токены: вход {data.inputTokens ?? '—'}, выход{' '}
              {data.outputTokens ?? '—'}, всего {data.totalTokens ?? '—'}
            </Typography>
            <Typography variant="body2">
              Время: {data.latencyMs != null ? `${data.latencyMs} мс` : '—'}
            </Typography>
            <Typography variant="body2">
              Ключевое слово: {data.keyword}
            </Typography>
          </Stack>
        </AccordionDetails>
      </Accordion>
    </Stack>
  );
};
