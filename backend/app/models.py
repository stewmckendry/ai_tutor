from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class AIProvider(str, Enum):
    CLAUDE = "claude"
    OPENAI = "openai"


class ConversationMode(str, Enum):
    LEARNING = "learning"
    EXPLANATORY = "explanatory"
    STORY = "story"
    DISCOVERY = "discovery"


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    provider: Optional[AIProvider] = None
    mode: Optional[ConversationMode] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    force_provider: Optional[AIProvider] = None
    force_mode: Optional[ConversationMode] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    provider: AIProvider
    mode: ConversationMode
    has_activity: bool = False
    activity_markers: Optional[List[str]] = None
    curriculum_content: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None  # Enhanced metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SessionData(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    created_at: datetime
    last_activity: datetime
    current_topic: Optional[str] = None
    student_level: Optional[str] = "grade-4"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, bool]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AirtableContent(BaseModel):
    topic: str
    content: str
    grade_level: str
    canadian_examples: Optional[List[str]] = None
    activities: Optional[List[Dict[str, Any]]] = None
    learning_objectives: Optional[List[str]] = None


class AIProviderConfig(BaseModel):
    provider: AIProvider
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str