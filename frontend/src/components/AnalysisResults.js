import React from 'react';
import './AnalysisResults.css';

const AnalysisResults = ({ analysisData, onExportCSV }) => {
  console.log('AnalysisResults received data:', analysisData);
  console.log('AnalysisData ideas:', analysisData?.ideas);
  console.log('Number of ideas:', analysisData?.ideas?.length || 0);
  
  if (!analysisData || !analysisData.ideas) {
    console.log('No analysis data or ideas, returning null');
    return null;
  }

  const { ideas, summary } = analysisData;
  
  // Sort ideas by ICE score in descending order (highest first)
  const sortedIdeas = [...ideas].sort((a, b) => {
    const scoreA = parseFloat(a.ice.score) || 0;
    const scoreB = parseFloat(b.ice.score) || 0;
    return scoreB - scoreA;
  });
  
  console.log('Rendering with ideas:', sortedIdeas.length);

  const handleExportCSV = () => {
    if (onExportCSV) {
      onExportCSV(sortedIdeas); // Export sorted ideas
    }
  };

  return (
    <div className="analysis-results">
      <div className="results-header">
        <h2>Growth Backlog Analysis Results</h2>
        <div className="summary-stats">
          <div className="stat">
            <span className="stat-number">{summary.total_ideas}</span>
            <span className="stat-label">Total Ideas</span>
          </div>
          <div className="stat">
            <span className="stat-number">{summary.high_priority_ideas}</span>
            <span className="stat-label">High Priority</span>
          </div>
          <div className="stat">
            <span className="stat-number">{summary.average_impact}</span>
            <span className="stat-label">Avg Impact</span>
          </div>
          <div className="stat">
            <span className="stat-number">{summary.average_effort}</span>
            <span className="stat-label">Avg Effort</span>
          </div>
        </div>
        <button className="export-button" onClick={handleExportCSV}>
          📊 Export to CSV
        </button>
      </div>

      <div className="results-table-container">
        <table className="results-table">
          <thead>
            <tr>
              <th>Priority</th>
              <th>Title</th>
              <th>Hypothesis</th>
              <th>Category</th>
              <th>Impact</th>
              <th>Confidence</th>
              <th>Effort</th>
              <th>ICE Score</th>
              <th>Est. Lift</th>
              <th>Time</th>
              <th>Implementation</th>
            </tr>
          </thead>
          <tbody>
            {sortedIdeas.map((idea, index) => (
              <tr key={idea.id || index} className={`priority-${idea.priority}`}>
                <td>
                  <span className={`priority-badge ${idea.priority}`}>
                    {idea.priority.toUpperCase()}
                  </span>
                </td>
                <td className="idea-title">{idea.title}</td>
                <td className="idea-hypothesis">{idea.hypothesis}</td>
                <td>
                  <span className="category-badge">{idea.category}</span>
                </td>
                <td className="ice-score impact">{idea.ice.impact}</td>
                <td className="ice-score confidence">{idea.ice.confidence}</td>
                <td className="ice-score effort">{idea.ice.effort}</td>
                <td className="ice-score total">
                  <strong>{idea.ice.score}</strong>
                </td>
                <td className="estimated-lift">{idea.estimated_lift}</td>
                <td className="implementation-time">{idea.implementation_time}</td>
                <td className="implementation-steps">
                  <details>
                    <summary>View Steps</summary>
                    <div className="steps-content">
                      {idea.implementation ? (
                        idea.implementation.split('.').map((step, index) => (
                          step.trim() && <div key={index} className="step">• {step.trim()}</div>
                        ))
                      ) : (
                        <div className="no-steps">No implementation steps available</div>
                      )}
                    </div>
                  </details>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="results-footer">
        <p>
          <strong>Estimated Total Impact:</strong> {summary.estimated_total_lift}
        </p>
        <p>
          <strong>Analysis Summary:</strong> Generated {summary.total_ideas} actionable growth ideas 
          with {summary.high_priority_ideas} high-priority opportunities.
        </p>
      </div>
    </div>
  );
};

export default AnalysisResults; 