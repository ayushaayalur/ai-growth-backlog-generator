/**
 * API service for communicating with the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiService = {
  /**
   * Analyze a screenshot and generate growth backlog
   * @param {File} screenshotFile - The uploaded screenshot file
   * @returns {Promise<Object>} Analysis results with ideas and ICE scores
   */
  async analyzeScreenshot(screenshotFile) {
    try {
      const formData = new FormData();
      formData.append('file', screenshotFile);

      // Create a timeout promise
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Request timed out after 2 minutes')), 120000);
      });

      // Create the fetch promise
      const fetchPromise = fetch(`${API_BASE_URL}/analyze-screenshot`, {
        method: 'POST',
        body: formData,
      });

      // Race between fetch and timeout
      const response = await Promise.race([fetchPromise, timeoutPromise]);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      return await response.json();
    } catch (error) {
      console.error('API call failed:', error);
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