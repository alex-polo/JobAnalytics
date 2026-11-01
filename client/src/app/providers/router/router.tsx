import { lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';

import { ProtectedRoute } from '@/features';
import { ROUTE_PATHS } from '@/shared/config';

import { AuthLayout } from '@/widgets/auth-layout';
import { BaseLayout } from '@/widgets/base-layout';
import { DashboardLayout } from '@/widgets/dashboard-layout';

const NotFoundPage = lazy(() =>
  import('@/pages/not-found').then(module => ({ default: module.NotFoundPage }))
);

const HomePage = lazy(() =>
  import('@/pages/home').then(module => ({ default: module.HomePage }))
);

const LoginPage = lazy(() =>
  import('@/pages/login').then(module => ({ default: module.LoginPage }))
);

const DashboardPage = lazy(() =>
  import('@/pages/dashboard').then(module => ({
    default: module.DashboardPage,
  }))
);

const SettingsPage = lazy(() =>
  import('@/pages/settings').then(module => ({
    default: module.SettingsPage,
  }))
);

const ProfilePage = lazy(() =>
  import('@/pages/profile').then(module => ({
    default: module.ProfilePage,
  }))
);

const ResumeMatchingPage = lazy(() =>
  import('@/pages/resume-matching').then(module => ({
    default: module.ResumeMatchingPage,
  }))
);

const MatchDetailsPage = lazy(() =>
  import('@/pages/match-details-page').then(module => ({
    default: module.MatchDetailsPage,
  }))
);

const ResumesPage = lazy(() =>
  import('@/pages/resumes').then(module => ({
    default: module.ResumesPage,
  }))
);

export const router = createBrowserRouter([
  // Public pages
  {
    element: <BaseLayout />,
    children: [
      {
        path: '/',
        element: <HomePage />,
        handle: { crumb: () => ({ label: 'Главная', path: ROUTE_PATHS.HOME }) },
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
  // Auth pages
  {
    element: <AuthLayout />,
    children: [
      {
        path: ROUTE_PATHS.LOGIN,
        element: <LoginPage />,
      },
    ],
  },

  // Private pages
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <DashboardLayout />,
        handle: {
          crumb: () => ({ label: 'Главная', path: ROUTE_PATHS.DASHBOARD }),
        },
        children: [
          {
            path: ROUTE_PATHS.DASHBOARD,
            element: <DashboardPage />,
          },
          {
            path: ROUTE_PATHS.RESUMES,
            element: <ResumesPage />,
            handle: {
              crumb: () => ({ label: 'Резюме', path: ROUTE_PATHS.RESUMES }),
            },
          },
          {
            path: ROUTE_PATHS.RESUME_MATCHING,
            element: <ResumeMatchingPage />,
            handle: {
              crumb: () => ({
                label: 'Аналитика резюме',
                path: ROUTE_PATHS.RESUME_MATCHING,
              }),
            },
          },
          {
            path: ROUTE_PATHS.MATCH_DETAILS(':matchId'),
            element: <MatchDetailsPage />,
            handle: {
              crumb: () => ({
                label: 'Аналитика резюме',
                path: ROUTE_PATHS.RESUME_MATCHING,
              }),
            },
          },
          {
            path: ROUTE_PATHS.PROFILE,
            element: <ProfilePage />,
            handle: {
              crumb: () => ({
                label: 'Профиль пользователя',
                path: ROUTE_PATHS.PROFILE,
              }),
            },
          },
          {
            path: ROUTE_PATHS.SETTINGS,
            element: <SettingsPage />,
            handle: {
              crumb: () => ({ label: 'Настройки', path: ROUTE_PATHS.SETTINGS }),
            },
          },
        ],
      },
    ],
  },
]);
