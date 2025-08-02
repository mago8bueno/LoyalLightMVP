import React from 'react';

const Logo = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-32 h-32',
    lg: 'w-48 h-48',
  };

  return (
    <img
      src="/logo.png"
      alt="LoyalLight logo"
      className={`${sizeClasses[size]} object-contain ${className}`}
      onError={(e) => {
        // Fallback if logo doesn't load
        e.target.style.display = 'none';
        e.target.nextSibling.style.display = 'flex';
      }}
    />
  );
};

export default Logo;

