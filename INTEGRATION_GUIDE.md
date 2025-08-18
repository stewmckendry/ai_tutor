# 🔗 AI Tutor v0 - Integration Guide

## ✅ Integration Status

### Completed Components
- ✅ Backend API with FastAPI
- ✅ Frontend React chat interface  
- ✅ API integration (frontend ↔ backend)
- ✅ CORS configuration
- ✅ Environment variable setup
- ✅ Error handling in frontend
- ✅ Deployment configurations (Vercel + Railway)
- ✅ Student testing protocol
- ✅ Development startup script

### Pending Tasks
- ⏳ Airtable content verification
- ⏳ End-to-end testing with real API keys
- ⏳ Production deployment
- ⏳ Domain/SSL setup
- ⏳ Student testing execution

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- API Keys: OpenAI, Claude (Anthropic), Airtable

### 1. Clone & Setup
```bash
git clone https://github.com/stewmckendry/ai_tutor.git
cd ai_tutor
git checkout issue-1d-integration
```

### 2. Configure Environment

**Backend (.env)**
```bash
cd backend
cp .env.example .env
# Edit .env with your actual API keys:
# - CLAUDE_API_KEY=sk-ant-...
# - OPENAI_API_KEY=sk-...
# - AIRTABLE_API_KEY=pat...
# - AIRTABLE_BASE_ID=app...
```

**Frontend (.env)**
```bash
cd ../packages/web
echo "VITE_API_URL=http://localhost:8000" > .env
```

### 3. Start Development
```bash
# From project root
./start-dev.sh

# Or manually:
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd packages/web
npm install
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🏗️ Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React App     │────▶│  FastAPI Backend │────▶│   AI Providers  │
│   (Vercel)      │◀────│    (Railway)     │◀────│ Claude/OpenAI   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │    Airtable     │
                        │  (Curriculum)   │
                        └─────────────────┘
```

## 📝 API Endpoints

### Core Endpoints
- `POST /api/chat/message` - Send message and get AI response
- `GET /api/session/{id}` - Retrieve session history
- `GET /health` - Health check

### Request/Response Format
```typescript
// Request
{
  "message": "How does light travel?",
  "session_id": "optional-session-id"
}

// Response
{
  "response": "Great question! Light travels in straight lines...",
  "session_id": "generated-session-id",
  "provider": "claude",
  "mode": "learning",
  "metadata": {
    "todos": ["Try this experiment..."],
    "curriculum_topic": "Light and Sound"
  }
}
```

## 🧪 Testing

### API Testing
```bash
# Run test script
cd backend
python test_api.py

# Manual testing with curl
curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Maple!", "session_id": "test"}'
```

### Frontend Testing
1. Open http://localhost:5173
2. Send a test message
3. Verify response appears
4. Check browser console for errors
5. Test TODO markers
6. Test session persistence (refresh page)

## 🚢 Deployment

### Frontend (Vercel)
```bash
cd packages/web
npx vercel

# Follow prompts:
# - Set root directory: packages/web
# - Add env var: VITE_API_URL=https://your-backend.railway.app
```

### Backend (Railway)
```bash
# Via Railway CLI
railway login
railway link
railway up

# Or via Dashboard:
# 1. Connect GitHub repo
# 2. Set root directory: /backend
# 3. Add environment variables
```

### Environment Variables (Production)

**Railway (Backend)**
```
CLAUDE_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...
ALLOWED_ORIGINS=["https://your-app.vercel.app"]
DEBUG=false
```

**Vercel (Frontend)**
```
VITE_API_URL=https://your-backend.railway.app
```

## 🔍 Troubleshooting

### Common Issues

**CORS Error**
- Check ALLOWED_ORIGINS in backend .env
- Ensure frontend URL is included
- No trailing slashes in URLs

**API Connection Failed**
- Verify backend is running: `curl http://localhost:8000/health`
- Check VITE_API_URL in frontend
- Look for console errors

**AI Provider Errors**
- Verify API keys are correct
- Check API credit/quotas
- Look at backend logs for details

**Session Not Persisting**
- Check localStorage in browser
- Verify session_id is being sent
- Check backend session manager

### Debug Commands
```bash
# Check backend logs
docker logs ai-tutor-backend

# Test Airtable connection
python -c "from app.airtable_service import AirtableService; s = AirtableService(); print(s.test_connection())"

# Check frontend build
cd packages/web
npm run build

# Verify environment variables
python -c "from app.config import settings; print(settings.dict())"
```

## 📊 Success Metrics

### Technical
- [ ] Response time < 2 seconds
- [ ] Error rate < 5%
- [ ] Session persistence working
- [ ] Mobile responsive

### Educational
- [ ] Age-appropriate responses
- [ ] TODO markers functioning
- [ ] Canadian content included
- [ ] Curriculum alignment verified

## 📚 Documentation

- [Deployment Guide](./DEPLOYMENT.md)
- [Student Testing Protocol](./STUDENT_TESTING_PROTOCOL.md)
- [Backend Documentation](./docs/backend.md)
- [Frontend Documentation](./docs/web_interface.md)
- [API Documentation](http://localhost:8000/docs)

## 🤝 Contributing

### Development Workflow
1. Create feature branch from `main`
2. Make changes
3. Test locally with `./start-dev.sh`
4. Run API tests: `python backend/test_api.py`
5. Create PR with description
6. Await review and merge

### Code Standards
- Python: Follow PEP 8
- TypeScript: Use ESLint config
- Commits: Conventional commits
- Documentation: Update relevant docs

## 🆘 Support

- **GitHub Issues**: [Create Issue](https://github.com/stewmckendry/ai_tutor/issues)
- **Documentation**: Check `/docs` folder
- **API Docs**: http://localhost:8000/docs when running locally

## 📅 Next Steps

1. **Immediate** (Before Student Testing)
   - [ ] Add real API keys to .env
   - [ ] Populate Airtable with curriculum content
   - [ ] Deploy to production
   - [ ] Test with real devices

2. **Short-term** (After v0 Testing)
   - [ ] Implement authentication
   - [ ] Add progress tracking
   - [ ] Enhance TODO features
   - [ ] Add more curriculum content

3. **Long-term** (v1 and beyond)
   - [ ] Parent dashboard
   - [ ] Teacher tools
   - [ ] Offline mode
   - [ ] Multi-language support