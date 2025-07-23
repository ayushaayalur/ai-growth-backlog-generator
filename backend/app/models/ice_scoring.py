"""
ICE (Impact, Confidence, Effort) Scoring System
for prioritizing CRO ideas based on growth best practices
"""

from typing import Dict, List, Tuple
import math

class ICEScorer:
    """ICE Scoring system for CRO idea prioritization"""
    
    def __init__(self):
        self.impact_factors = {
            'value_proposition': 0.25,
            'cta_optimization': 0.20,
            'trust_signals': 0.15,
            'social_proof': 0.15,
            'form_optimization': 0.10,
            'visual_hierarchy': 0.10,
            'mobile_optimization': 0.05
        }
        
        self.confidence_factors = {
            'case_study_evidence': 0.40,
            'best_practice_alignment': 0.30,
            'logical_reasoning': 0.20,
            'industry_standard': 0.10
        }
        
        self.effort_factors = {
            'implementation_complexity': 0.40,
            'development_time': 0.30,
            'design_work': 0.20,
            'testing_requirements': 0.10
        }
    
    def calculate_impact(self, idea_data: Dict) -> float:
        """
        Calculate impact score (1-10) based on potential conversion lift
        
        Args:
            idea_data: Dictionary containing idea analysis data
            
        Returns:
            float: Impact score between 1-10
        """
        base_score = 5.0
        
        # Adjust based on category
        category_weights = {
            'copy': 1.2,
            'design': 1.1,
            'ux': 1.3,
            'technical': 0.9,
            'layout': 1.0
        }
        
        category = idea_data.get('category', 'layout')
        base_score *= category_weights.get(category, 1.0)
        
        # Adjust based on specific factors
        if idea_data.get('affects_value_proposition'):
            base_score += 2.0
        if idea_data.get('affects_cta'):
            base_score += 1.5
        if idea_data.get('affects_trust'):
            base_score += 1.0
        if idea_data.get('affects_social_proof'):
            base_score += 1.0
            
        # Cap at 10
        return min(10.0, max(1.0, base_score))
    
    def calculate_confidence(self, idea_data: Dict) -> float:
        """
        Calculate confidence score (1-10) based on evidence and best practices
        
        Args:
            idea_data: Dictionary containing idea analysis data
            
        Returns:
            float: Confidence score between 1-10
        """
        base_score = 5.0
        
        # Evidence from case studies
        if idea_data.get('has_case_studies'):
            base_score += 2.0
        if idea_data.get('case_study_count', 0) > 3:
            base_score += 1.0
            
        # Best practice alignment
        if idea_data.get('follows_best_practices'):
            base_score += 1.5
        if idea_data.get('industry_standard'):
            base_score += 1.0
            
        # Logical reasoning strength
        reasoning_strength = idea_data.get('reasoning_strength', 0.5)
        base_score += reasoning_strength * 2.0
        
        # Cap at 10
        return min(10.0, max(1.0, base_score))
    
    def calculate_effort(self, idea_data: Dict) -> float:
        """
        Calculate effort score (1-10) based on implementation complexity
        
        Args:
            idea_data: Dictionary containing idea analysis data
            
        Returns:
            float: Effort score between 1-10 (higher = more effort)
        """
        base_score = 5.0
        
        # Implementation complexity
        complexity = idea_data.get('complexity', 'medium')
        complexity_scores = {'low': -2, 'medium': 0, 'high': 2}
        base_score += complexity_scores.get(complexity, 0)
        
        # Development time
        dev_time_days = idea_data.get('dev_time_days', 3)
        if dev_time_days <= 1:
            base_score -= 2
        elif dev_time_days <= 3:
            base_score -= 1
        elif dev_time_days >= 7:
            base_score += 2
            
        # Design work required
        if idea_data.get('requires_design'):
            base_score += 1
        if idea_data.get('requires_copywriting'):
            base_score += 0.5
            
        # Testing requirements
        if idea_data.get('requires_ab_testing'):
            base_score += 1
        if idea_data.get('requires_user_research'):
            base_score += 1.5
            
        # Cap at 10
        return min(10.0, max(1.0, base_score))
    
    def calculate_ice_score(self, impact: float, confidence: float, effort: float) -> float:
        """
        Calculate ICE score using the formula: (Impact × Confidence) / Effort
        
        Args:
            impact: Impact score (1-10)
            confidence: Confidence score (1-10)
            effort: Effort score (1-10)
            
        Returns:
            float: ICE score (higher = higher priority)
        """
        if effort == 0:
            return 0.0
        
        ice_score = (impact * confidence) / effort
        return round(ice_score, 2)
    
    def get_priority_level(self, ice_score: float) -> str:
        """
        Determine priority level based on ICE score
        
        Args:
            ice_score: Calculated ICE score
            
        Returns:
            str: Priority level ('high', 'medium', 'low')
        """
        if ice_score >= 8.0:
            return 'high'
        elif ice_score >= 4.0:
            return 'medium'
        else:
            return 'low'
    
    def score_idea(self, idea_data: Dict) -> Dict:
        """
        Score a complete CRO idea with ICE metrics
        
        Args:
            idea_data: Dictionary containing idea analysis data
            
        Returns:
            Dict: Complete ICE scoring results
        """
        impact = self.calculate_impact(idea_data)
        confidence = self.calculate_confidence(idea_data)
        effort = self.calculate_effort(idea_data)
        ice_score = self.calculate_ice_score(impact, confidence, effort)
        priority = self.get_priority_level(ice_score)
        
        return {
            'impact': round(impact, 1),
            'confidence': round(confidence, 1),
            'effort': round(effort, 1),
            'ice_score': ice_score,
            'priority': priority,
            'estimated_lift': self._estimate_lift(impact, confidence),
            'implementation_time': self._estimate_time(effort)
        }
    
    def _estimate_lift(self, impact: float, confidence: float) -> str:
        """Estimate conversion lift based on impact and confidence"""
        expected_lift = (impact * confidence) / 100 * 25  # Base 25% max lift
        
        if expected_lift >= 15:
            return "15-25% conversion increase"
        elif expected_lift >= 10:
            return "10-15% conversion increase"
        elif expected_lift >= 5:
            return "5-10% conversion increase"
        else:
            return "2-5% conversion increase"
    
    def _estimate_time(self, effort: float) -> str:
        """Estimate implementation time based on effort score"""
        if effort <= 3:
            return "1-2 days"
        elif effort <= 6:
            return "3-5 days"
        else:
            return "1-2 weeks"
    
    def sort_ideas_by_priority(self, ideas: List[Dict]) -> List[Dict]:
        """
        Sort ideas by ICE score in descending order
        
        Args:
            ideas: List of ideas with ICE scores
            
        Returns:
            List[Dict]: Sorted ideas by priority
        """
        return sorted(ideas, key=lambda x: x.get('ice_score', 0), reverse=True) 