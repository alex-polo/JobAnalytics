import * as z from 'zod';

export const loginSchema = z.object({
  username: z.email('Введите корректный email'),

  password: z
    .string()
    .min(6, { error: 'Пароль должен быть не менее 6 символов' }),
});

export type LoginFormValues = z.infer<typeof loginSchema>;
