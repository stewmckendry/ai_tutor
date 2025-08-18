import openai
from typing import List, Dict, Any, Optional
import logging
from app.config import settings
from app.models import ChatMessage, ConversationMode

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self):
        self.client = None
        self.model = "gpt-4-turbo-preview"
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize OpenAI client"""
        try:
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
            self.is_initialized = True
            logger.info("OpenAI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI service: {str(e)}")
            self.is_initialized = False
            raise
    
    async def check_health(self) -> bool:
        """Check if OpenAI service is healthy"""
        if not self.is_initialized or not self.client:
            return False
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {str(e)}")
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
        """Generate response using OpenAI"""
        try:
            formatted_messages = self._format_messages(messages, system_prompt, mode, curriculum_content)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI service: {str(e)}")
            raise
    
    def _format_messages(
        self, 
        messages: List[ChatMessage],
        system_prompt: str,
        mode: ConversationMode,
        curriculum_content: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Format messages for OpenAI API"""
        formatted = []
        
        enhanced_system = self._enhance_system_prompt(system_prompt, mode, curriculum_content)
        formatted.append({"role": "system", "content": enhanced_system})
        
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
        
        if mode == ConversationMode.EXPLANATORY:
            enhanced += "\n\nMode: EXPLANATORY - Provide clear, detailed explanations. Break down complex concepts into simple terms. Use analogies and examples that a Grade 4 student can relate to."
        elif mode == ConversationMode.STORY:
            enhanced += "\n\nMode: STORY - Use narrative and storytelling to teach. Create engaging scenarios that illustrate the concepts."
        elif mode == ConversationMode.LEARNING:
            enhanced += "\n\nMode: LEARNING - Balance explanation with questions. Help the student understand by providing clear guidance."
        
        if curriculum_content:
            enhanced += f"\n\nCurriculum Context: {curriculum_content.get('topic', 'General')}"
            enhanced += f"\nGrade Level: {curriculum_content.get('grade_level', 'Grade 4')}"
            
            if curriculum_content.get('canadian_examples'):
                enhanced += f"\nCanadian Context: Use these examples when relevant: {', '.join(curriculum_content['canadian_examples'][:3])}"
            
            if curriculum_content.get('learning_objectives'):
                enhanced += f"\nLearning Goals: {', '.join(curriculum_content['learning_objectives'][:3])}"
            
            if curriculum_content.get('activities'):
                enhanced += "\nHands-on Activities Available: Suggest TODO activities when appropriate."
        
        enhanced += """
        
Important Guidelines:
- You're talking to a Grade 4 student (age 9-10)
- Use simple, clear language
- Be encouraging and positive
- Make connections to everyday life
- Include Canadian references when possible
- Mark hands-on activities with 'TODO:' prefix
"""
        
        return enhanced
    
    async def cleanup(self):
        """Cleanup OpenAI service resources"""
        self.client = None
        self.is_initialized = False
        logger.info("OpenAI service cleaned up")