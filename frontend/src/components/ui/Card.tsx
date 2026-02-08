import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  divider?: boolean;
}

export interface CardBodyProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  divider?: boolean;
}

const Card = ({ children, variant = 'default', padding = 'md', className = '', ...props }: CardProps) => {
  const baseStyles = 'bg-white rounded-lg';

  const variantStyles = {
    default: 'border border-gray-200',
    bordered: 'border-2 border-gray-300',
    elevated: 'shadow-lg',
  };

  const paddingStyles = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  };

  return (
    <div
      className={`${baseStyles} ${variantStyles[variant]} ${paddingStyles[padding]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

const CardHeader = ({ children, divider = false, className = '', ...props }: CardHeaderProps) => {
  return (
    <div
      className={`${divider ? 'pb-4 border-b border-gray-200' : ''} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

const CardBody = ({ children, className = '', ...props }: CardBodyProps) => {
  return (
    <div className={`py-4 ${className}`} {...props}>
      {children}
    </div>
  );
};

const CardFooter = ({ children, divider = false, className = '', ...props }: CardFooterProps) => {
  return (
    <div
      className={`${divider ? 'pt-4 border-t border-gray-200' : ''} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

export default Card;
