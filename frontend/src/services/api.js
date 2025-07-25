/**
 * API service for communicating with the backend
 */

// Use localhost for development, production URL for deployed version
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (window.location.hostname === 'localhost' ? 'http://localhost:8000' : 'https://ai-growth-backlog-generator.onrender.com');

console.log('API_BASE_URL:', API_BASE_URL);
console.log('window.location.hostname:', window.location.hostname);

// Fallback for when backend is not available
const isBackendAvailable = async () => {
  try {
    console.log('Checking backend availability at:', `${API_BASE_URL}/health`);
    
    // Create a timeout promise
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Health check timeout')), 5000);
    });

    // Create the fetch promise
    const fetchPromise = fetch(`${API_BASE_URL}/health`, { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      }
    });

    // Race between fetch and timeout
    const response = await Promise.race([fetchPromise, timeoutPromise]);
    console.log('Health check response:', response.status, response.ok);
    return response.ok;
  } catch (error) {
    console.warn('Backend health check failed:', error);
    return false;
  }
};

export const apiService = {
  /**
   * Analyze a screenshot and generate growth backlog
   * @param {File} screenshotFile - The uploaded screenshot file
   * @returns {Promise<Object>} Analysis results with ideas and ICE scores
   */
  async analyzeScreenshot(screenshotFile) {
    try {
      console.log('Starting analyzeScreenshot...');
      // Check if backend is available first
      const backendAvailable = await isBackendAvailable();
      console.log('Backend available:', backendAvailable);
      if (!backendAvailable) {
        throw new Error('Backend service is currently unavailable. Please try again in a few minutes.');
      }

      const formData = new FormData();
      formData.append('file', screenshotFile);

      // Create a timeout promise
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Request timed out after 2 minutes')), 120000);
      });

      // Create the fetch promise with better error handling
      const fetchPromise = fetch(`${API_BASE_URL}/analyze-screenshot`, {
        method: 'POST',
        body: formData,
        headers: {
          // Don't set Content-Type for FormData, let browser set it
        },
      });

      // Race between fetch and timeout
      const response = await Promise.race([fetchPromise, timeoutPromise]);

      if (!response.ok) {
        let errorMessage = 'Analysis failed';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          // If we can't parse JSON, use status text
          errorMessage = response.statusText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('API call failed:', error);
      
      // Provide more specific error messages for mobile users
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error: Please check your internet connection and try again.');
      } else if (error.message.includes('timed out')) {
        throw new Error('Request timed out: The analysis is taking longer than expected. Please try again.');
      } else if (error.message.includes('CORS')) {
        throw new Error('Server connection error: Please try again later.');
      } else if (error.message.includes('Backend service is currently unavailable')) {
        throw new Error('Service temporarily unavailable. Please try again in a few minutes.');
      }
      
      throw error;
    }
  },

  /**
   * Health check endpoint
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
}; 