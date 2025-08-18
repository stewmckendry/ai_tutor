# Web Interface Documentation

React-based chat interface for the Grade 4 AI Tutor system (Maple).

## Overview

The web interface provides a child-friendly chat experience for Grade 4 students to interact with the AI tutor. Built with React 18 and TypeScript, it features real-time messaging, session persistence, and mobile responsiveness.

## Architecture

### Tech Stack
- **React 18**: Component-based UI framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tooling and HMR
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client for API calls
- **localStorage**: Client-side session persistence

### Key Design Decisions
1. **Component-based architecture**: Reusable, testable components
2. **TypeScript interfaces**: Strong typing for message and session data
3. **Tailwind utilities**: Consistent styling without CSS modules
4. **Local persistence**: Sessions survive page refreshes
5. **Error boundaries**: Graceful error handling for production

## Features

### Core Functionality
- 💬 Real-time chat interface with AI tutor
- 🎓 Topic pills for quick subject selection
- 📝 Activity and example integration in responses
- 💾 Session persistence with localStorage
- 📱 Mobile-responsive design
- ⌨️ Loading states for AI responses
- 🍁 Canadian-themed UI with Maple branding
- 📊 Metadata display for curriculum content

### User Experience
- **Auto-scrolling**: Always shows latest message
- **Message timestamps**: Track conversation flow
- **Typing indicators**: Visual feedback during AI processing
- **Session management**: Start new sessions while preserving history
- **Error recovery**: Graceful handling of failures

## Development Setup

### Prerequisites
- Node.js 18+ and npm
- Git for version control

### Installation
```bash
# From project root
cd packages/web
npm install
```

### Development Commands
```bash
# Start development server (port 5173 with Vite)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint
```

### Project Structure
```
packages/web/
├── public/              # Static assets
│   └── maple-leaf.svg   # App icon
├── src/
│   ├── components/      # React components
│   │   ├── ChatInterface.tsx    # Main chat container
│   │   ├── Header.tsx           # Navigation header
│   │   ├── MessageInput.tsx     # Message input area
│   │   ├── MessageItem.tsx      # Individual message
│   │   ├── MessageList.tsx      # Message container
│   │   ├── TopicPills.tsx       # Quick topic buttons
│   │   ├── ErrorBoundary.tsx    # Error handling
│   │   └── Loading.tsx          # Loading states
│   ├── services/        # API integration
│   │   └── api.ts        # Backend communication
│   ├── types/           # TypeScript definitions
│   │   └── chat.ts      # Message/Session types
│   ├── App.tsx          # Main application
│   ├── main.tsx         # Entry point
│   ├── index.css        # Global styles
│   └── vite-env.d.ts    # Vite types
```

## Component Architecture

### Data Flow
```
App.tsx (Session Management)
    ├── Header.tsx (Navigation)
    └── ChatInterface.tsx (Chat Container)
        ├── TopicPills.tsx (Quick Topics)
        ├── MessageList.tsx (Message Display)
        │   └── MessageItem.tsx (Individual Messages)
        └── MessageInput.tsx (User Input)
```

### State Management
- **Session state**: Managed in App.tsx
- **Messages**: Array of Message objects
- **Persistence**: Auto-save to localStorage on changes
- **Loading states**: Managed per component

### Type System
```typescript
interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  metadata?: {
    provider?: 'claude' | 'openai';
    mode?: 'learning' | 'explanatory' | 'story' | 'discovery';
    curriculum_topic?: string;
    learning_objectives?: string[];
    canadian_examples?: string[];
    suggested_activity?: Activity;
  };
}

interface ChatResponse {
  response: string;
  session_id: string;
  provider: string;
  mode: string;
  has_activity: boolean;
  activity_markers: string[] | null;
  curriculum_content: any;
  metadata: any;
  timestamp: string;
}
```

## API Integration

### Environment Variables
```env
# Backend API endpoint
VITE_API_URL=http://localhost:8000

# Feature flags (future)
VITE_ENABLE_VOICE=false
VITE_ENABLE_ANALYTICS=false
```

### Backend Integration Points
1. **Chat API**: POST /api/chat/message
2. **Session API**: GET /api/session/{session_id}
3. **Health Check**: GET /api/health
4. **Content APIs**: 
   - GET /api/content/curriculum/topics
   - GET /api/content/activities
   - GET /api/content/canadian-examples

### API Service Layer
The app uses a centralized API service (`services/api.ts`):
- Axios for HTTP requests
- Type-safe request/response handling
- Error handling and retry logic
- Session ID management
- CORS configuration

## Testing Strategy

### Unit Tests (TODO)
- Component rendering tests
- User interaction tests
- State management tests
- Error boundary tests

### Integration Tests (TODO)
- Message flow testing
- Session persistence
- WebSocket connection
- API integration

### E2E Tests (TODO)
- Full conversation flows
- Session management
- Error recovery
- Mobile responsiveness

## Deployment Considerations

### Build Optimization
- Tree shaking with Vite
- Code splitting for lazy loading
- Asset optimization
- Minification for production

### Performance Targets
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Bundle size**: < 200KB gzipped
- **Lighthouse score**: > 90

### Security Considerations
- Content Security Policy headers
- XSS prevention via React
- Sanitized user inputs
- Secure WebSocket connections
- localStorage encryption for sensitive data

## Accessibility

### Current Support
- Semantic HTML structure
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus management

### Future Enhancements
- Screen reader optimization
- High contrast mode
- Keyboard shortcuts
- Voice input/output
- Adjustable font sizes

## Mobile Considerations

### Responsive Design
- Flexbox layouts
- Touch-friendly tap targets (44px minimum)
- Viewport meta tag configuration
- Adaptive message display

### Performance
- Optimized for 3G connections
- Progressive enhancement
- Offline support (future)

## Future Enhancements

### Planned Features
- [ ] Multiple session history with browser
- [ ] Rich message formatting (markdown, LaTeX)
- [ ] File attachments for homework help
- [ ] Voice input/output integration
- [ ] Student progress dashboard
- [ ] Parent/teacher view modes
- [ ] Offline mode with service workers
- [ ] Dark mode support

### Technical Improvements
- [ ] Redux/Zustand for complex state
- [ ] React Query for API caching
- [ ] Progressive Web App features
- [ ] Internationalization (i18n)
- [ ] Analytics integration
- [ ] Performance monitoring

## Troubleshooting

### Common Issues

**Build Errors**
- Clear node_modules and reinstall
- Check Node.js version (18+ required)
- Verify TypeScript configuration

**Style Issues**
- Ensure Tailwind CSS is properly configured
- Check PostCSS configuration
- Clear browser cache

**State Issues**
- Clear localStorage if corrupted
- Check browser console for errors
- Verify session data structure

### Debug Mode
Enable debug logging:
```javascript
localStorage.setItem('debug', 'true');
```

## Contributing

### Code Style
- Follow existing TypeScript patterns
- Use functional components with hooks
- Maintain single responsibility principle
- Add TypeScript types for all props
- Keep components under 200 lines

### Git Workflow
1. Create feature branch from issue number
2. Make atomic commits
3. Update component inventory
4. Add tests for new features
5. Update documentation

### Review Checklist
- [ ] TypeScript types complete
- [ ] No console errors/warnings
- [ ] Mobile responsive
- [ ] Accessibility checked
- [ ] Performance acceptable
- [ ] Documentation updated

## Support

For issues or questions:
- GitHub Issues: https://github.com/stewmckendry/ai_tutor/issues
- Component inventory: docs/component_inventory.md
- Project documentation: README.md