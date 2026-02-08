import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '../services/authService';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  logout: () => void;
  initialize: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      setUser: (user) => set({
        user,
        isAuthenticated: !!user
      }),

      setToken: (token) => set({
        token,
        isAuthenticated: !!token
      }),

      logout: () => set({
        user: null,
        token: null,
        isAuthenticated: false
      }),

      initialize: () => {
        const token = localStorage.getItem('access_token');
        const userStr = localStorage.getItem('user');
        const user = userStr ? JSON.parse(userStr) : null;

        if (token && user) {
          set({
            token,
            user,
            isAuthenticated: true
          });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
