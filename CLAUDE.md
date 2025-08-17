# 🤖 Claude Code Implementation Guide

## Project Overview
You are building **Maple**, an AI-powered tutor for Ontario Grade 4 students (ages 9-10). This system uses adaptive AI to provide personalized, curriculum-aligned education with a focus on maintaining intellectual curiosity and critical thinking skills.

## 🎯 Core Principles

### Educational Philosophy
- **Never give direct answers** - Guide discovery through Socratic questioning
- **Promote curiosity** - Encourage "why" and "how" questions over "what"
- **Canadian context** - Use metric units, Canadian examples, and local references
- **Age-appropriate** - Grade 4 reading level, simple explanations, encouraging tone

### Technical Philosophy
- **Ship fast, iterate** - MVP in 2 weeks, then enhance
- **Parallel development** - Multiple workstreams work independently
- **AI orchestration** - Claude for discovery, OpenAI for detailed explanations
- **Real-time data** - Fresh Canadian content daily

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Chat    │───▶│  FastAPI Backend │───▶│   Claude API    │
│   Interface     │    │   (Orchestrator) │    │   OpenAI API    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   RAG System     │
                       │ • Curriculum DB  │
                       │ • Canadian Context│
                       └──────────────────┘
```

## 🔧 Development Standards

### Code Structure
```
ai_tutor/
├── frontend/             # React TypeScript app
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/              # Python FastAPI app
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core logic
│   │   ├── models/      # Pydantic models
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI app
│   ├── tests/
│   └── requirements.txt
├── content/              # RAG and curriculum data
│   ├── embeddings/
│   ├── curriculum/
│   └── canadian/
├── docs/                 # Technical documentation
└── scripts/              # Build and deployment scripts
```

### Tech Stack
- **Frontend**: React 18, TypeScript, Tailwind CSS, Socket.io-client
- **Backend**: Python 3.11+, FastAPI, Pydantic, SQLAlchemy
- **AI**: Anthropic SDK (Claude), OpenAI SDK
- **Database**: PostgreSQL (sessions), Pinecone/Weaviate (vectors)
- **Cache**: Redis
- **Infrastructure**: Docker, n8n workflows
- **Testing**: Pytest (backend), Jest (frontend)

### Git Workflow
```bash
# You're working in a git worktree
# Your branch corresponds to your specific issue
# Example for backend work:
git checkout issue-1b-backend
git add .
git commit -m "feat(backend): implement AI orchestrator"
git push origin issue-1b-backend
```

### Commit Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Testing
- `chore:` Maintenance

## 🐍 Python Backend Standards

### Project Structure
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, content, analytics
from app.core.config import settings

app = FastAPI(title="Maple AI Tutor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat")
app.include_router(content.router, prefix="/api/content")
app.include_router(analytics.router, prefix="/api/analytics")
```

### Pydantic Models
```python
# app/models/chat.py
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class Message(BaseModel):
    id: str
    session_id: str
    role: Literal["student", "tutor"]
    content: str
    mode: Optional[Literal["learning", "explanatory", "story"]] = None
    provider: Optional[Literal["claude", "openai"]] = None
    timestamp: datetime
    todos: Optional[List["TODO"]] = []
    insights: Optional[List["Insight"]] = []

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: Message
    session_id: str
    timestamp: datetime
```

### Service Layer
```python
# app/services/ai_orchestrator.py
from typing import Tuple
from anthropic import Anthropic
from openai import OpenAI
from app.models.chat import Message, ConversationContext
from app.core.config import settings

class AIOrchestrator:
    def __init__(self):
        self.claude = Anthropic(api_key=settings.CLAUDE_API_KEY)
        self.openai = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def process_message(
        self, 
        message: str, 
        context: ConversationContext
    ) -> Message:
        # Select provider and mode
        provider, mode = self._select_provider_and_mode(context)
        
        # Generate prompt
        prompt = self._build_prompt(message, context, provider, mode)
        
        # Get AI response
        if provider == "claude":
            response = await self._get_claude_response(prompt, mode)
        else:
            response = await self._get_openai_response(prompt, mode)
        
        # Process response
        return self._process_response(response, provider, mode)
    
    def _select_provider_and_mode(
        self, 
        context: ConversationContext
    ) -> Tuple[str, str]:
        """Select AI provider and interaction mode based on context"""
        # Implementation here
        pass
```

### Async Patterns
```python
# app/api/chat.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.ai_orchestrator import AIOrchestrator
from app.dependencies import get_session

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    orchestrator: AIOrchestrator = Depends(),
    session = Depends(get_session)
):
    try:
        # Process message
        response = await orchestrator.process_message(
            request.message,
            session.context
        )
        
        # Save to database
        await session.save_message(response)
        
        return ChatResponse(
            response=response,
            session_id=session.id,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Testing
```python
# tests/test_orchestrator.py
import pytest
from app.services.ai_orchestrator import AIOrchestrator
from app.models.chat import ConversationContext

