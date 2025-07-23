import React, { useState } from 'react';
import './App.css';
import ScreenshotUpload from './components/ScreenshotUpload';
import AnalysisResults from './components/AnalysisResults';
import LoadingBar from './components/LoadingBar';
import { apiService } from './services/api';
import { exportAnalysisResults } from './utils/csvExport';

function App() {
  const [uploadedScreenshot, setUploadedScreenshot] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showLoadingBar, setShowLoadingBar] = useState(false);
  const [error, setError] = useState(null);

  const handleScreenshotUpload = (file) => {
    setUploadedScreenshot(file);
    setAnalysisData(null);
    setError(null);
    console.log('Screenshot uploaded:', file.name);
  };

  const handleGenerateBacklog = async () => {
    if (!uploadedScreenshot) return;

    setIsAnalyzing(true);
    setShowLoadingBar(true);
    setError(null);

    try {
      console.log('Starting analysis...');
      const result = await apiService.analyzeScreenshot(uploadedScreenshot);
      console.log('Analysis completed:', result);
      console.log('Number of ideas:', result.ideas ? result.ideas.length : 0);
      console.log('First idea:', result.ideas && result.ideas.length > 0 ? result.ideas[0] : 'No ideas');
      setAnalysisData(result);
    } catch (err) {
      console.error('Analysis failed:', err);
      setError(err.message || 'Analysis failed. Please try again.');
      // Hide loading bar immediately on error
      setShowLoadingBar(false);
    }
    // Remove the finally block - let loading bar complete naturally
  };

  const handleLoadingComplete = () => {
    // This will be called when the loading bar reaches 100%
    setShowLoadingBar(false);
    setIsAnalyzing(false); // Also set analyzing to false when loading completes
  };

  const handleExportCSV = (ideas) => {
    try {
      exportAnalysisResults(ideas);
    } catch (err) {
      console.error('Export failed:', err);
      setError('Export failed. Please try again.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-yusha's Growth Backlog Generator</h1>
        <p>Generate and prioritize growth initiatives for your business</p>
      </header>
      <main>
        <ScreenshotUpload onScreenshotUpload={handleScreenshotUpload} />
        
        {uploadedScreenshot && !analysisData && (
          <div className="upload-success">
            <h3>✅ Screenshot Uploaded Successfully!</h3>
            <p>Ready to generate backlog for: <strong>{uploadedScreenshot.name}</strong></p>
            <button 
              className="generate-button"
              onClick={handleGenerateBacklog}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? '🔄 Analyzing...' : 'Generate Growth Backlog'}
            </button>
          </div>
        )}

        {error && (
          <div className="error-message">
            <h3>❌ Error</h3>
            <p>{error}</p>
            <button 
              className="retry-button"
              onClick={handleGenerateBacklog}
              disabled={isAnalyzing}
            >
              Try Again
            </button>
          </div>
        )}

        {analysisData && (
          <AnalysisResults 
            analysisData={analysisData} 
            onExportCSV={handleExportCSV}
          />
        )}
      </main>
      
      <LoadingBar 
        isVisible={showLoadingBar} 
        onComplete={handleLoadingComplete}
      />
    </div>
  );
}

export default App; 