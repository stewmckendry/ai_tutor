# Python Backend - v0 MVP Setup

## Quick Start for v0

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install minimal dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API keys to .env

# Run development server
uvicorn app.main:app --reload --port 8000

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## v0 MVP Structure (Minimal)

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment config
│   ├── models.py            # Pydantic models
│   ├── ai_orchestrator.py   # Claude + OpenAI selection
│   ├── airtable_service.py  # Airtable curriculum content
│   └── prompts.py           # System prompts
├── .env.example
├── requirements.txt
└── README.md
```

## Key v0 Features

- **Single chat endpoint**: POST /chat/message
- **AI orchestration**: Claude vs OpenAI selection
- **Airtable integration**: Curriculum content retrieval
- **Session handling**: In-memory for v0
- **Basic error handling**: FastAPI defaults

## Environment Setup

```bash
# .env.example
CLAUDE_API_KEY=sk-ant-your-key
OPENAI_API_KEY=sk-your-key
AIRTABLE_API_KEY=your-airtable-key
AIRTABLE_BASE_ID=your-base-id
```

## Core Files to Create

### 1. `app/main.py` - FastAPI App
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chat_endpoint import router as chat_router

app = FastAPI(title="Grade 4 AI Tutor v0", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Grade 4 AI Tutor v0"}
```

### 2. `app/models.py` - Basic Models
```python
from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    provider: str  # "claude" or "openai"
    mode: str      # "learning", "explanatory", "story"
```

### 3. `app/ai_orchestrator.py` - Core Logic
```python
import anthropic
import openai
from app.config import settings

class AIOrchestrator:
    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def process_message(self, message: str) -> dict:
        # Simple provider selection
        provider, mode = self._select_provider(message)
        
        if provider == "claude":
            response = await self._claude_response(message, mode)
        else:
            response = await self._openai_response(message, mode)
        
        return {
            "response": response,
            "provider": provider,
            "mode": mode
        }
```

## Next Steps for v0

1. Create the 4 core files above
2. Add Airtable curriculum integration
3. Test with simple chat frontend
4. Deploy to validate concept

**Goal**: Ship working v0 in 1-2 weeks, not months!
