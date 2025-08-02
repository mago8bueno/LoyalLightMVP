/**
 * API Service
 * 
 * Centralized service for all API communications with the backend.
 * Includes error handling, request/response logging, and proper configuration.
 */

import axios from 'axios';

/**
 * Get backend URL from environment variables
 * Ensures proper configuration and fallback handling
 */
const getBackendUrl = () => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  
  if (!backendUrl) {
    console.warn('REACT_APP_BACKEND_URL not configured, using default');
    return 'http://localhost:8001';
  }
  
  return backendUrl;
};

/**
 * Configure axios instance with proper defaults
 */
const apiClient = axios.create({
  baseURL: `${getBackendUrl()}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor for logging and debugging
 */
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

/**
 * Response interceptor for logging and error handling
 */
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    const errorMessage = error.response?.data?.detail || error.message || 'Unknown error';
    const statusCode = error.response?.status || 'No status';
    
    console.error(`❌ API Error: ${statusCode} - ${errorMessage}`);
    
    // Enhance error object with more context
    const enhancedError = new Error(errorMessage);
    enhancedError.statusCode = statusCode;
    enhancedError.originalError = error;
    
    return Promise.reject(enhancedError);
  }
);

/**
 * API Service class with all backend operations
 */
class ApiService {
  /**
   * Health check endpoint
   * Tests basic connectivity with the backend
   * 
   * @returns {Promise<Object>} API response with hello message
   * @throws {Error} If API is unreachable or returns error
   */
  async checkHealth() {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }

  /**
   * Create a new status check
   * 
   * @param {string} clientName - Name of the client
   * @returns {Promise<Object>} Created status check object
   * @throws {Error} If creation fails
   */
  async createStatusCheck(clientName) {
    if (!clientName || typeof clientName !== 'string' || clientName.trim().length === 0) {
      throw new Error('Client name is required and must be a non-empty string');
    }

    try {
      const response = await apiClient.post('/status', {
        client_name: clientName.trim(),
      });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to create status check: ${error.message}`);
    }
  }

  /**
   * Get all status checks
   * 
   * @returns {Promise<Array>} Array of status check objects
   * @throws {Error} If retrieval fails
   */
  async getStatusChecks() {
    try {
      const response = await apiClient.get('/status');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to retrieve status checks: ${error.message}`);
    }
  }

  /**
   * Get current backend configuration info
   * 
   * @returns {Object} Configuration information
   */
  getConfig() {
    return {
      baseURL: apiClient.defaults.baseURL,
      timeout: apiClient.defaults.timeout,
      backendUrl: getBackendUrl(),
    };
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export class for testing purposes
export { ApiService };

// Export default for backward compatibility
export default apiService;