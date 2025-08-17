# Grade 4 AI Tutor - v0 Documentation

## Overview
Minimal viable product for Ontario Grade 4 AI tutor with Claude/OpenAI orchestration and Airtable curriculum integration.

## Core Components (v0 Only)

### 1. AI Orchestration
- **Claude**: Discovery learning, Socratic method, storytelling
- **OpenAI**: Direct explanations when student struggling
- **Simple selection logic**: Based on message content analysis

### 2. Airtable Integration
- **Curriculum Content**: Ontario Grade 4 expectations
- **Canadian Examples**: Real-world context
- **Activity Templates**: TODO markers for hands-on learning

### 3. Basic Chat API
- Single endpoint: `POST /api/chat/message`
- In-memory session handling
- No auth required for v0

## API Specification

### POST /api/chat/message

**Request:**
```json
{
  "message": "How does light travel?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Great question! Let me ask you something first - when you turn on a flashlight in a dark room, what do you notice? TODO(student): Try this experiment...",
  "session_id": "generated-or-provided-id",
  "provider": "claude",
  "mode": "learning"
}
```

## Deployment

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add API keys

# Run
uvicorn app.main:app --reload
```

**API Docs**: http://localhost:8000/docs

---
**v0 Scope**: Issues #1, #2, #3 only
**Timeline**: 1-2 weeks
**Goal**: Validate educational AI approach
