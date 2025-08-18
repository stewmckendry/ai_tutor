# Backend API Documentation

FastAPI-based backend service for the Grade 4 AI Tutor system (Maple).

## Overview

The backend provides a RESTful API for AI-powered tutoring, supporting multiple AI providers (OpenAI and Anthropic), intelligent mode selection, and integration with Airtable for curriculum content. Built with FastAPI and Python 3.11, it features asynchronous processing, automatic provider failover, and session management.

## Architecture

### Tech Stack
- **FastAPI**: Modern async web framework with automatic OpenAPI docs
- **Python 3.11**: Latest stable Python with performance improvements
- **Pydantic**: Data validation and serialization
- **httpx**: Async HTTP client for AI provider APIs
- **pyairtable**: Airtable integration for curriculum data
- **PyYAML**: Externalized prompt configuration
- **uvicorn**: ASGI server for production deployment

### Key Design Decisions
1. **Dual AI provider support**: OpenAI and Anthropic with automatic failover
2. **Intelligent mode selection**: Keyword-based conversation mode detection
3. **Externalized prompts**: YAML-based prompt configuration for easy editing
4. **Async architecture**: Non-blocking I/O for scalability
5. **In-memory session storage**: Fast session management (Redis-ready)

## Features

### Core Functionality
- 🤖 Dual AI provider integration (OpenAI GPT-4, Anthropic Claude)
- 🎯 Intelligent mode selection based on conversation context
- 📚 Four distinct conversation modes (Learning, Explanatory, Story, Discovery)
- 📊 Airtable integration for curriculum content
- 💾 Session management with conversation history
- 🔄 Automatic provider failover for high availability
- ⚡ Asynchronous request processing
- 📝 Externalized prompt configuration via YAML

### AI Orchestration
- **Provider Selection**: Cost-optimized routing (Claude for learning, GPT-4 for technical)
- **Mode Detection**: Keyword analysis for automatic mode switching
- **Fallback Logic**: Seamless failover between providers
- **Context Management**: Full conversation history in prompts

## Development Setup

### Prerequisites
- Python 3.11+
- Virtual environment (venv or conda)
- API keys for OpenAI and/or Anthropic
- Airtable account (optional)

### Installation
```bash
# From project root
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
Create `.env` file in backend directory:
```env
# AI Provider Keys (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Airtable Configuration (required for content)
AIRTABLE_API_KEY=pat...  # Full Personal Access Token
AIRTABLE_BASE_ID=app...

# Server Configuration
PORT=8000
DEBUG=true
```

### Development Commands
```bash
# Start development server with hot reload
python -m uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Type checking (future)
mypy app

# Linting (future)
ruff check app
```

### Project Structure
```
backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application and routes
│   ├── config.py                # Environment configuration
│   ├── models.py                # Pydantic models
│   ├── prompts.py               # Prompt loading from YAML
│   ├── prompts.yaml             # Externalized prompts
│   ├── ai_orchestrator.py       # Provider selection logic
│   ├── session_manager.py       # Session storage
│   ├── claude_service.py        # Anthropic Claude integration
│   ├── openai_service.py        # OpenAI GPT integration
│   ├── airtable_service.py      # Curriculum content service
│   └── api/
│       └── content.py           # Content API endpoints
├── tests/
│   └── test_main.py             # Basic API tests
├── requirements.txt             # Python dependencies
├── test_prompts_yaml.py         # YAML prompt testing
└── PROMPTS_README.md           # Prompt configuration guide
```

## API Endpoints

### Chat Endpoint
```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "Can you help me understand how light works?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "force_provider": "claude",  // Optional: auto-selected if not provided
  "force_mode": "learning"  // Optional: auto-detected if not provided
}
```

**Response:**
```json
{
  "response": "Of course! I'm thrilled to dive into the world of light with you...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "provider": "claude",
  "mode": "learning",
  "has_activity": true,
  "activity_markers": null,
  "curriculum_content": {
    "topic": "Light",
    "learning_objectives": ["2.5 Investigate reflection of light"],
    "canadian_examples": ["Northern Lights in Yukon"]
  },
  "metadata": {
    "curriculum_topic": "light",
    "learning_objectives": ["2.5 Investigate reflection of light"],
    "canadian_examples": ["Northern Lights in Yukon", "Sunrise over Lake Ontario"],
    "suggested_activity": {
      "name": "Shadow Puppet Theatre",
      "description": "Create shadows using flashlights and objects"
    }
  },
  "timestamp": "2025-08-18T12:00:00Z"
}
```

### Health Check
```http
GET /api/health

Response:
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-08-18T12:00:00Z",
  "services": {
    "claude": true,
    "openai": true,
    "airtable": true
  }
}
```

### Content Endpoints
```http
GET /api/content/curriculum/topics?topic=light

Response:
[
  {
    "topic": "Light",
    "content": "Learn how light bounces off surfaces",
    "grade_level": "Grade 4",
    "learning_objectives": ["2.5 Investigate reflection of light"],
    "canadian_examples": ["Reflections on Canada's many lakes"]
  }
]
```

```http
GET /api/content/activities?topic=light

Response:
[
  {
    "name": "Shadow Puppet Theatre",
    "description": "Create shadows using flashlights and objects",
    "materials": ["Flashlight", "Paper", "Objects"],
    "learning_outcome": "Understanding how shadows are formed"
  }
]
```

```http
GET /api/content/canadian-examples?topic=light

Response:
[
  "Northern Lights in Yukon",
  "Sunrise over Lake Ontario",
  "Reflections on Lake Louise"
]
```

### Session Management
```http
GET /api/session/{session_id}

