import anthropic
from typing import List, Dict, Any, Optional
import logging
from app.config import settings
from app.models import ChatMessage, ConversationMode

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service for interacting with Claude API"""
    
    def __init__(self):
        self.client = None
        self.model = "claude-3-5-sonnet-20241022"  # Updated to latest model
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize Claude client"""
        try:
            self.client = anthropic.Anthropic(api_key=settings.claude_api_key)
            self.is_initialized = True
            logger.info("Claude service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Claude service: {str(e)}")
            self.is_initialized = False
            raise
    
    async def check_health(self) -> bool:
        """Check if Claude service is healthy"""
        if not self.is_initialized or not self.client:
            return False
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}]
            )
            return True
        except Exception as e:
            logger.error(f"Claude health check failed: {str(e)}")
            return False
    
    async def generate_response(
        self,
        messages: List[ChatMessage],
        system_prompt: str,
        mode: ConversationMode,
        curriculum_content: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate response using Claude"""
        try:
            formatted_messages = self._format_messages(messages)
            
            enhanced_system_prompt = self._enhance_system_prompt(
                system_prompt, 
                mode, 
                curriculum_content
            )
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=enhanced_system_prompt,
                messages=formatted_messages
            )
            
            return response.content[0].text
            
        except anthropic.APIError as e:
            logger.error(f"Claude API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Claude service: {str(e)}")
            raise
    
    def _format_messages(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Format messages for Claude API"""
        formatted = []
        for msg in messages:
            if msg.role != "system":
                formatted.append({
                    "role": msg.role,
                    "content": msg.content
                })
        return formatted
    
    def _enhance_system_prompt(
        self, 
        base_prompt: str, 
        mode: ConversationMode,
        curriculum_content: Optional[Dict[str, Any]] = None
    ) -> str:
        """Enhance system prompt based on mode and curriculum content"""
        enhanced = base_prompt
        
        if mode == ConversationMode.LEARNING:
            enhanced += "\n\nMode: LEARNING - Use Socratic questioning to guide discovery. Ask thought-provoking questions rather than giving direct answers."
        elif mode == ConversationMode.DISCOVERY:
            enhanced += "\n\nMode: DISCOVERY - Encourage exploration and curiosity. Help the student discover concepts through guided inquiry."
        elif mode == ConversationMode.STORY:
            enhanced += "\n\nMode: STORY - Use storytelling and narrative to explain concepts. Make learning engaging through stories."
        
        if curriculum_content:
            enhanced += f"\n\nCurriculum Context: {curriculum_content.get('topic', 'General')}"
            if curriculum_content.get('canadian_examples'):
                enhanced += f"\nCanadian Examples: {', '.join(curriculum_content['canadian_examples'][:3])}"
            if curriculum_content.get('learning_objectives'):
                enhanced += f"\nLearning Objectives: {', '.join(curriculum_content['learning_objectives'][:3])}"
        
        enhanced += "\n\nRemember: You're talking to a Grade 4 student. Use simple language, be encouraging, and make learning fun!"
        
        return enhanced
    
    async def cleanup(self):
        """Cleanup Claude service resources"""
        self.client = None
        self.is_initialized = False
        logger.info("Claude service cleaned up")