// authService.ts - Authentication API Service
//
// API calls for authentication endpoints.

import api from './api';

/**
 * Auth Service
 *
 * Methods:
 * - login(email, password) - POST /auth/login
 * - register(data) - POST /auth/register
 * - refreshToken() - POST /auth/refresh
 * - forgotPassword(email) - POST /auth/forgot-password
 * - resetPassword(token, password) - POST /auth/reset-password
 */

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  password: string;
  confirm_password: string;
  role: 'student' | 'teacher' | 'parent' | 'principal';
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user_id: string;
  role: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: string;
  avatar_url?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface PasswordResetRequest {
  email: string;
}

export interface PasswordResetConfirm {
  token: string;
  new_password: string;
  confirm_password: string;
}

export interface PasswordChangeRequest {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

class AuthService {
  /**
   * Login with email and password
   */
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/login', credentials);

    // Store tokens and user info
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('refresh_token', response.data.refresh_token);
    localStorage.setItem('user_id', response.data.user_id);
    localStorage.setItem('user_role', response.data.role);

    return response.data;
  }

  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  }

  /**
   * Logout - clear local storage
   */
  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      // Always clear local storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_role');
      localStorage.removeItem('user');
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<TokenResponse> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });

    // Update tokens
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('refresh_token', response.data.refresh_token);

    return response.data;
  }

  /**
   * Request password reset
   */
  async forgotPassword(email: string): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>('/auth/forgot-password', { email });
    return response.data;
  }

  /**
   * Reset password with token
   */
  async resetPassword(data: PasswordResetConfirm): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>('/auth/reset-password', data);
    return response.data;
  }

  /**
   * Change password (authenticated)
   */
  async changePassword(data: PasswordChangeRequest): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>('/auth/change-password', data);
    return response.data;
  }

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me');
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  /**
   * Get stored access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Get stored user role
   */
  getUserRole(): string | null {
    return localStorage.getItem('user_role');
  }

  /**
   * Get stored user ID
   */
  getUserId(): string | null {
    return localStorage.getItem('user_id');
  }
}

export default new AuthService();
