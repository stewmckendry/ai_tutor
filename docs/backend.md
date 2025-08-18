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

# Airtable Configuration (optional)
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...
AIRTABLE_TABLE_NAME=Content

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
│   └── services/
│       ├── __init__.py
│       ├── claude_service.py    # Anthropic Claude integration
│       ├── openai_service.py    # OpenAI GPT integration
│       └── airtable_service.py  # Curriculum content
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
  "message": "Can you help me understand fractions?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "mode": "learning"  // Optional: auto-detected if not provided
}
```

**Response:**
```json
{
  "response": "I'd love to help you with fractions! 🍕 Let's start by thinking about something you know well. Have you ever shared a pizza with friends? When you cut a pizza into slices, you're actually creating fractions! What do you already know about fractions?",
  "mode": "learning",
  "provider": "anthropic",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "msg_123",
  "metadata": {
    "provider_used": "anthropic",
    "fallback_used": false,
    "mode_detected": "learning"
  }
}
```

### Health Check
```http
GET /api/health

Response:
{
  "status": "healthy",
  "providers": {
    "openai": true,
    "anthropic": true
  },
  "airtable": false,
  "version": "1.0.0"
}
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
- **Strengths**: Technical explanations, math, code
- **Token Limit**: 4096 response tokens
- **Temperature**: 0.7 for creativity

### Anthropic Service
- **Model**: Claude 3 Sonnet
- **Strengths**: Socratic method, storytelling, empathy
- **Token Limit**: 4096 response tokens
- **Temperature**: 0.7 for natural conversation

### Provider Selection Logic
```python
# Simplified decision tree
if "math" or "code" in message:
    use_openai()
elif mode == "learning" or mode == "story":
    use_anthropic()
else:
    use_anthropic()  # Default
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