import React from 'react';
import { Eye, EyeOff } from 'lucide-react';

export type InputVariant = 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' | 'date' | 'datetime-local' | 'time';

export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement>, 'size'> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: InputVariant;
  textarea?: boolean;
  rows?: number;
  icon?: React.ReactNode;
  fullWidth?: boolean;
}

const Input = React.forwardRef<HTMLInputElement | HTMLTextAreaElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      variant = 'text',
      textarea = false,
      rows = 4,
      icon,
      fullWidth = true,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = React.useState(false);

    const baseStyles = 'block w-full px-3 py-2 border rounded-lg shadow-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-0 disabled:bg-gray-100 disabled:cursor-not-allowed';

    const normalStyles = 'border-gray-300 focus:border-primary-500 focus:ring-primary-500';
    const errorStyles = 'border-red-500 focus:border-red-500 focus:ring-red-500';

    const inputStyles = `${baseStyles} ${error ? errorStyles : normalStyles}`;
    const widthStyle = fullWidth ? 'w-full' : '';

    const inputType = variant === 'password' && showPassword ? 'text' : variant;

    const commonProps = {
      className: inputStyles,
      disabled,
      'aria-invalid': !!error,
      'aria-describedby': error ? `${props.id}-error` : helperText ? `${props.id}-helper` : undefined,
      ...props,
    };

    return (
      <div className={widthStyle}>
        {label && (
          <label htmlFor={props.id} className="block text-sm font-medium text-gray-700 mb-1">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}

        <div className="relative">
          {icon && !textarea && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
              {icon}
            </div>
          )}

          {textarea ? (
            <textarea
              ref={ref as React.ForwardedRef<HTMLTextAreaElement>}
              rows={rows}
              {...(commonProps as React.TextareaHTMLAttributes<HTMLTextAreaElement>)}
            />
          ) : (
            <input
              ref={ref as React.ForwardedRef<HTMLInputElement>}
              type={inputType}
              className={`${inputStyles} ${icon ? 'pl-10' : ''} ${variant === 'password' ? 'pr-10' : ''}`}
              {...(commonProps as React.InputHTMLAttributes<HTMLInputElement>)}
            />
          )}

          {variant === 'password' && !textarea && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              tabIndex={-1}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          )}
        </div>

        {error && (
          <p id={`${props.id}-error`} className="mt-1 text-sm text-red-600">
            {error}
          </p>
        )}

        {helperText && !error && (
          <p id={`${props.id}-helper`} className="mt-1 text-sm text-gray-500">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
