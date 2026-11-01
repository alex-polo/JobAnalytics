export type ResumeMatchLevel =
  | 'perfect'
  | 'strong'
  | 'moderate'
  | 'weak'
  | 'mismatch';

export type LocationItems = 'remote' | 'office' | 'gibrid';

export interface ResumeMatch {
  id: number;
  vacancyTitle: string;
  resumeTitle: string;
  matchScore: number;
  matchLevel: ResumeMatchLevel;
  keyword: string;
  salary: string;
  location: LocationItems;
  locationMatch: boolean;
  url: string;
}

export interface ResumeMatchDetails {
  id: number;
  resumeId: number;
  vacancyId: number;

  url: string;
  keyword: string;

  matchScore: number;
  matchLevel: ResumeMatchLevel;

  matchingSkills: string[];
  missingSkills: string[];
  extraSkills: string[];

  experienceMatch: boolean;
  levelMatch: boolean;
  locationMatch: boolean;
  salaryMatch: boolean | null;
  location: LocationItems;

  summary: string;
  strengths: string[];
  gaps: string[];
  recommendation: string;

  promptName: string | null;
  promptVersion: string | null;
  promptLocale: string | null;
  modelName: string | null;
  finishReason: string | null;
  inputTokens: number | null;
  outputTokens: number | null;
  totalTokens: number | null;
  latencyMs: number | null;
}
