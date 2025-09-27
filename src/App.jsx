import React, { useState } from 'react';
import './App.css';
import DiseaseDetectionPage from './DiseaseDetection';
import GddCalculatorPage from './GddCalculator';
import PlantHealthPage from './PlantHealth';

function App() {
  const [activePage, setActivePage] = useState('health');

  const renderPage = () => {
    switch (activePage) {
      case 'detection':
        return <DiseaseDetectionPage />;
      case 'gdd':
        return <GddCalculatorPage />;
      case 'health':
      default:
        return <PlantHealthPage />;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1><span></span> CropGenie Dashboard</h1>
      </header>
      <nav className="app-nav">
        <button 
          className={activePage === 'health' ? 'active' : ''}
          onClick={() => setActivePage('health')}>
          Plant Health Status
        </button>
        <button 
          className={activePage === 'detection' ? 'active' : ''}
          onClick={() => setActivePage('detection')}>
          Disease Detection
        </button>
        <button 
          className={activePage === 'gdd' ? 'active' : ''}
          onClick={() => setActivePage('gdd')}>
          GDD Calculator
        </button>
      </nav>
      <main className="page-container">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;