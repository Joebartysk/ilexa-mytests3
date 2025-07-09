// src/api/auth.service.ts

import axios, { AxiosInstance } from 'axios';

import { UserData } from './api.types';

class AuthService {
	private axios: AxiosInstance;
	private baseUrl: string;

	constructor() {
		this.baseUrl = process.env.NODE_ENV === 'development'
					 ? 'http://localhost:8000'
					 : 'https://tu-URL-de-producción.com';
		this.axios = axios.create({
			baseURL: this.baseUrl,
			headers: {
				'Content-Type': 'application/json',
			},
		});

		// Configurar interceptor para errores
		this.axios.interceptors.response.use(
			(response) => response.data,
			(error) => {
				throw new Error(error.message || 'Error de servidor');
			}
		);
	}

	public async register(userData: UserData): Promise<void> {
		const response = await this.axios.post('/v1/auth/register', userData);
		return response.data;
	}

	public async login(email: string, password: string): Promise<string> {
		const response = await this.axios.post('/v1/auth/login', { email, password });
		// Asumiendo que el token de acceso se envía en los headers
		return response.headers['Authorization'];
	}
}

export default AuthService;