@pytest.mark.asyncio
async def test_provider_selection():
    orchestrator = AIOrchestrator()
    
    # Test discovery question routes to Claude
    context = ConversationContext(
        message_intent="exploration",
        confidence_level=0.8
    )
    provider, mode = orchestrator._select_provider_and_mode(context)
    
    assert provider == "claude"
    assert mode == "learning"

@pytest.mark.asyncio
async def test_struggling_student_gets_openai():
    orchestrator = AIOrchestrator()
    
    context = ConversationContext(
        frustration_level=0.7,
        recent_incorrect=3
    )
    provider, mode = orchestrator._select_provider_and_mode(context)
    
    assert provider == "openai"
    assert mode == "explanatory"
```

## 🎨 UI/UX Guidelines

### Chat Interface
- **Clean and simple** - Focus on conversation, minimal distractions
- **Mobile-first** - Must work on tablets/phones
- **Accessibility** - WCAG 2.1 AA compliance
- **Canadian theme** - Subtle maple leaf accents, red/white color hints

### Message Types
1. **Student Message** - Right-aligned, blue background
2. **Maple Response** - Left-aligned, with avatar
3. **TODO Marker** - Highlighted yellow box with checkbox
4. **Insight Callout** - Light bulb icon with green background
5. **Loading State** - Three dots animation

## 🧠 AI Integration

### Mode Selection Logic
```python
def select_ai_mode(context: ConversationContext) -> Tuple[str, str]:
    """Select provider and mode based on context"""
    
    if context.is_new_concept or context.student_struggling:
        return ("openai", "explanatory")
    
    if context.needs_discovery or context.exploratory_question:
        return ("claude", "learning")
    
    if context.narrative_requested:
        return ("claude", "story")
    
    return ("claude", "learning")  # default
```

### System Prompts

#### Maple Base Persona
```python
BASE_PERSONA = """
You are Maple, a friendly AI tutor for Ontario Grade 4 students.
- Use Canadian English spelling (colour, centre, favourite)
- Reference Canadian contexts (hockey, Tim Hortons, provinces)
- Use metric measurements exclusively
- Speak at a Grade 4 reading level
- Be encouraging and patient
- Never provide direct answers to homework
"""
```

#### Learning Mode Addition
```python
LEARNING_MODE = """
In learning mode:
- Guide discovery through questions
- Use TODO(student): markers for tasks
- Celebrate small victories
- Build from what student knows
- Provide hints, not solutions
"""
```

## 📚 Curriculum Alignment

### Ontario Grade 4 Focus Areas
1. **Science & Technology**
   - Light and Sound (primary focus for MVP)
   - Habitats and Communities
   - Pulleys and Gears
   - Rocks and Minerals

2. **Mathematics**
   - Number Sense and Numeration (to 10,000)
   - Measurement (metric units)
   - Geometry and Spatial Sense
   - Patterning and Algebra
   - Data Management and Probability

3. **Language Arts**
   - Reading comprehension
   - Writing skills
   - Oral communication
   - Media literacy

## 💡 Quick Reference

### Environment Variables
```bash
# Backend (.env)
# AI Configuration
CLAUDE_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Database
DATABASE_URL=postgresql://user:pass@localhost/maple_tutor
REDIS_URL=redis://localhost:6379

# Vector DB
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=us-west1-gcp

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Security
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=20
```

### Useful Commands
```bash
# Backend Development
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Run tests
pytest
pytest --cov=app

# Format code
black app/
isort app/

# Type checking
mypy app/

# Frontend Development
cd frontend
npm install
npm run dev

# Git workflow
git status
git add .
git commit -m "feat: implement feature"
git push
gh pr create
```

### Python Dependencies
```txt
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
python-dotenv==1.0.0
anthropic==0.18.0
openai==1.10.0
sqlalchemy==2.0.25
asyncpg==0.29.0
redis==5.0.1
pinecone-client==3.0.0
langchain==0.1.0
numpy==1.26.0
pandas==2.1.0
pytest==7.4.0
pytest-asyncio==0.23.0
black==23.12.0
isort==5.13.0
mypy==1.8.0
```

## 🎯 Remember

You're building an educational tool that:
1. **Enhances** rather than replaces thinking
2. **Celebrates** Canadian culture and values  
3. **Protects** children's safety and privacy
4. **Promotes** curiosity over answer-seeking
5. **Adapts** to each student's needs

When in doubt, ask: "Does this help the student think better?"
