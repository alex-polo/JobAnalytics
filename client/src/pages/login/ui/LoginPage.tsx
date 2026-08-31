import { useLogin } from '@/features/auth';
import { loginSchema, type LoginFormValues } from '@/features/auth/model/types';
import { zodResolver } from '@hookform/resolvers/zod';
import { Box, Button, TextField, Typography } from '@mui/material';
import { useForm } from 'react-hook-form';

export const LoginPage = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    mode: 'onBlur',
  });

  const { mutate, isPending } = useLogin();

  const onSubmit = (data: LoginFormValues) => {
    mutate(data);
  };

  return (
    <>
      <Typography
        variant="h5"
        align="center"
        gutterBottom
        sx={{ fontWeight: 700 }}
      >
        Вход
      </Typography>

      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
        noValidate
        sx={{ mt: 2, width: '100%' }}
      >
        <TextField
          {...register('username')}
          label="Email"
          fullWidth
          margin="normal"
          error={!!errors.username}
          helperText={errors.username?.message}
          disabled={isSubmitting}
        />

        <TextField
          {...register('password')}
          label="Пароль"
          type="password"
          fullWidth
          margin="normal"
          error={!!errors.password}
          helperText={errors.password?.message}
          disabled={isSubmitting}
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          size="large"
          disabled={isSubmitting}
          sx={{ mt: 3, mb: 2, py: 1.5, borderRadius: 2 }}
        >
          {isPending ? 'Вход...' : 'Войти'}
        </Button>
      </Box>
    </>
  );
};
