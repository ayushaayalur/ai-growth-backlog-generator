export interface ICE {
  impact: number; // 1-10 scale
  confidence: number; // 1-10 scale
  effort: number; // 1-10 scale
  score: number; // Calculated: (impact * confidence) / effort
}

export interface CROIdea {
  id: string;
  title: string;
  description: string;
  hypothesis: string;
  category: 'copy' | 'design' | 'ux' | 'technical' | 'layout';
  ice: ICE;
  reasoning: string;
  examples?: string[];
  bestPractices: string[];
  estimatedLift: string; // e.g., "10-15% conversion increase"
  implementationTime: string; // e.g., "2-3 days"
  priority: 'high' | 'medium' | 'low';
}

export interface AnalysisRequest {
  file: File;
  options?: {
    includeHypotheses?: boolean;
    iceScoring?: boolean;
    exportFormat?: 'json' | 'csv' | 'pdf';
    categories?: string[];
  };
}

export interface AnalysisResponse {
  id: string;
  status: 'processing' | 'completed' | 'failed';
  ideas: CROIdea[];
  summary: {
    totalIdeas: number;
    highPriorityIdeas: number;
    averageImpact: number;
    averageEffort: number;
    estimatedTotalLift: string;
  };
  metadata: {
    fileName: string;
    fileSize: number;
    analysisTime: number;
    timestamp: string;
  };
  error?: string;
}

export interface AnalysisProgress {
  stage: 'uploading' | 'processing' | 'analyzing' | 'generating' | 'completed';
  progress: number; // 0-100
  message: string;
  estimatedTimeRemaining?: number;
}

export interface ExportOptions {
  format: 'csv' | 'json' | 'pdf' | 'jira' | 'notion';
  includeHypotheses: boolean;
  includeReasoning: boolean;
  filterByPriority?: 'high' | 'medium' | 'low' | 'all';
  sortBy?: 'ice_score' | 'impact' | 'effort' | 'category';
} 