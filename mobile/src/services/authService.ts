// authService.ts - Mobile Auth Service
//
// Authentication API calls with secure storage.

import api from './api';
import * as SecureStore from 'expo-secure-store';

/**
 * Auth Service for React Native
 *
 * Methods:
 * - login(email, password) -> Token & User data
 * - register(data) -> User
 * - refreshToken() -> Token
 * - logout() -> void
 * - getCurrentUser() -> User
 * - isAuthenticated() -> boolean
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
  role: 'student' | 'parent';
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

// Secure storage keys
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const USER_ID_KEY = 'user_id';
const USER_ROLE_KEY = 'user_role';
const USER_KEY = 'user';

class AuthService {
  /**
   * Login with email and password
   */
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/login', credentials);

    // Store tokens and user info in secure storage
    await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, response.data.access_token);
    await SecureStore.setItemAsync(REFRESH_TOKEN_KEY, response.data.refresh_token);
    await SecureStore.setItemAsync(USER_ID_KEY, response.data.user_id);
    await SecureStore.setItemAsync(USER_ROLE_KEY, response.data.role);

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
   * Logout - clear secure storage
   */
  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      // Always clear secure storage
      await SecureStore.deleteItemAsync(ACCESS_TOKEN_KEY);
      await SecureStore.deleteItemAsync(REFRESH_TOKEN_KEY);
      await SecureStore.deleteItemAsync(USER_ID_KEY);
      await SecureStore.deleteItemAsync(USER_ROLE_KEY);
      await SecureStore.deleteItemAsync(USER_KEY);
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<TokenResponse> {
    const refreshToken = await SecureStore.getItemAsync(REFRESH_TOKEN_KEY);
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });

    // Update tokens in secure storage
    await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, response.data.access_token);
    await SecureStore.setItemAsync(REFRESH_TOKEN_KEY, response.data.refresh_token);

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
    await SecureStore.setItemAsync(USER_KEY, JSON.stringify(response.data));
    return response.data;
  }

  /**
   * Check if user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    const token = await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
    return !!token;
  }

  /**
   * Get stored access token
   */
  async getAccessToken(): Promise<string | null> {
    return await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
  }

  /**
   * Get stored user role
   */
  async getUserRole(): Promise<string | null> {
    return await SecureStore.getItemAsync(USER_ROLE_KEY);
  }

  /**
   * Get stored user ID
   */
  async getUserId(): Promise<string | null> {
    return await SecureStore.getItemAsync(USER_ID_KEY);
  }

  /**
   * Get stored user data
   */
  async getStoredUser(): Promise<User | null> {
    const userStr = await SecureStore.getItemAsync(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  }
}

export default new AuthService();
