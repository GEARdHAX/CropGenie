import React, { useState } from 'react';

function GddCalculatorPage() {
  const [tMax, setTMax] = useState('');
  const [tMin, setTMin] = useState('');
  const [tBase, setTBase] = useState('10'); // Common base temp for many plants
  const [result, setResult] = useState(null);

  const handleCalculate = (e) => {
    e.preventDefault();
    const max = parseFloat(tMax);
    const min = parseFloat(tMin);
    const base = parseFloat(tBase);

    if (isNaN(max) || isNaN(min) || isNaN(base)) {
      alert("Please enter valid numbers.");
      return;
    }

    const avgTemp = (max + min) / 2;
    const gdd = avgTemp > base ? avgTemp - base : 0;
    setResult(gdd.toFixed(2));
  };

  return (
    <div className="card">
      <h2>Growing Degree Day (GDD) Calculator</h2>
      <p>GDD is a measure of heat accumulation used to predict plant development stages.</p>
      
      <form onSubmit={handleCalculate}>
        <div className="form-group">
          <label>Max Temperature (°C)</label>
          <input type="number" value={tMax} onChange={(e) => setTMax(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Min Temperature (°C)</label>
          <input type="number" value={tMin} onChange={(e) => setTMin(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Base Temperature (°C)</label>
          <input type="number" value={tBase} onChange={(e) => setTBase(e.target.value)} required />
        </div>
        <button type="submit" className="btn">Calculate GDD</button>
      </form>

      {result !== null && (
        <div style={{ marginTop: '2rem', textAlign: 'center', backgroundColor: '#e8f5e9', padding: '1rem', borderRadius: '8px' }}>
          <h3>Calculated GDD for the day:</h3>
          <p style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1b5e20', margin: 0 }}>
            {result}
          </p>
        </div>
      )}
    </div>
  );
}

export default GddCalculatorPage;