Response:
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [...],
  "created_at": "2024-01-01T00:00:00Z",
  "last_activity": "2024-01-01T00:30:00Z"
}
```

## Conversation Modes

### 1. **Learning Mode** (Socratic Method)
- Guides through questions rather than direct answers
- Encourages critical thinking
- Knowledge checks and mini-quizzes
- Best for: Deep understanding and exploration

### 2. **Explanatory Mode** (Direct Teaching)
- Clear, step-by-step explanations
- Uses analogies and examples
- Scaffolding technique for complexity
- Best for: When students are stuck or confused

### 3. **Story Mode** (Narrative Learning)
- Teaches through engaging stories
- Makes abstract concepts concrete
- Canadian contexts and characters
- Best for: Memorable learning experiences

### 4. **Discovery Mode** (Exploration)
- Encourages curiosity and wonder
- Open-ended exploration
- "What if" thinking
- Best for: Fostering natural interest

## Prompt Configuration

### YAML Structure
```yaml
base_prompt: |
  You are Maple, a friendly AI tutor...
  
modes:
  learning:
    name: "Socratic Learning Mode"
    description: "Guide through questions"
    prompt: |
      Socratic techniques here...
      
activity_prompt: |
  TODO: format for activities...
```

### Customization
1. Edit `app/prompts.yaml`
2. Changes load automatically in DEBUG mode
3. Otherwise, restart server
4. See `PROMPTS_README.md` for detailed guide

## AI Provider Integration

### OpenAI Service
- **Model**: GPT-4 Turbo (gpt-4-turbo-preview)
- **Strengths**: Clear explanations, step-by-step teaching, technical topics
- **Token Limit**: 1000 response tokens
- **Temperature**: 0.7 for creativity
- **Content Integration**: Incorporates activities and Canadian examples naturally

### Anthropic Service
- **Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **Strengths**: Socratic method, storytelling, empathy, discovery learning
- **Token Limit**: 1000 response tokens
- **Temperature**: 0.7 for natural conversation
- **Content Integration**: Naturally weaves curriculum content into responses

### Provider Selection Logic
```python
# Simplified decision tree
if mode == ConversationMode.EXPLANATORY:
    provider = AIProvider.OPENAI
elif mode in [ConversationMode.LEARNING, ConversationMode.DISCOVERY]:
    provider = AIProvider.CLAUDE
elif mode == ConversationMode.STORY:
    provider = AIProvider.CLAUDE if len(messages) < 10 else AIProvider.OPENAI
else:
    provider = AIProvider.CLAUDE  # Default

# Automatic failover if primary provider fails
```

## Testing Strategy

### Unit Tests
- Service layer testing
- Model validation
- Prompt loading
- Mode detection logic

### Integration Tests
- API endpoint testing
- Provider failover
- Session persistence
- Error handling

### Load Tests (Future)
- Concurrent request handling
- Provider rate limiting
- Memory management
- Response time targets

## Deployment Considerations

### Performance Targets
- **Response Time**: < 3s for AI responses
- **Throughput**: 100 concurrent sessions
- **Availability**: 99.9% uptime
- **Memory**: < 512MB per instance

### Security Considerations
- API key rotation
- Rate limiting per session
- Input sanitization
- CORS configuration
- Request validation

### Scalability
- Stateless design for horizontal scaling
- Redis-ready session management
- Connection pooling for providers
- Async processing throughout

## Error Handling

### Provider Failures
- Automatic failover to alternate provider
- Graceful degradation of features
- Error logging with context
- User-friendly error messages

### Rate Limiting
- Provider-specific rate limit handling
- Exponential backoff with retry
- Queue management for requests
- Circuit breaker pattern (future)

## Monitoring & Observability

### Logging
- Structured JSON logging
- Request/response tracking
- Provider usage metrics
- Error aggregation

### Metrics (Future)
- Response time percentiles
- Provider success rates
- Mode usage distribution
- Token consumption

### Health Checks
- Provider availability
- Database connectivity
- Memory usage
- Response time monitoring

## Future Enhancements

### Planned Features
- [ ] Redis session storage
- [ ] WebSocket support for streaming
- [ ] Multi-language support
- [ ] Parent/teacher dashboard API
- [ ] Progress tracking endpoints
- [ ] Content recommendation engine
- [ ] Voice transcription support
- [ ] Image analysis for homework help

### Technical Improvements
- [ ] Response streaming
- [ ] Provider load balancing
- [ ] Caching layer (Redis)
- [ ] GraphQL API option
- [ ] OpenAPI client generation
- [ ] Distributed tracing
- [ ] A/B testing framework
- [ ] ML-based mode detection

## Troubleshooting

### Common Issues

**API Key Errors**
- Verify keys in `.env` file
- Check key permissions/scopes
- Ensure billing is active

**Mode Detection Issues**
- Review keyword lists in ai_orchestrator.py
- Check prompt configuration
- Enable DEBUG logging

**Performance Issues**
- Monitor provider response times
- Check session storage size
- Review async implementation

### Debug Mode
Enable detailed logging:
```python
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG
```

## Contributing

### Code Style
- Follow PEP 8 guidelines
- Type hints for all functions
- Docstrings for public APIs
- Async/await for I/O operations
- Keep functions under 50 lines

### Testing Requirements
- Unit tests for new features
- Integration tests for endpoints
- Mock external services
- Maintain > 80% coverage

### Review Checklist
- [ ] Type hints complete
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Error handling implemented
- [ ] Performance acceptable
- [ ] Security reviewed

## API Documentation

### Interactive Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

### Postman Collection
Available in `docs/postman_collection.json` (future)

## Support

For issues or questions:
- GitHub Issues: https://github.com/stewmckendry/ai_tutor/issues
- Component inventory: docs/component_inventory.md
- Frontend documentation: docs/web_interface.md