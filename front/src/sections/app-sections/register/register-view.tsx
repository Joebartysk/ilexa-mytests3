// src/sections/app-sections/register/register-view.tsx

import { useState, useCallback } from 'react';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

import { useRouter } from 'src/routes/hooks';

import Auth from 'src/api/auth.service';
import { UserData } from 'src/api/api.types';


export function RegisterView() {
  const router = useRouter();

  // Estados para los campos del formulario
  const [showPassword, setShowPassword] = useState(false);
  const [firstName, setFirstName] = useState(''); // Nombre
  const [lastName, setLastName] = useState('');   // Apellido
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('hello@gmail.com');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');

  const handleRegister = useCallback(() => {

    const dataUsr: UserData = {
      email: email,
      password: password,
      first_name: firstName,
      last_name: lastName,
      phone: phone
    };

		const auth = new Auth();
    auth.register(dataUsr).then(data => {
      console.log('Registro exitoso:', data);
    }).catch(error => {
      console.error('Error en el registro:', error);
    });
  }, [firstName, lastName, username, email, password, phone, router]);

  const renderForm = (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'flex-end',
        flexDirection: 'column',
      }}
    >
      {/* Campo de nombre */}
      <TextField
        fullWidth
        name="firstName"
        label="Nombre"
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
        sx={{ mb: 3 }}
        slotProps={{
          inputLabel: { shrink: true },
        }}
      />

      {/* Campo de apellido */}
      <TextField
        fullWidth
        name="lastName"
        label="Apellido"
        value={lastName}
        onChange={(e) => setLastName(e.target.value)}
        sx={{ mb: 3 }}
        slotProps={{
          inputLabel: { shrink: true },
        }}
      />

      {/* Campo de nombre de usuario */}
      <TextField
        fullWidth
        name="username"
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        sx={{ mb: 3 }}
        slotProps={{
          inputLabel: { shrink: true },
        }}
      />

      {/* Campo de correo electrónico */}
      <TextField
        fullWidth
        name="email"
        label="Email address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        sx={{ mb: 3 }}
        slotProps={{
          inputLabel: { shrink: true },
        }}
      />

      {/* Campo de contraseña */}
      <TextField
        fullWidth
        name="password"
        label="Contraseña"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        sx={{ mb: 3 }}
        slotProps={{
          inputLabel: { shrink: true },
        }}
      />

      {/* Campo de teléfono */}
      <TextField
        fullWidth
        name="phone"
        label="Teléfono"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        sx={{ mb: 3 }}
        slotProps={{
          inputLabel: { shrink: true },
        }}
      />

      {/* Botón de registro */}
      <Button
        variant="contained"
        fullWidth
        onClick={handleRegister}
        sx={{ mt: 2, backgroundColor: '#1976d2', color: 'white' }}
      >
        Crear cuenta
      </Button>
    </Box>
  );

  return renderForm;
}
