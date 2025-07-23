/**
 * Utility functions for CSV export
 */

/**
 * Convert analysis results to CSV format
 * @param {Array} ideas - Array of idea objects with ICE scores
 * @returns {string} CSV formatted string
 */
export const exportToCSV = (ideas) => {
  if (!ideas || !Array.isArray(ideas)) {
    throw new Error('Invalid ideas data');
  }

  // Define CSV headers
  const headers = [
    'Priority',
    'Title',
    'Hypothesis',
    'Category',
    'Impact',
    'Confidence',
    'Effort',
    'ICE Score',
    'Estimated Lift',
    'Implementation Time',
    'Description',
    'Reasoning',
    'Implementation Steps',
    'Success Metrics',
    'Priority Level'
  ];

  // Convert ideas to CSV rows
  const rows = ideas.map(idea => [
    idea.priority?.toUpperCase() || '',
    `"${idea.title || ''}"`,
    `"${idea.hypothesis || ''}"`,
    idea.category || '',
    idea.ice?.impact || '',
    idea.ice?.confidence || '',
    idea.ice?.effort || '',
    idea.ice?.score || '',
    `"${idea.estimated_lift || ''}"`,
    `"${idea.implementation_time || ''}"`,
    `"${idea.description || ''}"`,
    `"${idea.reasoning || ''}"`,
    `"${idea.implementation || ''}"`,
    `"${idea.success_metrics || ''}"`,
    idea.priority || ''
  ]);

  // Combine headers and rows
  const csvContent = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');

  return csvContent;
};

/**
 * Download CSV file
 * @param {string} csvContent - CSV formatted string
 * @param {string} filename - Name of the file to download
 */
export const downloadCSV = (csvContent, filename = 'growth-backlog.csv') => {
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

/**
 * Export analysis results to CSV and trigger download
 * @param {Array} ideas - Array of idea objects with ICE scores
 * @param {string} filename - Optional custom filename
 */
export const exportAnalysisResults = (ideas, filename) => {
  try {
    console.log('Exporting ideas to CSV:', ideas);
    console.log('Number of ideas to export:', ideas ? ideas.length : 0);
    
    if (!ideas || ideas.length === 0) {
      console.error('No ideas to export!');
      throw new Error('No ideas to export');
    }
    
    const csvContent = exportToCSV(ideas);
    console.log('CSV content length:', csvContent.length);
    console.log('CSV content preview:', csvContent.substring(0, 200));
    
    const defaultFilename = `growth-backlog-${new Date().toISOString().split('T')[0]}.csv`;
    downloadCSV(csvContent, filename || defaultFilename);
    
    console.log('CSV export completed successfully');
  } catch (error) {
    console.error('CSV export failed:', error);
    throw error;
  }
}; 