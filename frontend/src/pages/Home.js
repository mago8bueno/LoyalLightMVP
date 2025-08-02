/**
 * Home Page Component
 * 
 * Main landing page with API integration and accessibility features.
 * Includes error handling and loading states with smooth animations.
 */

import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import { apiService } from '../services/apiService';
import './Home.css';

const Home = () => {
  const [apiStatus, setApiStatus] = useState('loading');
  const [error, setError] = useState(null);

  useEffect(() => {
    const initializeApi = async () => {
      try {
        setApiStatus('loading');
        await apiService.checkHealth();
        setApiStatus('success');
        setError(null);
      } catch (err) {
        console.error('API connection failed:', err);
        setApiStatus('error');
        setError(err.message || 'Failed to connect to API');
      }
    };

    initializeApi();
  }, []);

  return (
    <main 
      className="home-page"
      role="main"
      aria-label="LoyalLight MVP Home Page"
    >
      <Header />
      
      {/* API Status Indicator */}
      <div 
        className="api-status-container animate-fade-in-delayed"
        role="status"
        aria-live="polite"
      >
        <div className={`api-status api-status--${apiStatus}`}>
          {apiStatus === 'loading' && (
            <>
              <div className="status-spinner" aria-hidden="true"></div>
              <span>Connecting to API...</span>
            </>
          )}
          
          {apiStatus === 'success' && (
            <>
              <div className="status-icon status-icon--success" aria-hidden="true">✓</div>
              <span>API Connected Successfully</span>
            </>
          )}
          
          {apiStatus === 'error' && (
            <>
              <div className="status-icon status-icon--error" aria-hidden="true">⚠</div>
              <span>API Connection Failed</span>
              {error && (
                <div className="error-details" role="alert">
                  {error}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  );
};

export default Home;