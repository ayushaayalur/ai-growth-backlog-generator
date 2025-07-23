import React, { useState, useEffect, useRef } from 'react';
import './LoadingBar.css';

const LoadingBar = ({ isVisible, onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const onCompleteRef = useRef(onComplete);

  const steps = [
    'Uploading screenshot...',
    'Analyzing visual elements...',
    'Extracting text content...',
    'Generating CRO ideas...',
    'Calculating ICE scores...',
    'Finalizing results...'
  ];

  // Update the ref when onComplete changes
  useEffect(() => {
    onCompleteRef.current = onComplete;
  }, [onComplete]);

  useEffect(() => {
    if (!isVisible) {
      setProgress(0);
      setCurrentStep(0);
      return;
    }

    const startTime = Date.now();
    const duration = 6000; // 6 seconds

    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min((elapsed / duration) * 100, 100);
      
      setProgress(newProgress);
      
      // Update step based on progress
      const stepIndex = Math.floor((newProgress / 100) * steps.length);
      setCurrentStep(Math.min(stepIndex, steps.length - 1));

      if (newProgress >= 100) {
        clearInterval(timer);
        if (onCompleteRef.current) {
          onCompleteRef.current();
        }
      }
    }, 50); // Update every 50ms for smooth animation

    return () => clearInterval(timer);
  }, [isVisible]); // Only depend on isVisible, not onComplete

  if (!isVisible) return null;

  return (
    <div className="loading-container">
      <div className="loading-content">
        <h3>🔄 Analyzing Your Screenshot</h3>
        <p className="current-step">{steps[currentStep]}</p>
        
        <div className="progress-bar-container">
          <div 
            className="progress-bar" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        
        <div className="progress-text">
          {Math.round(progress)}% Complete
        </div>
        
        <div className="loading-tips">
          <p>💡 <strong>Tip:</strong> This usually takes about 6 seconds to analyze your page</p>
          <p>📊 We're analyzing your page for conversion optimization opportunities</p>
        </div>
      </div>
    </div>
  );
};

export default LoadingBar; 