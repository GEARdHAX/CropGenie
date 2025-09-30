import React, { useState, useEffect } from 'react';
import { WiThermometer, WiHumidity, WiRaindrop } from 'react-icons/wi';

function PlantHealthPage() {
  const [healthData, setHealthData] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('Connecting...');

  useEffect(() => {
    // TODO: Replace with your computer's CURRENT local IP address
    const WS_URL = 'ws://172.25.25.112:5000/ws';
    
    const socket = new WebSocket(WS_URL);

    socket.onopen = () => {
      console.log('WebSocket connection established.');
      setConnectionStatus('Live Feed Active');
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setHealthData(message);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed.');
      setConnectionStatus('Disconnected. Check server/network.');
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('Connection Error');
    };

    // Clean up the connection when the component unmounts
    return () => {
      socket.close();
    };
  }, []); // The empty array ensures this effect runs only once

  const status = healthData?.plant_health_status || '...';
  const suggestions = healthData?.improvement_suggestions || [];
  const sensors = {
    moisture: healthData?.live_data?.Soil_Moisture,
    temperature: healthData?.live_data?.Soil_Temperature,
    humidity: healthData?.live_data?.Humidity,
  };

  const getStatusStyle = (currentStatus) => {
    switch (currentStatus) {
      case 'Healthy': return { color: '#2e7d32', icon: '✅' };
      case 'High Stress': return { color: '#d32f2f', icon: '⚠️' };
      default: return { color: '#5f6368', icon: '...' };
    }
  };
  const statusStyle = getStatusStyle(status);

  return (
    <div>
      <div className="card">
        <h3>Live Feed Status</h3>
        <p style={{ fontWeight: 'bold' }}>{connectionStatus}</p>
      </div>

      {!healthData ? (
        <div className="card" style={{ textAlign: 'center', color: '#555' }}>
          <h2>Waiting for data...</h2>
          <p>Attempting to connect to the live sensor feed. Please ensure the Python server is running and the ESP8266 is sending data.</p>
        </div>
      ) : (
        <>
          <div className="card" style={{ textAlign: 'center' }}>
            <h2 style={{ ...statusStyle, fontSize: '2.5rem', margin: '1rem 0' }}>
              {statusStyle.icon} {status}
            </h2>
            <p style={{ fontSize: '1.2rem', color: '#555', marginTop: 0 }}>
              Real-time plant health assessment.
            </p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
            <SensorCard 
              icon={<WiRaindrop size={40} color="#3498db" />} 
              label="Soil Moisture" 
              value={sensors.moisture !== undefined ? `${sensors.moisture.toFixed(1)}%` : '--'} 
            />
            <SensorCard 
              icon={<WiThermometer size={40} color="#e74c3c" />} 
              label="Temperature" 
              value={sensors.temperature !== undefined ? `${sensors.temperature.toFixed(1)}°C` : '--'} 
            />
            <SensorCard 
              icon={<WiHumidity size={40} color="#8e44ad" />} 
              label="Air Humidity" 
              value={sensors.humidity !== undefined ? `${sensors.humidity.toFixed(1)}%` : '--'} 
            />
          </div>
          <div className="card">
            <h2>Improvement Suggestions</h2>
            {suggestions.length > 0 ? (
              <ul style={{ paddingLeft: '20px', margin: 0 }}>
                {suggestions.map((s, i) => <li key={i} style={{ marginBottom: '0.5rem', fontSize: '1.1rem' }}>{s}</li>)}
              </ul>
            ) : (
              <p>✅ No suggestions at this time. The plant is healthy.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

const SensorCard = ({ icon, label, value }) => (
  <div className="card" style={{ textAlign: 'center' }}>
    {icon}
    <h3 style={{ marginTop: '0.5rem', marginBottom: '0.2rem', color: '#555' }}>{label}</h3>
    <p style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#333', margin: 0 }}>{value}</p>
  </div>
);

export default PlantHealthPage;