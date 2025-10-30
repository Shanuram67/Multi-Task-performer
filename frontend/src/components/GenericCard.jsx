// GenericCard.jsx
import React from 'react';

const GenericCard = ({ children, title, icon: Icon }) => (
  <div className="generic-card">
    {/* Card Header Section */}
    {title && (
      <header className="card-header">
        {Icon && <Icon className="card-icon" />}
        <h2 className="card-title">{title}</h2>
      </header>
    )}
    
    {/* Main Content Area */}
    {children}
  </div>
);

export default GenericCard;