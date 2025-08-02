/**
 * Header Component
 * 
 * Main application header with subtle animations and accessibility features.
 * Includes fade-in animation and proper ARIA labeling.
 */

import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header 
      className="app-header animate-fade-in" 
      role="banner"
      aria-label="LoyalLight MVP Application Header"
    >
      <div className="header-content">
        <a
          className="app-link"
          href="https://emergent.sh"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Visit Emergent website (opens in new tab)"
          tabIndex="0"
        >
          <img 
            src="https://avatars.githubusercontent.com/in/1201222?s=120&u=2686cf91179bbafbc7a71bfbc43004cf9ae1acea&v=4"
            alt="Emergent logo"
            className="header-logo animate-scale-hover"
            loading="lazy"
            width="120"
            height="120"
          />
        </a>
        <p className="header-text animate-slide-up">
          Building something incredible ~!
        </p>
      </div>
    </header>
  );
};

export default Header;