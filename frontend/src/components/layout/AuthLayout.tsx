import React from 'react';
import { Link } from 'react-router-dom';

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-12">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex flex-col items-center gap-2">
              <div className="w-16 h-16 bg-primary-600 rounded-xl flex items-center justify-center text-white font-bold text-3xl shadow-lg">
                E
              </div>
              <h1 className="text-3xl font-bold text-gray-900">EduProof</h1>
              <p className="text-sm text-gray-600">AI-Powered Homework Management</p>
            </Link>
          </div>

          <div className="bg-white rounded-lg shadow-md border border-gray-200 p-8">
            {children}
          </div>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              &copy; {new Date().getFullYear()} EduProof. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
