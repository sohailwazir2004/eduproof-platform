import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';

import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <div className="p-8">Dashboard - To be implemented</div>
            </ProtectedRoute>
          }
        />

        <Route
          path="/homework"
          element={
            <ProtectedRoute allowedRoles={['student', 'teacher']}>
              <div className="p-8">Homework - To be implemented</div>
            </ProtectedRoute>
          }
        />

        <Route
          path="/submissions"
          element={
            <ProtectedRoute allowedRoles={['student', 'teacher']}>
              <div className="p-8">Submissions - To be implemented</div>
            </ProtectedRoute>
          }
        />

        <Route
          path="/textbooks"
          element={
            <ProtectedRoute allowedRoles={['teacher', 'principal']}>
              <div className="p-8">Textbooks - To be implemented</div>
            </ProtectedRoute>
          }
        />

        <Route
          path="/classes"
          element={
            <ProtectedRoute allowedRoles={['teacher', 'principal']}>
              <div className="p-8">Classes - To be implemented</div>
            </ProtectedRoute>
          }
        />

        <Route
          path="/students"
          element={
            <ProtectedRoute allowedRoles={['teacher', 'principal']}>
              <div className="p-8">Students - To be implemented</div>
            </ProtectedRoute>
          }
        />

        <Route
          path="/analytics"
          element={
            <ProtectedRoute allowedRoles={['teacher', 'parent', 'principal']}>
              <div className="p-8">Analytics - To be implemented</div>
            </ProtectedRoute>
          }
        />

        <Route path="/unauthorized" element={<div className="p-8 text-center">Unauthorized Access</div>} />
        <Route path="*" element={<div className="p-8 text-center">404 - Page Not Found</div>} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
