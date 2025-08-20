# 🍁 Maple - Grade 4 AI Tutor (v0)

> A minimal viable AI tutor for Ontario Grade 4 students using Python FastAPI + Airtable. Focus: **Ship fast, validate with real students, iterate.**

[![Python](https://img.shields.io/badge/Backend-Python%20FastAPI-blue.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-blue.svg)](https://reactjs.org/)
[![Airtable](https://img.shields.io/badge/Content-Airtable-yellow.svg)](https://airtable.com/)
[![Grade Level](https://img.shields.io/badge/Grade-4-blue.svg)](https://www.ontario.ca/curriculum)

## 🎯 **v0 Vision: Validate Educational AI**

**Goal**: Build the simplest possible AI tutor that can intelligently help Grade 4 students learn about **Light & Sound** using Canadian examples. Test with real students to validate the approach.

### **What v0 Proves**
- ✅ Students engage with AI-guided discovery learning
- ✅ Dual AI orchestration (Claude + OpenAI) improves outcomes  
- ✅ Canadian curriculum content enhances relevance
- ✅ TODO activities drive hands-on learning

### **What v0 Doesn't Include (Yet)**
- ❌ User accounts or authentication
- ❌ Complex analytics or dashboards
- ❌ Multiple subjects beyond Science & Technology
- ❌ Advanced features (voice, AR, gamification)

## 👥 **Meet Emma - Our Test User**

Emma is 9 years old, in Grade 4 in Toronto. She's learning about light and sound in science class.

**Emma's v0 Journey:**
```
Emma: "I need help with light and sound"

Maple: "Hi Emma! I'm Maple 🍁, your science buddy from Canada! 
Let's be light detectives. Can you find 3 things in your room that make light?"

Emma: "My lamp, my iPad, and the window"

Maple: "Great detective work! Now here's a puzzle - do you think 
your iPad MAKES light or just shows light from somewhere else?

TODO(student): Turn your iPad off and on. Does it glow in the dark?"

Emma: "It glows! So it makes its own light!"

Maple: "Exactly! Your iPad has tiny LEDs that change electrical energy 
into light energy. Just like the CN Tower lights in Toronto! 🏙️"
```

## 🔄 **n8n Content Pipeline (NEW)**

### Dynamic Content Generation
- **Status**: ✅ **POC Working** (Issue #18 Complete)
- **Location**: `/n8n` directory  
- **Purpose**: Automated pipeline to fetch Canadian weather data and transform it into Grade 4 educational content
- **Features**: Weather → AI enrichment → Airtable storage, hourly schedule, Grade 4 curriculum alignment

### Quick Start
```bash
cd n8n
./setup.sh  # Start n8n with Docker
# Access at http://localhost:5678
```

See [n8n README](n8n/README.md) for full setup instructions.

## 🎨 **Current Implementation Status**

### ✅ **Completed: Full Integration (Issue #1d)**
- **Frontend-Backend Integration** - React app connected to FastAPI backend
- **Airtable Content Integration** - Curriculum content naturally woven into AI responses
- **Topic Pills** - Quick access buttons for Grade 4 science topics
- **Natural Content Weaving** - Canadian examples and activities integrated conversationally
- **Session Management** - Persistent sessions with conversation history
- **Metadata Responses** - Structured curriculum data returned with chat responses

### ✅ **Completed: Backend AI Orchestration (Issue #5)**
- **FastAPI with Python 3.11** - Modern async framework with automatic API docs
- **Dual AI Provider Support** - OpenAI GPT-4 and Anthropic Claude 3
- **Intelligent Mode Selection** - Four conversation modes with keyword detection
- **YAML Prompt Configuration** - Externalized, editable prompts
- **Features**:
  - Automatic provider failover for high availability
  - Session management with conversation history
  - Cost-optimized provider routing
  - TODO activity generation
  - Canadian curriculum integration via Airtable
  - Error handling and graceful degradation

### ✅ **Completed: Frontend Chat Interface (Issue #4)**
- **React 18 with TypeScript** - Modern, type-safe development
- **Vite Build System** - Fast development and optimized builds  
- **Tailwind CSS** - Responsive, Canadian-themed design
- **Chat Features**:
  - Message display with user/AI distinction
  - Loading states for AI responses
  - Activity and example integration in responses
  - Session persistence with localStorage
  - Mobile-responsive layout
  - Topic pills for quick subject selection
  - Error boundaries and graceful handling
- **API Integration**:
  - Centralized API service layer
  - Type-safe request/response handling
  - Real-time backend communication

### ✅ **Completed: Airtable Curriculum Content (Issue #6)**
- **Structured Database** - 6 interconnected tables for curriculum data
- **Ontario Grade 4 Science** - Complete Light & Sound units
- **Canadian Context** - 27 Canadian examples from all provinces/territories
- **Hands-on Activities** - 16 activities naturally suggested in conversations
- **Story Characters** - 8 Canadian animal characters for narrative mode
- **Integration Features**:
  - Content fetched automatically when topics detected
  - Natural weaving into AI responses
  - Canadian examples incorporated conversationally
  - Activities suggested as part of learning flow
  - Full authentication with PAT tokens
  - Content APIs exposed and functional

### ✅ **Completed: n8n Content Pipeline (Issue #18)**
- **Automated Content Generation** - Weather data transformed into Grade 4 educational content
- **Canadian Weather Integration** - Real-time data from Environment Canada (Toronto, Vancouver)
- **AI Content Enrichment** - OpenAI GPT-3.5 creates curriculum-aligned educational content
- **Airtable Storage** - Generated content stored in Maple_Grade4_Science base
- **Scheduling & Monitoring** - Hourly execution with comprehensive error handling
- **Pipeline Features**:
  - Weather RSS feed parsing with error handling
  - Grade 4 appropriate content generation with Canadian spelling
  - Science curriculum connections (light, sound, energy concepts)
  - Hands-on activity suggestions integrated into content
  - Quality validation and monitoring tools included
  - Docker-based n8n deployment for reliability

## 🏗️ **v0 Technical Architecture** 

### **Enhanced Stack with Content Pipeline**
```
┌─────────────────┐    HTTPS     ┌──────────────────┐    API      ┌─────────────────┐
│   React Chat    │─────────────▶│ Python FastAPI   │────────────▶│ Claude/OpenAI   │
│   (Vercel)      │              │   (Railway)      │             │    APIs         │
└─────────────────┘              └──────────────────┘             └─────────────────┘
         │                                 │                               │
         │ localStorage                    │ Curriculum API                │
         ▼                                 ▼                               │
┌─────────────────┐              ┌──────────────────┐                     │
│   Session Data  │              │    Airtable      │◀────────────────────┘
│   (Browser)     │              │   (Curriculum +  │                      
└─────────────────┘              │   Dynamic Content│                      
                                 └──────────────────┘                      
                                          ▲                                
                                          │ Generated Content              
                                          │                                
                                 ┌──────────────────┐    Weather    ┌─────────────────┐
                                 │   n8n Pipeline   │─────────────▶│ Environment     │
                                 │   (Docker)       │              │ Canada RSS      │
                                 └──────────────────┘              └─────────────────┘
```

### **Core Components**

#### **Frontend (React)**
- Single chat page with TODO highlighting
- Session persistence in localStorage 
- Mobile responsive design
- Canadian maple leaf branding

#### **Backend (Python FastAPI)** 
- `POST /api/chat/message` - Main chat endpoint with content integration
- `GET /api/content/*` - Content endpoints for curriculum, activities, examples
- AI orchestration: Claude (learning/discovery) vs OpenAI (explanatory)
- Natural content weaving in AI responses
- Session management with conversation history
- Automatic topic extraction and content fetching

#### **Content (Airtable)**
- Ontario Grade 4 Science & Technology curriculum
- Canadian examples (CN Tower, Northern Lights, hockey arenas)
- Activity templates with TODO markers
- Story characters for narrative mode

#### **Content Pipeline (n8n)**
- Automated weather data fetching from Environment Canada
- AI content enrichment with OpenAI GPT-3.5
- Grade 4 curriculum-aligned content generation
- Hourly scheduled execution with error handling
- Direct integration with Airtable for content storage

## 🚀 **Quick Start**

### **Prerequisites**
```bash
Python 3.11+
Node.js 18+
API Keys: Claude, OpenAI, Airtable
```

### **Backend Setup**
```bash
cd backend/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your API keys to .env

# Run development server
uvicorn app.main:app --reload

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### **Frontend Setup** 
```bash
cd frontend/

# Install dependencies
npm install

# Configure API endpoint
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Run development server
npm start

# App available at http://localhost:3000
```

### **n8n Content Pipeline Setup (Optional)**
```bash
cd n8n/

# Start n8n with Docker
./setup.sh

# Access n8n at http://localhost:5678
# Import workflow: workflows/weather_to_education_poc.json
# Add API credentials (OpenAI + Airtable)
# Enable hourly schedule for automated content generation
```

## 📚 **Current Content (Light & Sound Unit)**

### **Curriculum Covered**
- **Ontario Expectation 2.1**: Assess uses of light and sound in society and the environment
- **Ontario Expectation 2.2**: Investigate characteristics and properties of light and sound
- **Ontario Expectation 2.3**: Demonstrate understanding of light and sound concepts

### **Canadian Examples**
- **Light**: CN Tower LEDs, Northern Lights, lighthouse technology
- **Sound**: Hockey arena acoustics, Thunder Bay weather warnings
- **Activities**: Shadow tracking, echo experiments, light source investigation

### **TODO Activities**
```
TODO(student): Find 5 light sources in your home and sort them into 
"natural" and "artificial" categories.

TODO(student): Stand outside and trace your shadow with chalk. 
Check again in 2 hours - what changed?

TODO(student): Clap your hands in a big room, then in a closet. 
Which echo is louder?
```

## 🎯 **v0 Development Plan**

### **Week 1: Core Infrastructure**
- [x] **Issue #4**: React chat interface ✅ COMPLETED
- [x] **Issue #5**: Python FastAPI backend ✅ COMPLETED
- [x] **Issue #6**: Airtable curriculum content ✅ COMPLETED

### **Week 2: Integration & Testing**
- [ ] **Issue #7**: Integration & deployment (2-3 days)
- [ ] **Student Testing**: 5-8 Grade 4 students (2 days)
- [ ] **Iteration**: Fix issues, deploy to production

### **Success Criteria**
- [ ] 5+ Grade 4 students complete 15-minute learning sessions
- [ ] 80%+ say "Maple helped me learn"
- [ ] 70%+ try the TODO activities
- [ ] System handles 10 concurrent conversations
- [ ] Response time < 3 seconds average

## 📊 **What Happens After v0**

### **If v0 Succeeds**
- 🚀 **Build v1**: Add storytelling mode, more subjects
- 📈 **Scale**: Multi-grade, teacher dashboard, analytics
- 🍁 **Enhance**: Dynamic Canadian content, voice interaction

### **If v0 Needs Iteration**
- 🔄 **Fix core issues** identified by student testing
- 🎯 **Simplify further** if students find it confusing
- 📚 **Adjust content** based on curriculum feedback

## 🧪 **Testing with Real Students**

### **Our Testing Protocol**
1. **Recruit**: 5-8 Grade 4 students (diverse backgrounds)
2. **Session**: 15-20 minutes supervised by parent/teacher
3. **Observe**: Do they understand? Do they engage with TODOs?
4. **Feedback**: "Was Maple helpful? Fun? Confusing?"
5. **Iterate**: Fix issues, improve content, deploy fixes

### **What We're Measuring**
- **Comprehension**: Do students understand Maple's responses?
- **Engagement**: Do they ask follow-up questions?
- **Activity Completion**: Do they try the TODO tasks?
- **Learning**: Can they explain concepts after the session?

## 📂 **Repository Structure**

```
ai_tutor/
├── backend/                 # Python FastAPI backend ✅ COMPLETED
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── ai_orchestrator.py  # Claude + OpenAI routing
│   │   ├── airtable_service.py  # Curriculum content
│   │   └── models.py       # Request/response models
│   ├── requirements.txt    # 8 core dependencies
│   └── .env.example       # API keys template
├── packages/
│   └── web/                # React frontend application ✅ COMPLETED
│       ├── src/            # Source code with components
│       ├── public/         # Static assets
│       └── package.json    # Frontend dependencies
├── content/                # Curriculum data ✅ COMPLETED
│   ├── curriculum_data.json    # 14 curriculum topics
│   ├── activity_templates.json # 16 hands-on activities
│   ├── canadian_examples.json  # 27 Canadian examples
│   └── story_characters.json   # 8 narrative characters
├── docs/
│   ├── backend.md         # Backend API documentation
│   ├── web_interface.md   # Frontend documentation
│   ├── curriculum_content.md # Content documentation
│   └── component_inventory.md  # Reusable components
└── README.md              # This file
```

## 🤝 **Contributing to v0**

### **Current Focus Areas**
- **Backend Development**: Python FastAPI implementation
- **Content Creation**: Airtable curriculum database
- **Frontend Development**: React chat interface
- **Student Testing**: Recruiting Grade 4 volunteers

### **GitHub Issues**
- [**Issue #1**](https://github.com/stewmckendry/ai_tutor/issues/1): Core v0 Implementation
- [**Issue #4**](https://github.com/stewmckendry/ai_tutor/issues/4): React Chat Interface
- [**Issue #5**](https://github.com/stewmckendry/ai_tutor/issues/5): Python FastAPI Backend
- [**Issue #6**](https://github.com/stewmckendry/ai_tutor/issues/6): Airtable Curriculum Content
- [**Issue #7**](https://github.com/stewmckendry/ai_tutor/issues/7): Integration & Deployment

## 📞 **Contact & Feedback**

- **Project Lead**: Stew McKendry [@stewmckendry](https://github.com/stewmckendry)
- **Issues**: [GitHub Issues](https://github.com/stewmckendry/ai_tutor/issues)
- **Student Testing**: Email if you have Grade 4 students who'd like to help test!

## 📄 **License**

MIT License - See [LICENSE](LICENSE) file for details.

---

<div align="center">

**v0 Status: 🚧 Active Development**

*Goal: Real Grade 4 students learning with Maple within 2 weeks* 🍁

**Remember: Ship fast → Test with students → Learn → Iterate**

</div>
