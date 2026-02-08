import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import authService, { LoginCredentials, RegisterData, User } from '../services/authService';

export const useAuth = () => {
  const navigate = useNavigate();
  const { user, token, isAuthenticated, setUser, setToken, logout: clearAuth, initialize } = useAuthStore();

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    initialize();
  }, [initialize]);

  const login = async (credentials: LoginCredentials) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await authService.login(credentials);
      setToken(response.access_token);

      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);

      navigate('/dashboard');
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Login failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    setIsLoading(true);
    setError(null);

    try {
      const newUser = await authService.register(data);

      await login({
        email: data.email,
        password: data.password,
      });

      return newUser;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await authService.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      clearAuth();
      setIsLoading(false);
      navigate('/login');
    }
  };

  const refreshUser = async () => {
    if (!isAuthenticated) return;

    setIsLoading(true);
    try {
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
    } catch (err) {
      console.error('Failed to refresh user:', err);
      clearAuth();
      navigate('/login');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    refreshUser,
    clearError: () => setError(null),
  };
};
