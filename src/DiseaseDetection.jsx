import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';

function DiseaseDetectionPage() {
  const [detections, setDetections] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const videoRef = useRef(null);
  const containerRef = useRef(null); // Ref for the container to get display dimensions
  const socketRef = useRef(null);
  const isProcessing = useRef(false);

  useEffect(() => {
    // --- 1. SET UP CAMERA ---
    async function setupCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: { ideal: 640 }, height: { ideal: 480 } } 
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing camera: ", err);
        alert("Could not access camera. Please grant permission and refresh.");
      }
    }
    setupCamera();
    
    // --- 2. CONNECT TO WEBSOCKET SERVER ---
    // TODO: Replace with your actual server IP address
    const serverUrl = "http://172.25.25.112:8080"; 
    socketRef.current = io(serverUrl);

    socketRef.current.on('connect', () => {
        console.log('Connected to detection server!');
        setIsConnected(true);
    });
    socketRef.current.on('disconnect', () => {
        console.log('Disconnected from server.');
        setIsConnected(false);
    });
    
    socketRef.current.on('detection_results', (data) => {
      setDetections(data.detections || []);
      isProcessing.current = false; // Allow the next frame to be sent
    });

    // --- 3. START SENDING FRAMES ---
    const frameInterval = setInterval(() => {
      if (videoRef.current && videoRef.current.readyState === 4 && !isProcessing.current) {
        isProcessing.current = true;
        
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/jpeg', 0.8); // Use JPEG for smaller size
        socketRef.current.emit('process_frame', imageData);
      }
    }, 500); // Send a frame every 500ms (2 FPS).

    // --- 4. CLEANUP ---
    return () => {
      clearInterval(frameInterval);
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  // --- Calculate scaling factors based on the video container size ---
  const getScaleFactors = () => {
      if (!videoRef.current || !containerRef.current || videoRef.current.videoWidth === 0) {
          return { scaleX: 1, scaleY: 1 };
      }
      const { clientWidth, clientHeight } = containerRef.current;
      const { videoWidth, videoHeight } = videoRef.current;

      return {
          scaleX: clientWidth / videoWidth,
          scaleY: clientHeight / videoHeight
      };
  }
  const { scaleX, scaleY } = getScaleFactors();


  return (
    <div className="card">
      {/* ==================================================================== */}
      {/* ## THIS IS THE CONNECTION STATUS LINE YOU REQUESTED ## */}
      {/* ==================================================================== */}
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
         <div style={{
           width: 12, height: 12, borderRadius: '50%',
           backgroundColor: isConnected ? '#4caf50' : '#f44336',
           marginRight: '8px',
           transition: 'background-color 0.3s'
         }}></div>
        <h2 style={{ margin: 0 }}>
          Live Detection Feed: <span style={{color: isConnected ? '#4caf50' : '#f44336'}}>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </h2>
      </div>

      <div ref={containerRef} style={{ position: 'relative', width: '100%', aspectRatio: `16/9`, backgroundColor: '#000', borderRadius: '8px', overflow: 'hidden' }}>
        <video 
          ref={videoRef} 
          autoPlay 
          playsInline 
          muted 
          style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
        />
        
        {/* Render detection boxes */}
        {detections.map((det, index) => (
          <div key={index} style={{
            position: 'absolute',
            left: `${det.box[0] * scaleX}px`,
            top: `${det.box[1] * scaleY}px`,
            width: `${(det.box[2] - det.box[0]) * scaleX}px`,
            height: `${(det.box[3] - det.box[1]) * scaleY}px`,
            border: '3px solid #4caf50',
            boxSizing: 'border-box',
            transition: 'all 0.1s linear'
          }}>
            <p style={{
              backgroundColor: '#4caf50',
              color: 'white',
              padding: '2px 6px',
              fontSize: '14px',
              fontWeight: 'bold',
              margin: 0,
              position: 'absolute',
              top: '-24px',
              whiteSpace: 'nowrap'
            }}>
              {det.label} ({(det.confidence * 100).toFixed(0)}%)
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DiseaseDetectionPage;