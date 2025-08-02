/**
 * Application Constants
 * 
 * Centralized constants for the LoyalLight MVP frontend application.
 * Includes configuration values, UI constants, and application metadata.
 */

/**
 * Application metadata
 */
export const APP_INFO = {
  name: 'LoyalLight MVP',
  version: '1.0.0',
  description: 'A FastAPI + React MVP application with modern architecture',
  author: 'LoyalLight Team',
};

/**
 * API configuration constants
 */
export const API_CONFIG = {
  timeout: 10000, // 10 seconds
  retryAttempts: 3,
  retryDelay: 1000, // 1 second
};

/**
 * UI animation durations (in milliseconds)
 */
export const ANIMATION_DURATIONS = {
  fast: 200,
  normal: 300,
  slow: 500,
  delayed: 1000,
};

/**
 * Breakpoints for responsive design
 */
export const BREAKPOINTS = {
  mobile: '768px',
  tablet: '1024px',
  desktop: '1200px',
};

/**
 * Status check related constants
 */
export const STATUS_CHECK = {
  maxClientNameLength: 255,
  minClientNameLength: 1,
  maxResults: 1000,
};

/**
 * Accessibility constants
 */
export const A11Y = {
  focusOutlineWidth: '2px',
  focusOutlineOffset: '4px',
  minContrastRatio: 4.5, // WCAG AA standard
};

/**
 * Color palette for consistent theming
 */
export const COLORS = {
  primary: '#61dafb',
  secondary: '#20232a',
  background: '#0f0f10',
  backgroundSecondary: '#1a1a1c',
  success: '#22c55e',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  text: {
    primary: '#ffffff',
    secondary: 'rgba(255, 255, 255, 0.9)',
    muted: 'rgba(255, 255, 255, 0.6)',
  },
};

/**
 * Z-index layers for consistent layering
 */
export const Z_INDEX = {
  base: 1,
  dropdown: 1000,
  modal: 2000,
  notification: 3000,
  tooltip: 4000,
};

/**
 * External links
 */
export const EXTERNAL_LINKS = {
  emergent: 'https://emergent.sh',
  emergentApp: 'https://app.emergent.sh/?utm_source=emergent-badge',
  github: 'https://github.com',
  documentation: '#', // Placeholder for future documentation
};

/**
 * Default values for forms and inputs
 */
export const DEFAULTS = {
  clientName: '',
  pageSize: 10,
  animationEnabled: true,
};

/**
 * Error messages
 */
export const ERROR_MESSAGES = {
  api: {
    connectionFailed: 'Unable to connect to the server. Please try again.',
    timeout: 'Request timed out. Please check your connection.',
    serverError: 'Server error occurred. Please try again later.',
    notFound: 'Resource not found.',
    badRequest: 'Invalid request. Please check your input.',
  },
  form: {
    required: 'This field is required.',
    tooShort: 'Input is too short.',
    tooLong: 'Input is too long.',
    invalid: 'Invalid input format.',
  },
  general: {
    unknown: 'An unexpected error occurred. Please try again.',
    offline: 'You appear to be offline. Please check your connection.',
  },
};

/**
 * Success messages
 */
export const SUCCESS_MESSAGES = {
  api: {
    connected: 'Successfully connected to API',
    statusCheckCreated: 'Status check created successfully',
    dataLoaded: 'Data loaded successfully',
  },
  general: {
    saved: 'Changes saved successfully',
    updated: 'Updated successfully',
  },
};