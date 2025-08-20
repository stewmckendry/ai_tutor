#!/usr/bin/env python3
"""
Content Validation Framework for Canadian Educational Content
Ensures content is age-appropriate for Grade 4 students (ages 9-10)
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Results from content validation"""
    is_appropriate: bool
    score: float
    issues: List[str]
    suggestions: List[str]
    reading_level: str
    has_canadian_context: bool


class ContentValidator:
    """Validates content for Grade 4 appropriateness and educational value"""
    
    # Keywords to avoid for Grade 4 students
    INAPPROPRIATE_KEYWORDS = {
        'violence': [
            'death', 'died', 'killed', 'murder', 'suicide', 'violence', 
            'assault', 'attack', 'shooting', 'stabbing', 'bomb', 'explosion',
            'terrorist', 'terrorism', 'weapon', 'gun', 'knife'
        ],
        'mature_themes': [
            'sex', 'sexual', 'rape', 'abuse', 'drug', 'alcohol', 'cigarette',
            'addiction', 'overdose', 'drunk', 'intoxicated', 'gambling'
        ],
        'complex_politics': [
            'election', 'politician', 'parliament', 'senate', 'scandal',
            'corruption', 'impeach', 'partisan', 'ideology', 'extremist',
            'radical', 'conspiracy', 'propaganda'
        ],
        'health_anxiety': [
            'cancer', 'tumor', 'disease', 'illness', 'virus', 'pandemic',
            'epidemic', 'infection', 'surgery', 'hospital', 'emergency',
            'fatal', 'terminal', 'diagnosis'
        ],
        'disturbing': [
            'horror', 'scary', 'nightmare', 'demon', 'evil', 'haunted',
            'ghost', 'corpse', 'blood', 'gore', 'torture', 'suffer'
        ]
    }
    
    # Educational keywords to prioritize
    EDUCATIONAL_KEYWORDS = {
        'science': [
            'science', 'experiment', 'discovery', 'research', 'study',
            'observe', 'hypothesis', 'data', 'measure', 'investigate',
            'explore', 'learn', 'understand', 'explain', 'wonder'
        ],
        'nature': [
            'nature', 'animal', 'plant', 'ecosystem', 'habitat', 'species',
            'environment', 'conservation', 'wildlife', 'forest', 'ocean',
            'weather', 'climate', 'season', 'earth'
        ],
        'technology': [
            'technology', 'innovation', 'invention', 'robot', 'computer',
            'internet', 'digital', 'code', 'program', 'design', 'create',
            'build', 'engineer', 'solve', 'solution'
        ],
        'canadian': [
            'canada', 'canadian', 'ontario', 'toronto', 'ottawa', 'montreal',
            'vancouver', 'province', 'territory', 'maple', 'hockey', 'rcmp',
            'first nations', 'indigenous', 'inuit', 'métis'
        ],
        'curriculum': [
            'math', 'reading', 'writing', 'art', 'music', 'history',
            'geography', 'french', 'physical education', 'health',
            'social studies', 'language arts'
        ]
    }
    
    # Grade 4 reading level indicators
    COMPLEX_WORDS_PATTERN = re.compile(r'\b\w{10,}\b')  # Words with 10+ letters
    SIMPLE_SENTENCE_PATTERN = re.compile(r'[.!?]+')
    
    def __init__(self):
        """Initialize the content validator"""
        self.validation_stats = {
            'total_processed': 0,
            'approved': 0,
            'rejected': 0,
            'rejection_reasons': {}
        }
    
    def validate_content(self, content: Dict) -> ValidationResult:
        """
        Validate content for Grade 4 appropriateness
        
        Args:
            content: Dictionary containing content fields
            
        Returns:
            ValidationResult with validation details
        """
        self.validation_stats['total_processed'] += 1
        
        # Extract text for analysis
        text_fields = [
            content.get('title', ''),
            content.get('description', ''),
            content.get('simplified_content', ''),
            content.get('activity_suggestion', '')
        ]
        full_text = ' '.join(text_fields).lower()
        
        issues = []
        suggestions = []
        
        # Check for inappropriate content
        inappropriate_found = self._check_inappropriate_content(full_text)
        if inappropriate_found:
            issues.extend(inappropriate_found)
            
        # Check educational value
        educational_score = self._calculate_educational_score(full_text)
        
        # Check reading level
        reading_level = self._assess_reading_level(full_text)
        if reading_level not in ['Grade 3', 'Grade 4', 'Grade 5']:
            issues.append(f'Reading level ({reading_level}) not appropriate for Grade 4')
            suggestions.append('Simplify language and use shorter sentences')
        
        # Check Canadian context
        has_canadian = self._check_canadian_context(full_text)
        if not has_canadian:
            suggestions.append('Add Canadian examples or references')
        
        # Calculate overall score
        score = self._calculate_overall_score(
            len(issues) == 0,
            educational_score,
            reading_level in ['Grade 3', 'Grade 4', 'Grade 5'],
            has_canadian
        )
        
        # Determine if content is appropriate
        is_appropriate = (
            len(issues) == 0 and 
            score >= 0.7 and
            educational_score >= 0.3
        )
        
        # Update stats
        if is_appropriate:
            self.validation_stats['approved'] += 1
        else:
            self.validation_stats['rejected'] += 1
            for issue in issues:
                category = issue.split(':')[0] if ':' in issue else 'other'
                self.validation_stats['rejection_reasons'][category] = \
                    self.validation_stats['rejection_reasons'].get(category, 0) + 1
        
        return ValidationResult(
            is_appropriate=is_appropriate,
            score=score,
            issues=issues,
            suggestions=suggestions,
            reading_level=reading_level,
            has_canadian_context=has_canadian
        )
    
    def _check_inappropriate_content(self, text: str) -> List[str]:
        """Check for inappropriate keywords"""
        issues = []
        
        for category, keywords in self.INAPPROPRIATE_KEYWORDS.items():
            found = [kw for kw in keywords if kw in text]
            if found:
                issues.append(f"{category}: Found inappropriate terms ({', '.join(found[:3])})")
        
        return issues
    
    def _calculate_educational_score(self, text: str) -> float:
        """Calculate educational value score (0-1)"""
        total_keywords = 0
        categories_found = 0
        
        for category, keywords in self.EDUCATIONAL_KEYWORDS.items():
            found = sum(1 for kw in keywords if kw in text)
            if found > 0:
                categories_found += 1
                total_keywords += found
        
        # Score based on keyword density and category diversity
        keyword_score = min(total_keywords / 10, 1.0)  # Cap at 10 keywords
        diversity_score = categories_found / len(self.EDUCATIONAL_KEYWORDS)
        
        return (keyword_score * 0.6) + (diversity_score * 0.4)
    
    def _assess_reading_level(self, text: str) -> str:
        """Assess reading level of content"""
        if not text:
            return "Unknown"
        
        # Count complex words
        words = text.split()
        complex_words = len(self.COMPLEX_WORDS_PATTERN.findall(text))
        
        # Count sentences
        sentences = len(self.SIMPLE_SENTENCE_PATTERN.split(text)) - 1
        if sentences == 0:
            sentences = 1
        
        # Calculate average words per sentence
        avg_words_per_sentence = len(words) / sentences
        
        # Calculate complexity ratio
        complexity_ratio = complex_words / len(words) if words else 0
        
        # Determine grade level
        if avg_words_per_sentence < 10 and complexity_ratio < 0.1:
            return "Grade 3"
        elif avg_words_per_sentence < 15 and complexity_ratio < 0.15:
            return "Grade 4"
        elif avg_words_per_sentence < 20 and complexity_ratio < 0.2:
            return "Grade 5"
        elif avg_words_per_sentence < 25 and complexity_ratio < 0.25:
            return "Grade 6"
        else:
            return "Above Grade 6"
    
    def _check_canadian_context(self, text: str) -> bool:
        """Check if content has Canadian context"""
        canadian_keywords = self.EDUCATIONAL_KEYWORDS['canadian']
        return any(keyword in text for keyword in canadian_keywords)
    
    def _calculate_overall_score(
        self, 
        no_issues: bool,
        educational_score: float,
        appropriate_reading: bool,
        has_canadian: bool
    ) -> float:
        """Calculate overall content score"""
        score = 0.0
        
        if no_issues:
            score += 0.4
        if educational_score > 0:
            score += educational_score * 0.3
        if appropriate_reading:
            score += 0.2
        if has_canadian:
            score += 0.1
            
        return min(score, 1.0)
    
    def get_statistics(self) -> Dict:
        """Get validation statistics"""
        total = self.validation_stats['total_processed']
        if total == 0:
            return self.validation_stats
        
        self.validation_stats['approval_rate'] = \
            self.validation_stats['approved'] / total
        self.validation_stats['rejection_rate'] = \
            self.validation_stats['rejected'] / total
        
        return self.validation_stats
    
    def validate_batch(self, content_items: List[Dict]) -> List[Tuple[Dict, ValidationResult]]:
        """Validate multiple content items"""
        results = []
        for item in content_items:
            result = self.validate_content(item)
            results.append((item, result))
        return results
    
    def export_report(self, filepath: str = None) -> str:
        """Export validation report"""
        stats = self.get_statistics()
        
        report = f"""
Content Validation Report
Generated: {datetime.now().isoformat()}

Summary Statistics:
- Total Processed: {stats['total_processed']}
- Approved: {stats['approved']}
- Rejected: {stats['rejected']}
- Approval Rate: {stats.get('approval_rate', 0):.2%}
- Rejection Rate: {stats.get('rejection_rate', 0):.2%}

Rejection Reasons:
"""
        for reason, count in stats['rejection_reasons'].items():
            report += f"  - {reason}: {count}\n"
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(report)
        
        return report


def main():
    """Example usage of content validator"""
    validator = ContentValidator()
    
    # Example content to validate
    sample_content = {
        'title': 'How Canadian Scientists Study Arctic Animals',
        'description': 'Learn about polar bears and Arctic foxes in Canada',
        'simplified_content': 'Scientists in Canada study amazing Arctic animals! They watch polar bears hunt for seals and observe Arctic foxes change colour with the seasons.',
        'activity_suggestion': 'Draw your favourite Arctic animal and write three facts about how it survives in the cold.'
    }
    
    result = validator.validate_content(sample_content)
    
    print(f"Content Appropriate: {result.is_appropriate}")
    print(f"Score: {result.score:.2f}")
    print(f"Reading Level: {result.reading_level}")
    print(f"Canadian Context: {result.has_canadian_context}")
    
    if result.issues:
        print("\nIssues Found:")
        for issue in result.issues:
            print(f"  - {issue}")
    
    if result.suggestions:
        print("\nSuggestions:")
        for suggestion in result.suggestions:
            print(f"  - {suggestion}")


if __name__ == "__main__":
    main()