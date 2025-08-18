# AI Tutor v0 - Deployment Guide

## 🚀 Quick Start

### Local Development
```bash
# 1. Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 2. Start both services
./start-dev.sh

# 3. Access the application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📦 Production Deployment

### Backend Deployment (Railway)

1. **Create Railway Account**
   - Sign up at [railway.app](https://railway.app)
   - Create new project

2. **Deploy from GitHub**
   ```bash
   # In Railway dashboard:
   # 1. Click "New Project"
   # 2. Select "Deploy from GitHub repo"
   # 3. Choose stewmckendry/ai_tutor
   # 4. Set root directory to /backend
   ```

3. **Configure Environment Variables**
   Add these in Railway dashboard:
   ```
   CLAUDE_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-...
   AIRTABLE_API_KEY=pat...
   AIRTABLE_BASE_ID=app...
   ALLOWED_ORIGINS=["https://your-frontend.vercel.app"]
   DEBUG=false
   ```

4. **Get Deployment URL**
   - Railway provides URL like: `https://ai-tutor-backend.up.railway.app`

### Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Sign up at [vercel.com](https://vercel.com)
   - Connect GitHub account

2. **Import Project**
   ```bash
   # Using Vercel CLI:
   cd packages/web
   npx vercel
   
   # Or via dashboard:
   # 1. Click "New Project"
   # 2. Import stewmckendry/ai_tutor
   # 3. Set root directory to packages/web
   ```

3. **Configure Environment Variables**
   Add in Vercel dashboard:
   ```
   VITE_API_URL=https://ai-tutor-backend.up.railway.app
   ```

4. **Deploy**
   - Vercel auto-deploys on push to main
   - Get URL like: `https://ai-tutor.vercel.app`

## 🔒 Production Checklist

### Security
- [ ] API keys secured in environment variables
- [ ] CORS configured for production domain only
- [ ] HTTPS enabled on both frontend and backend
- [ ] Debug mode disabled in production
- [ ] Rate limiting configured (future)

### Testing
- [ ] Health endpoint responding
- [ ] Chat endpoint working with real AI providers
- [ ] Session persistence verified
- [ ] Mobile responsiveness tested
- [ ] Error handling working

### Monitoring
- [ ] Backend logs accessible (Railway dashboard)
- [ ] Frontend analytics (Vercel Analytics)
- [ ] Error tracking configured (future: Sentry)
- [ ] Uptime monitoring (future: UptimeRobot)

## 🎓 Student Testing Setup

### Test Environment URLs
- Production: `https://ai-tutor.vercel.app`
- Staging: `https://ai-tutor-staging.vercel.app` (optional)

### Pre-Testing Checklist
1. **Technical Readiness**
   - [ ] Both services deployed and accessible
   - [ ] AI providers have sufficient credits
   - [ ] Airtable content populated
   - [ ] Mobile devices tested

2. **Content Readiness**
   - [ ] Grade 4 curriculum content loaded
   - [ ] Canadian examples configured
   - [ ] Activity templates with TODOs ready
   - [ ] Age-appropriate responses verified

3. **Testing Protocol**
   - [ ] Consent forms prepared
   - [ ] Testing script ready
   - [ ] Feedback forms created
   - [ ] Screen recording setup (optional)

## 🔧 Troubleshooting

### Backend Issues

**API Keys Invalid**
```bash
# Test locally first
cd backend
python test_api.py
```

**CORS Errors**
- Verify ALLOWED_ORIGINS includes frontend URL
- Check URL format (no trailing slash)

**Railway Deploy Fails**
- Check Python version (3.11+)
- Verify requirements.txt
- Check build logs in Railway dashboard

### Frontend Issues

**API Connection Failed**
- Verify VITE_API_URL is correct
- Check backend is running
- Test with curl: `curl https://your-backend/health`

**Build Errors**
- Clear node_modules and reinstall
- Check Node version (18+)
- Verify all TypeScript types

### Quick Fixes

```bash
# Backend not starting
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend not building
cd packages/web
rm -rf node_modules package-lock.json
npm install
npm run build

# Test API endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'
```

## 📊 Success Metrics

### Technical Metrics
- [ ] < 2s average response time
- [ ] 99%+ uptime
- [ ] Zero critical errors in first 24h
- [ ] Successful API calls > 95%

### Educational Metrics
- [ ] 80%+ session completion rate
- [ ] 90%+ message comprehension
- [ ] 70%+ TODO activity engagement
- [ ] 60%+ positive feedback

## 🚨 Emergency Contacts

- **Technical Issues**: [Create GitHub Issue](https://github.com/stewmckendry/ai_tutor/issues)
- **Railway Support**: support@railway.app
- **Vercel Support**: support@vercel.com

## 📝 Post-Deployment

1. **Monitor First 24 Hours**
   - Check logs frequently
   - Monitor API usage
   - Track error rates

2. **Gather Feedback**
   - Student testing sessions
   - Teacher evaluations
   - Technical performance data

3. **Iterate**
   - Fix critical bugs immediately
   - Plan v1 improvements
   - Document lessons learned