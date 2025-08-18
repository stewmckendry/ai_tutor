from pyairtable import Api
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from app.config import settings

logger = logging.getLogger(__name__)


class AirtableService:
    """Service for interacting with Airtable curriculum content"""
    
    def __init__(self):
        self.api = None
        self.base = None
        self.is_initialized = False
        self.cache = {}
        self.cache_expiry = {}
    
    async def initialize(self):
        """Initialize Airtable connection"""
        try:
            self.api = Api(settings.airtable_api_key)
            self.base = self.api.base(settings.airtable_base_id)
            self.is_initialized = True
            logger.info("Airtable service initialized successfully")
            
            await self._load_initial_content()
            
        except Exception as e:
            logger.error(f"Failed to initialize Airtable service: {str(e)}")
            self.is_initialized = False
    
    async def check_health(self) -> bool:
        """Check if Airtable service is healthy"""
        if not self.is_initialized:
            return False
        
        try:
            curriculum_table = self.base.table('Curriculum')
            records = curriculum_table.all(max_records=1)
            return True
        except Exception as e:
            logger.error(f"Airtable health check failed: {str(e)}")
            return False
    
    async def get_content_for_topic(self, topic: str) -> Optional[Dict[str, Any]]:
        """Get curriculum content for a specific topic"""
        
        cache_key = f"topic_{topic}"
        if self._is_cache_valid(cache_key):
            logger.debug(f"Returning cached content for topic: {topic}")
            return self.cache[cache_key]
        
        try:
            curriculum_table = self.base.table('Curriculum')
            
            formula = f"LOWER({{Topic}}) = '{topic.lower()}'"
            records = curriculum_table.all(formula=formula)
            
            if not records:
                formula = f"SEARCH('{topic.lower()}', LOWER({{Topic}})) > 0"
                records = curriculum_table.all(formula=formula)
            
            if records:
                content = self._format_curriculum_content(records[0])
                self._update_cache(cache_key, content)
                return content
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to fetch content for topic {topic}: {str(e)}")
            return self._get_fallback_content(topic)
    
    async def get_canadian_examples(self, topic: str) -> List[str]:
        """Get Canadian examples for a topic"""
        try:
            examples_table = self.base.table('CanadianExamples')
            
            formula = f"LOWER({{Topic}}) = '{topic.lower()}'"
            records = examples_table.all(formula=formula)
            
            examples = []
            for record in records:
                if 'fields' in record and 'Example' in record['fields']:
                    examples.append(record['fields']['Example'])
            
            return examples
            
        except Exception as e:
            logger.error(f"Failed to fetch Canadian examples: {str(e)}")
            return self._get_fallback_canadian_examples(topic)
    
    async def get_activities(self, topic: str) -> List[Dict[str, Any]]:
        """Get hands-on activities for a topic"""
        try:
            activities_table = self.base.table('Activities')
            
            formula = f"LOWER({{Topic}}) = '{topic.lower()}'"
            records = activities_table.all(formula=formula)
            
            activities = []
            for record in records:
                if 'fields' in record:
                    activity = {
                        'name': record['fields'].get('Name', 'Activity'),
                        'description': record['fields'].get('Description', ''),
                        'materials': record['fields'].get('Materials', '').split(',') if record['fields'].get('Materials') else [],
                        'steps': record['fields'].get('Steps', '').split('\n') if record['fields'].get('Steps') else [],
                        'learning_outcome': record['fields'].get('LearningOutcome', '')
                    }
                    activities.append(activity)
            
            return activities
            
        except Exception as e:
            logger.error(f"Failed to fetch activities: {str(e)}")
            return self._get_fallback_activities(topic)
    
    async def _load_initial_content(self):
        """Load initial content into cache"""
        try:
            topics = ['light', 'sound', 'structures', 'habitats', 'rocks', 'pulleys']
            for topic in topics:
                await self.get_content_for_topic(topic)
            logger.info("Initial content loaded into cache")
        except Exception as e:
            logger.warning(f"Failed to load initial content: {str(e)}")
    
    def _format_curriculum_content(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Format Airtable record into curriculum content"""
        fields = record.get('fields', {})
        
        return {
            'topic': fields.get('Topic', ''),
            'content': fields.get('Content', ''),
            'grade_level': fields.get('GradeLevel', 'Grade 4'),
            'learning_objectives': fields.get('LearningObjectives', '').split('\n') if fields.get('LearningObjectives') else [],
            'key_concepts': fields.get('KeyConcepts', '').split(',') if fields.get('KeyConcepts') else [],
            'vocabulary': fields.get('Vocabulary', '').split(',') if fields.get('Vocabulary') else [],
            'ontario_expectations': fields.get('OntarioExpectations', ''),
            'assessment_ideas': fields.get('AssessmentIdeas', '').split('\n') if fields.get('AssessmentIdeas') else []
        }
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached content is still valid"""
        if key not in self.cache or key not in self.cache_expiry:
            return False
        return datetime.utcnow() < self.cache_expiry[key]
    
    def _update_cache(self, key: str, value: Any):
        """Update cache with new content"""
        self.cache[key] = value
        self.cache_expiry[key] = datetime.utcnow() + timedelta(seconds=settings.cache_ttl_seconds)
    
    def _get_fallback_content(self, topic: str) -> Dict[str, Any]:
        """Get fallback content when Airtable is unavailable"""
        fallback_content = {
            'light': {
                'topic': 'Light and Sound',
                'content': 'Light travels in straight lines and can be reflected, refracted, and absorbed.',
                'grade_level': 'Grade 4',
                'learning_objectives': [
                    'Understand how light travels',
                    'Explore reflection and shadows',
                    'Learn about colors and light'
                ],
                'canadian_examples': [
                    'Northern Lights (Aurora Borealis)',
                    'Reflection on Canadian lakes',
                    'Rainbow at Niagara Falls'
                ]
            },
            'sound': {
                'topic': 'Sound',
                'content': 'Sound is created by vibrations and travels in waves through different materials.',
                'grade_level': 'Grade 4',
                'learning_objectives': [
                    'Understand how sound is produced',
                    'Explore pitch and volume',
                    'Learn how sound travels'
                ],
                'canadian_examples': [
                    'Echo in the Rocky Mountains',
                    'Whale songs in the Pacific',
                    'Thunder during Canadian storms'
                ]
            }
        }
        
        return fallback_content.get(topic, {
            'topic': topic,
            'content': f'Learning about {topic}',
            'grade_level': 'Grade 4',
            'learning_objectives': [f'Explore {topic}'],
            'canadian_examples': []
        })
    
    def _get_fallback_canadian_examples(self, topic: str) -> List[str]:
        """Get fallback Canadian examples"""
        examples = {
            'light': ['Northern Lights in Yukon', 'Sunrise over Lake Ontario', 'Rainbow at Niagara Falls'],
            'sound': ['Loon calls on Canadian lakes', 'Thunder Bay storms', 'CN Tower wind sounds'],
            'structures': ['CN Tower', 'Confederation Bridge', 'Quebec City walls'],
            'habitats': ['Canadian Arctic tundra', 'Great Lakes ecosystem', 'Pacific rainforest']
        }
        return examples.get(topic, [f'Canadian example related to {topic}'])
    
    def _get_fallback_activities(self, topic: str) -> List[Dict[str, Any]]:
        """Get fallback activities"""
        activities = {
            'light': [{
                'name': 'Shadow Puppet Theatre',
                'description': 'Create shadows using flashlights and objects',
                'materials': ['Flashlight', 'Paper', 'Objects'],
                'steps': ['Set up flashlight', 'Place objects', 'Observe shadows'],
                'learning_outcome': 'Understanding how shadows are formed'
            }],
            'sound': [{
                'name': 'Water Glass Orchestra',
                'description': 'Make different sounds with water glasses',
                'materials': ['Glasses', 'Water', 'Spoon'],
                'steps': ['Fill glasses with different water levels', 'Tap gently', 'Listen to pitch differences'],
                'learning_outcome': 'Understanding pitch and vibration'
            }]
        }
        return activities.get(topic, [{
            'name': f'{topic.title()} Exploration',
            'description': f'Hands-on activity exploring {topic}',
            'materials': ['Various materials'],
            'steps': ['Explore and discover'],
            'learning_outcome': f'Understanding {topic}'
        }])
    
    async def cleanup(self):
        """Cleanup Airtable service resources"""
        self.api = None
        self.base = None
        self.cache.clear()
        self.cache_expiry.clear()
        self.is_initialized = False
        logger.info("Airtable service cleaned up")