import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Lock, User as UserIcon, Phone, AlertCircle } from 'lucide-react';
import AuthLayout from '../../components/layout/AuthLayout';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';
import { useAuth } from '../../hooks/useAuth';

const RegisterPage: React.FC = () => {
  const { register, isLoading, error, clearError } = useAuth();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    confirm_password: '',
    role: 'student',
  });

  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
    clearError();
    setValidationErrors((prev) => ({
      ...prev,
      [e.target.name]: '',
    }));
  };

  const validate = (): boolean => {
    const errors: Record<string, string> = {};

    if (!formData.first_name.trim()) errors.first_name = 'First name is required';
    if (!formData.last_name.trim()) errors.last_name = 'Last name is required';
    if (!formData.email.trim()) errors.email = 'Email is required';
    if (!formData.password) errors.password = 'Password is required';
    if (formData.password.length < 8) errors.password = 'Password must be at least 8 characters';
    if (formData.password !== formData.confirm_password) {
      errors.confirm_password = 'Passwords do not match';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    try {
      await register(formData);
    } catch (err) {
      console.error('Registration error:', err);
    }
  };

  return (
    <AuthLayout>
      <div>
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-2">
          Create an Account
        </h2>
        <p className="text-sm text-gray-600 text-center mb-6">
          Sign up to get started with EduProof
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
            <AlertCircle size={18} className="text-red-600 mt-0.5 flex-shrink-0" />
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input
              id="first_name"
              name="first_name"
              type="text"
              label="First Name"
              placeholder="John"
              icon={<UserIcon size={18} />}
              value={formData.first_name}
              onChange={handleChange}
              error={validationErrors.first_name}
              required
              disabled={isLoading}
            />

            <Input
              id="last_name"
              name="last_name"
              type="text"
              label="Last Name"
              placeholder="Doe"
              value={formData.last_name}
              onChange={handleChange}
              error={validationErrors.last_name}
              required
              disabled={isLoading}
            />
          </div>

          <Input
            id="email"
            name="email"
            type="email"
            label="Email Address"
            placeholder="you@example.com"
            variant="email"
            icon={<Mail size={18} />}
            value={formData.email}
            onChange={handleChange}
            error={validationErrors.email}
            required
            disabled={isLoading}
          />

          <Input
            id="phone"
            name="phone"
            type="tel"
            label="Phone Number (Optional)"
            placeholder="+1 (555) 000-0000"
            variant="tel"
            icon={<Phone size={18} />}
            value={formData.phone}
            onChange={handleChange}
            disabled={isLoading}
          />

          <div>
            <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-1">
              I am a <span className="text-red-500">*</span>
            </label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-100"
              required
              disabled={isLoading}
            >
              <option value="student">Student</option>
              <option value="teacher">Teacher</option>
              <option value="parent">Parent</option>
              <option value="principal">Principal</option>
            </select>
          </div>

          <Input
            id="password"
            name="password"
            type="password"
            label="Password"
            placeholder="At least 8 characters"
            variant="password"
            icon={<Lock size={18} />}
            value={formData.password}
            onChange={handleChange}
            error={validationErrors.password}
            helperText="Must be at least 8 characters"
            required
            disabled={isLoading}
          />

          <Input
            id="confirm_password"
            name="confirm_password"
            type="password"
            label="Confirm Password"
            placeholder="Re-enter your password"
            variant="password"
            icon={<Lock size={18} />}
            value={formData.confirm_password}
            onChange={handleChange}
            error={validationErrors.confirm_password}
            required
            disabled={isLoading}
          />

          <Button
            type="submit"
            variant="primary"
            size="lg"
            fullWidth
            loading={isLoading}
          >
            Create Account
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link
              to="/login"
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </AuthLayout>
  );
};

export default RegisterPage;
