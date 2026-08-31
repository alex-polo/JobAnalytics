import { type AlertColor } from '@mui/material';

type NotifyEvent = {
  message: string;
  severity: AlertColor;
};

type Listener = (event: NotifyEvent) => void;
const listeners = new Set<Listener>();

export const notify = {
  subscribe: (callback: Listener) => {
    listeners.add(callback);
    return () => {
      listeners.delete(callback);
    };
  },
  show: (message: string, severity: AlertColor = 'info') => {
    listeners.forEach(l => l({ message, severity }));
  },
  error: (msg: string) => notify.show(msg, 'error'),
  success: (msg: string) => notify.show(msg, 'success'),
};
