# 🍁 Grade 4 AI Tutor - Maple

An intelligent tutoring system for Ontario Grade 4 students, featuring adaptive AI-powered learning with curriculum alignment.

## 🎯 Project Overview

This AI tutor provides personalized educational support for Grade 4 students following the Ontario curriculum, with a focus on:
- Science & Technology (Light & Sound unit)
- Mathematics
- Language Arts
- Canadian cultural context

## 🏗️ Architecture

### Tech Stack
- **Frontend**: React 18 with TypeScript, Vite, Tailwind CSS
- **Backend**: Node.js with Express (planned)
- **AI**: Claude (learning mode) + OpenAI (study mode)
- **Content**: RAG system with curriculum database
- **Infrastructure**: Docker, n8n workflows

### Project Structure
```
ai_tutor/
├── packages/
│   └── web/              # React frontend application
├── docs/                 # Project documentation
│   ├── web_interface.md  # Frontend documentation
│   └── component_inventory.md  # Reusable components
└── README.md            # This file
```

## 📚 Documentation

- [Web Interface Documentation](docs/web_interface.md) - Frontend architecture and development
- [Component Inventory](docs/component_inventory.md) - Reusable UI components
- [GitHub Issues](https://github.com/stewmckendry/ai_tutor/issues) - Development tasks and roadmap

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Git for version control

### Development Setup

This project uses parallel development with git worktrees for concurrent feature development.

#### Frontend Development
```bash
# Navigate to web package
cd packages/web

# Install dependencies
npm install

# Start development server
npm run dev

# The app will be available at http://localhost:3000
```

#### Available Scripts
```bash
# From project root
npm run dev        # Start frontend dev server
npm run build      # Build for production
npm run preview    # Preview production build
npm run type-check # TypeScript validation
npm run lint       # Code linting
```

## 🎨 Current Implementation

### ✅ Completed Features (Issue #4 - Frontend)
- React chat interface with TypeScript
- Message display with user/AI distinction
- Typing indicators for AI responses
- TODO marker highlighting for learning objectives
- Session persistence with localStorage
- Mobile-responsive design
- Canadian-themed UI with Maple branding
- Error boundaries and loading states

### 🚧 In Progress
- Backend API development
- WebSocket real-time updates
- AI integration (Claude/OpenAI)
- Curriculum content database

## 📖 Development Epics

### Epic 1: Core v0 Implementation
- [x] Issue #4: Frontend chat interface
- [ ] Issue #5: Backend API
- [ ] Issue #6: AI integration
- [ ] Issue #7: Basic curriculum content

### Epic 2: Storytelling Enhancement
- [ ] Narrative-based learning modes
- [ ] Character development
- [ ] Interactive story elements

### Epic 3: Dynamic Content Generation
- [ ] Real-time Canadian content
- [ ] Location-based examples
- [ ] Current events integration

## 🤝 Contributing

### Development Workflow
1. Each feature stream has its own branch and worktree
2. Create feature branches from issue numbers (e.g., `issue-4-frontend`)
3. Follow component-based architecture
4. Update component inventory when adding new components
5. Maintain TypeScript types for all interfaces

### Code Standards
- TypeScript for type safety
- Functional React components with hooks
- Tailwind CSS for styling
- Comprehensive documentation
- Mobile-first responsive design

### Documentation Requirements
- Update component inventory for new components
- Document API endpoints and interfaces
- Include TypeScript type definitions
- Add inline code comments for complex logic

## 📄 License

MIT

## 🙏 Acknowledgments

- Ontario Ministry of Education for curriculum guidelines
- React and TypeScript communities
- Open source contributors
