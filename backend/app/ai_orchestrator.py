import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from app.models import AIProvider, ConversationMode, SessionData, ChatMessage
from app.claude_service import ClaudeService
from app.openai_service import OpenAIService
from app.prompts import get_system_prompt

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """Orchestrates AI provider selection and message processing"""
    
    def __init__(self):
        self.claude_service = ClaudeService()
        self.openai_service = OpenAIService()
        self.is_initialized = False
        
        self.keywords_learning = [
            "how", "why", "what if", "explain", "tell me about",
            "curious", "wonder", "think", "explore", "discover"
        ]
        
        self.keywords_explanatory = [
            "don't understand", "confused", "help", "stuck",
            "what does", "can you explain", "simpler", "example",
            "show me", "clarify"
        ]
        
        self.keywords_story = [
            "story", "tell a story", "adventure", "imagine",
            "pretend", "once upon", "character"
        ]
        
        self.topic_keywords = {
            "light": ["light", "shadow", "reflection", "refraction", "brightness", "color", "prism"],
            "sound": ["sound", "noise", "vibration", "echo", "pitch", "volume", "frequency"],
            "structures": ["structure", "building", "bridge", "strength", "material", "design"],
            "habitats": ["habitat", "animal", "environment", "ecosystem", "adaptation", "survival"],
            "rocks": ["rock", "mineral", "erosion", "sediment", "fossil", "geology"],
            "pulleys": ["pulley", "gear", "machine", "force", "lever", "mechanical"]
        }
    
    async def initialize(self):
        """Initialize AI services"""
        try:
            await self.claude_service.initialize()
            logger.info("Claude service initialized")
        except Exception as e:
            logger.warning(f"Claude initialization failed: {str(e)}")
        
        try:
            await self.openai_service.initialize()
            logger.info("OpenAI service initialized")
        except Exception as e:
            logger.warning(f"OpenAI initialization failed: {str(e)}")
        
        self.is_initialized = True
    
    async def check_claude_health(self) -> bool:
        """Check Claude service health"""
        return await self.claude_service.check_health()
    
    async def check_openai_health(self) -> bool:
        """Check OpenAI service health"""
        return await self.openai_service.check_health()
    
    async def process_message(
        self,
        message: str,
        session: SessionData,
        curriculum_content: Optional[Dict[str, Any]] = None,
        force_provider: Optional[AIProvider] = None,
        force_mode: Optional[ConversationMode] = None
    ) -> Dict[str, Any]:
        """Process message and generate response"""
        
        provider, mode = self._select_provider_and_mode(
            message, 
            session,
            force_provider,
            force_mode
        )
        
        logger.info(f"Selected provider: {provider}, mode: {mode}")
        
        system_prompt = get_system_prompt(mode)
        
        try:
            if provider == AIProvider.CLAUDE:
                response = await self._use_claude(
                    session.messages,
                    system_prompt,
                    mode,
                    curriculum_content
                )
            else:
                response = await self._use_openai(
                    session.messages,
                    system_prompt,
                    mode,
                    curriculum_content
                )
            
            return {
                "response": response,
                "provider": provider,
                "mode": mode
            }
            
        except Exception as e:
            logger.error(f"Primary provider {provider} failed: {str(e)}")
            
            fallback_provider = (
                AIProvider.OPENAI if provider == AIProvider.CLAUDE 
                else AIProvider.CLAUDE
            )
            
            logger.info(f"Attempting fallback to {fallback_provider}")
            
            try:
                if fallback_provider == AIProvider.CLAUDE:
                    response = await self._use_claude(
                        session.messages,
                        system_prompt,
                        mode,
                        curriculum_content
                    )
                else:
                    response = await self._use_openai(
                        session.messages,
                        system_prompt,
                        mode,
                        curriculum_content
                    )
                
                return {
                    "response": response,
                    "provider": fallback_provider,
                    "mode": mode
                }
            except Exception as fallback_error:
                logger.error(f"Fallback provider {fallback_provider} also failed: {str(fallback_error)}")
                raise Exception("Both AI providers failed. Please try again later.")
    
    def _select_provider_and_mode(
        self,
        message: str,
        session: SessionData,
        force_provider: Optional[AIProvider] = None,
        force_mode: Optional[ConversationMode] = None
    ) -> Tuple[AIProvider, ConversationMode]:
        """Select appropriate AI provider and conversation mode"""
        
        if force_provider and force_mode:
            return force_provider, force_mode
        
        message_lower = message.lower()
        
        mode = force_mode or self._determine_mode(message_lower, session)
        
        if force_provider:
            provider = force_provider
        else:
            if mode in [ConversationMode.LEARNING, ConversationMode.DISCOVERY]:
                provider = AIProvider.CLAUDE
            elif mode == ConversationMode.EXPLANATORY:
                provider = AIProvider.OPENAI
            elif mode == ConversationMode.STORY:
                provider = AIProvider.CLAUDE if len(session.messages) < 10 else AIProvider.OPENAI
            else:
                provider = AIProvider.CLAUDE
        
        return provider, mode
    
    def _determine_mode(self, message_lower: str, session: SessionData) -> ConversationMode:
        """Determine conversation mode based on message content"""
        
        explanatory_score = sum(1 for kw in self.keywords_explanatory if kw in message_lower)
        learning_score = sum(1 for kw in self.keywords_learning if kw in message_lower)
        story_score = sum(1 for kw in self.keywords_story if kw in message_lower)
        
        if len(session.messages) > 5:
            recent_messages = " ".join([m.content.lower() for m in session.messages[-5:]])
            if "confused" in recent_messages or "don't understand" in recent_messages:
                explanatory_score += 2
        
        if explanatory_score > learning_score and explanatory_score > story_score:
            return ConversationMode.EXPLANATORY
        elif story_score > learning_score:
            return ConversationMode.STORY
        elif learning_score > 0:
            return ConversationMode.LEARNING
        else:
            return ConversationMode.DISCOVERY
    
    async def _use_claude(
        self,
        messages: List[ChatMessage],
        system_prompt: str,
        mode: ConversationMode,
        curriculum_content: Optional[Dict[str, Any]] = None
    ) -> str:
        """Use Claude to generate response"""
        return await self.claude_service.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            mode=mode,
            curriculum_content=curriculum_content
        )
    
    async def _use_openai(
        self,
        messages: List[ChatMessage],
        system_prompt: str,
        mode: ConversationMode,
        curriculum_content: Optional[Dict[str, Any]] = None
    ) -> str:
        """Use OpenAI to generate response"""
        return await self.openai_service.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            mode=mode,
            curriculum_content=curriculum_content
        )
    
    def extract_topic(self, message: str) -> Optional[str]:
        """Extract topic from message"""
        message_lower = message.lower()
        
        for topic, keywords in self.topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return topic
        
        return None
    
    def extract_activity_markers(self, response: str) -> List[str]:
        """Extract TODO activity markers from response"""
        pattern = r'TODO:\s*([^\n]+)'
        matches = re.findall(pattern, response)
        return matches
    
    async def cleanup(self):
        """Cleanup AI services"""
        await self.claude_service.cleanup()
        await self.openai_service.cleanup()
        self.is_initialized = False
        logger.info("AI Orchestrator cleaned up")