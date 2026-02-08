import React from 'react';
import { Loader2 } from 'lucide-react';

export interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'primary' | 'white' | 'gray';
  fullScreen?: boolean;
  label?: string;
}

const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  color = 'primary',
  fullScreen = false,
  label,
}) => {
  const sizeStyles = {
    sm: 16,
    md: 24,
    lg: 32,
    xl: 48,
  };

  const colorStyles = {
    primary: 'text-primary-600',
    white: 'text-white',
    gray: 'text-gray-600',
  };

  const spinner = (
    <div className="flex flex-col items-center justify-center gap-2">
      <Loader2
        className={`animate-spin ${colorStyles[color]}`}
        size={sizeStyles[size]}
      />
      {label && (
        <p className={`text-sm font-medium ${colorStyles[color]}`}>
          {label}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white bg-opacity-90">
        {spinner}
      </div>
    );
  }

  return spinner;
};

export default Spinner;
