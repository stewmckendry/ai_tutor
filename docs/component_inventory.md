# Component Inventory

## Overview

This inventory catalogs all reusable components in the AI Tutor project. Each component is documented with its purpose, location, and usage patterns to ensure consistency and reusability across the application.

**Last Updated**: Issue #6 - Airtable Curriculum Content

---

## 🎨 Layout Components

### Header
**Path**: `packages/web/src/components/Header.tsx`  
**Purpose**: Application header with branding, navigation, and session controls  
**Props**:
- `isConnected: boolean` - Connection status indicator
- `onNewSession: () => void` - New session handler
- `sessionTitle?: string` - Current session title

**Features**:
- Maple logo and branding
- Connection status indicator
- New session button
- Responsive layout

**Usage**:
```tsx
<Header 
  isConnected={true}
  onNewSession={handleNewSession}
  sessionTitle="Learning Session"
/>
```

---

## 💬 Chat Components

### ChatInterface
**Path**: `packages/web/src/components/ChatInterface.tsx`  
**Purpose**: Main chat container managing message display and input  
**Props**:
- `messages: Message[]` - Array of chat messages
- `onSendMessage: (content: string) => void` - Message send handler

**Features**:
- Auto-scrolling message list
- Message input area
- Responsive height management

**Usage**:
```tsx
<ChatInterface
  messages={session.messages}
  onSendMessage={handleSendMessage}
/>
```

### MessageList
**Path**: `packages/web/src/components/MessageList.tsx`  
**Purpose**: Container for displaying message items  
**Props**:
- `messages: Message[]` - Array of messages to display

**Features**:
- Vertical message layout
- Consistent spacing

**Usage**:
```tsx
<MessageList messages={messages} />
```

### MessageItem
**Path**: `packages/web/src/components/MessageItem.tsx`  
**Purpose**: Individual message display with role-based styling  
**Props**:
- `message: Message` - Single message object

**Features**:
- User/assistant message distinction
- Typing indicators
- TODO marker highlighting
- Timestamp display
- Responsive width

**Sub-components**:
- `TypingIndicator` - Animated dots for AI thinking
- `TodoMarkers` - Learning task display

**Usage**:
```tsx
<MessageItem message={messageObject} />
```

### MessageInput
**Path**: `packages/web/src/components/MessageInput.tsx`  
**Purpose**: Text input area for user messages  
**Props**:
- `onSendMessage: (content: string) => void` - Message submission handler

**Features**:
- Auto-resizing textarea
- Enter to send (Shift+Enter for new line)
- Send button with disabled state
- Mobile-friendly design

**Sub-components**:
- `SendIcon` - SVG send button icon

**Usage**:
```tsx
<MessageInput onSendMessage={handleSendMessage} />
```

---

## 🛡️ Error & Loading Components

### ErrorBoundary
**Path**: `packages/web/src/components/ErrorBoundary.tsx`  
**Purpose**: React error boundary for graceful error handling  
**Props**:
- `children: ReactNode` - Child components to protect
- `fallback?: ReactNode` - Custom error UI (optional)

**Features**:
- Catches React component errors
- Displays user-friendly error message
- Page refresh option
- Debug details in development

**Usage**:
```tsx
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### Loading
**Path**: `packages/web/src/components/Loading.tsx`  
**Purpose**: Loading state indicator  
**Props**:
- `message?: string` - Loading message (default: "Loading...")

**Features**:
- Centered loading display
- Animated maple leaf icon
- Bouncing dots animation
- Custom message support

**Usage**:
```tsx
<Loading message="Initializing Maple..." />
```

---

## 📦 Type Definitions

### Chat Types
**Path**: `packages/web/src/types/chat.ts`  
**Purpose**: TypeScript interfaces for chat data structures

**Interfaces**:
```typescript
interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  metadata?: {
    isTyping?: boolean;
    hasTodo?: boolean;
    todoItems?: string[];
    error?: string;
  };
}

interface ChatSession {
  id: string;
  messages: Message[];
  startedAt: Date;
  lastActivityAt: Date;
  title?: string;
}

interface TodoMarker {
  id: string;
  text: string;
  completed: boolean;
  messageId: string;
}
```

---

## 🎨 Design System

### Color Palette (Tailwind Config)
**Path**: `packages/web/tailwind.config.js`

**Primary Colors (Maple Theme)**:
- `maple-50` to `maple-900` - Red color scale
- Based on Canadian flag red (#dc2626)

**Usage**:
```css
bg-maple-500    /* Primary buttons */
hover:bg-maple-600  /* Hover states */
text-maple-100  /* Light text on maple background */
```

### Typography
- **Font**: Inter (system-ui fallback)
- **Sizes**: Tailwind defaults
- **Special**: Mono font for code/timestamps

### Spacing
- **Message spacing**: `space-y-4`
- **Component padding**: `p-4`
- **Input padding**: `px-3 py-2`

### Animations
- `animate-bounce` - Typing indicators
- `animate-pulse` - Connection status
- `pulse-slow` - Custom 3s pulse

---

## 🔧 Utility Components

### App
**Path**: `packages/web/src/App.tsx`  
**Purpose**: Main application component with state management

**Responsibilities**:
- Session management
- localStorage persistence
- Message handling
- Mock AI responses

**Helper Functions**:
- `generateSessionId()` - Unique session IDs
- `generateMessageId()` - Unique message IDs
- `getSimulatedResponse()` - Mock AI responses
- `maybeAddTodoMarkers()` - TODO detection

---

## 📁 Assets

### Maple Leaf Icon
**Path**: `packages/web/public/maple-leaf.svg`  
**Purpose**: Application logo/favicon  
**Format**: SVG with red maple leaf design

---

## 🚀 Future Components (Planned)

### Session Management
- [ ] SessionHistory - Browse past sessions
- [ ] SessionPicker - Select from saved sessions

### Rich Content
- [ ] MarkdownMessage - Formatted text support
- [ ] CodeBlock - Syntax highlighted code
- [ ] MathDisplay - LaTeX equation rendering

### Learning Features
- [ ] ProgressTracker - Student progress display
- [ ] QuizComponent - Interactive quizzes
- [ ] FlashCard - Study card component

### Media
- [ ] VoiceInput - Speech-to-text input
- [ ] AudioPlayer - Play audio responses
- [ ] ImageUpload - Homework photo uploads

### Analytics
- [ ] UsageStats - Session statistics
- [ ] LearningInsights - Progress analytics

---

## 📝 Component Guidelines

### Creating New Components
1. Use TypeScript for all components
2. Define clear prop interfaces
3. Keep components under 200 lines
4. Create sub-components for complex logic
5. Add to this inventory

### Naming Conventions
- **Components**: PascalCase (e.g., `MessageItem`)
- **Props**: camelCase with descriptive names
- **Files**: Match component name exactly

### Documentation Requirements
- Purpose and responsibility
- Complete props documentation
- Usage examples
- Feature list
- Sub-components if applicable

### Testing Requirements
- Unit tests for logic
- Render tests for display
- Interaction tests for user input
- Accessibility tests

---

## 📊 Impact Assessment

### High-Impact Components (Used Everywhere)
- ErrorBoundary - Wraps entire app
- Header - Present on all screens
- Loading - All async operations

### Medium-Impact Components (Feature-Specific)
- ChatInterface - Main chat feature
- MessageInput - User interaction
- MessageItem - Message display

### Low-Impact Components (Isolated)
- TypingIndicator - Visual feedback only
- TodoMarkers - Optional enhancement

---

## 🚀 Backend Components

### API Endpoints

#### POST /api/chat/message
**Path**: `backend/app/main.py:50-90`  
**Purpose**: Process chat messages with AI providers  
**Request Body**:
```python
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    mode: Optional[ConversationMode] = None
```

**Response**:
```python
class ChatResponse(BaseModel):
    response: str
    mode: ConversationMode
    provider: str
    session_id: str
    message_id: str
    metadata: Optional[Dict] = None
```

**Features**:
- Automatic mode detection
- Provider selection and failover
- Session management
- Error handling

---

### AI Services

#### ClaudeService
**Path**: `backend/app/services/claude_service.py`  
**Purpose**: Anthropic Claude API integration  
**Methods**:
- `generate_response(prompt: str, conversation_history: List[Dict])` - Generate AI response
- `is_available()` - Check service availability

**Configuration**:
- Model: Claude 3 Sonnet
- Max tokens: 4096
- Temperature: 0.7

**Usage**:
```python
service = ClaudeService()
response = await service.generate_response(prompt, history)
```

#### OpenAIService
**Path**: `backend/app/services/openai_service.py`  
**Purpose**: OpenAI GPT-4 API integration  
**Methods**:
- `generate_response(prompt: str, conversation_history: List[Dict])` - Generate AI response
- `is_available()` - Check service availability

**Configuration**:
- Model: GPT-4 Turbo
- Max tokens: 4096
- Temperature: 0.7

---

### Orchestration Components

#### AIOrchestrator
**Path**: `backend/app/ai_orchestrator.py`  
**Purpose**: Intelligent provider selection and mode detection  
**Methods**:
- `select_mode(message: str, history: List)` - Detect conversation mode
- `select_provider(message: str, mode: ConversationMode)` - Choose AI provider
- `generate_response(message: str, mode: ConversationMode, session_id: str)` - Orchestrate response

**Mode Detection Keywords**:
- **Learning**: "why", "how", "explain", "understand"
- **Story**: "story", "tell me about", "adventure"
- **Explanatory**: "stuck", "confused", "help me"
- **Discovery**: "explore", "discover", "investigate"

**Provider Selection Logic**:
- Math/technical → OpenAI
- Learning/Story → Anthropic
- Default → Anthropic

---

### Data Management

#### SessionManager
**Path**: `backend/app/session_manager.py`  
**Purpose**: In-memory session storage  
**Methods**:
- `create_session()` - Create new session
- `get_session(session_id: str)` - Retrieve session
- `add_message(session_id: str, message: Message)` - Add to history
- `get_conversation_history(session_id: str)` - Get formatted history

**Data Structure**:
```python
Session = {
    "id": str,
    "messages": List[Message],
    "created_at": datetime,
    "last_activity": datetime
}
```

#### AirtableService
**Path**: `backend/app/airtable_service.py`  
**Purpose**: Curriculum content retrieval from Airtable database  
**Methods**:
- `initialize()` - Connect to Airtable API
- `get_content_for_topic(topic: str)` - Fetch curriculum content
- `get_activities(topic: str)` - Get topic-specific activities
- `get_canadian_examples(topic: str)` - Fetch Canadian examples
- `check_health()` - Verify service connectivity
- `cleanup()` - Cleanup service resources

**Features**:
- In-memory caching with TTL
- Fallback content for offline operation
- Automatic retry logic
- Connection pooling

---

## 📚 Content Components

### Content API Endpoints

#### GET /api/content/curriculum/topics
**Path**: `backend/app/api/content.py:22-45`  
**Purpose**: Retrieve curriculum topics with optional filtering  
**Query Parameters**:
- `topic` (optional): Filter by topic name

**Response Model**:
```python
{
    "data": CurriculumContentResponse,
    "cached": bool
}
```

#### GET /api/content/activities
**Path**: `backend/app/api/content.py:48-59`  
**Purpose**: Get activities for a specific curriculum topic  
**Query Parameters**:
- `topic` (required): Curriculum topic name

**Response Model**:
```python
{
    "data": List[ActivityResponse],
    "count": int
}
```

#### GET /api/content/canadian-examples
**Path**: `backend/app/api/content.py:62-80`  
**Purpose**: Retrieve Canadian examples for a topic  
**Query Parameters**:
- `topic` (required): Curriculum topic

**Response Model**:
```python
{
    "data": List[str]
}
```

#### GET /api/content/health
**Path**: `backend/app/api/content.py:83-101`  
**Purpose**: Check Airtable service health status  

**Response Model**:
```python
{
    "status": "healthy" | "unhealthy",
    "service": "airtable",
    "initialized": bool,
    "error": Optional[str]
}
```

---

### Content Models

#### CurriculumTopic
**Path**: `backend/app/models/content.py:69-83`  
**Purpose**: Ontario Grade 4 Science curriculum topic model  
**Fields**:
- `topic_name`: Main topic (Light/Sound)
- `subtopic`: Specific subtopic
- `curriculum_expectation`: Ontario curriculum code
- `key_concepts`: List of core concepts
- `difficulty_level`: Introductory/Intermediate/Advanced
- `canadian_connection`: Canadian context
- `indigenous_perspective`: Indigenous knowledge
- `estimated_duration`: Lesson duration in minutes

#### ActivityTemplate
**Path**: `backend/app/models/content.py:96-112`  
**Purpose**: Hands-on activity template with TODO markers  
**Fields**:
- `activity_name`: Activity title
- `curriculum_topic`: Related topic
- `activity_type`: Type of activity (Experiment/Investigation/etc.)
- `mode`: AI interaction mode (learning/explanatory/story)
- `materials_needed`: Required materials
- `instructions`: Step-by-step with TODO markers
- `safety_notes`: Safety considerations
- `discussion_prompts`: Reflection questions
- `canadian_example`: Canadian context
- `difficulty`: Difficulty level
- `group_size`: Individual/pairs/group

#### CanadianExample
**Path**: `backend/app/models/content.py:114-125`  
**Purpose**: Real-world Canadian examples for contextual learning  
**Fields**:
- `example_title`: Example name
- `curriculum_topic`: Related topic
- `province_territory`: Location in Canada
- `description`: Detailed description
- `indigenous_connection`: Indigenous perspectives
- `french_connection`: French-Canadian connections
- `visual_description`: Visual description for AI
- `fun_fact`: Engaging fact

#### StoryCharacter
**Path**: `backend/app/models/content.py:127-138`  
**Purpose**: Narrative mode characters for storytelling  
**Fields**:
- `character_name`: Character's name
- `character_type`: Role in stories
- `personality_traits`: Character traits list
- `backstory`: Character background
- `catchphrase`: Signature phrase
- `home_province`: Canadian province/territory
- `special_ability`: Unique abilities
- `curriculum_connection`: Related topics
- `visual_description`: Appearance description

#### ContentAdaptation
**Path**: `backend/app/models/content.py:140-149`  
**Purpose**: Modified content for different learning styles  
**Fields**:
- `base_content_id`: Original activity reference
- `learning_style`: Visual/Auditory/Kinesthetic/Reading-Writing
- `adaptation_type`: Type of modification
- `modified_instructions`: Adapted instructions
- `additional_supports`: Extra resources list
- `time_adjustment`: Time modification in minutes
- `success_modifications`: Adjusted success criteria

---

### Content Data Files

#### curriculum_data.json
**Path**: `content/curriculum_data.json`  
**Purpose**: Ontario Grade 4 Science curriculum structure  
**Structure**:
```json
{
  "grade4_science_curriculum": {
    "light_unit": {
      "overall_expectations": [...],
      "topics": [
        {
          "topic_name": "Light",
          "subtopic": "Sources of Light",
          "curriculum_expectation": "2.2 Distinguish...",
          "key_concepts": [...],
          "canadian_connection": "Northern Lights...",
          "indigenous_perspective": "Traditional Inuit..."
        }
      ]
    },
    "sound_unit": {...}
  }
}
```
**Content**: 14 curriculum topics (7 Light, 7 Sound)

#### activity_templates.json
**Path**: `content/activity_templates.json`  
**Purpose**: Hands-on learning activities with TODO markers  
**Structure**:
```json
{
  "activity_templates": [
    {
      "activity_name": "Rainbow Creation Lab",
      "curriculum_topic": "Light - Refraction",
      "instructions": "TODO(student): Fill glass...",
      "materials_needed": "Glass, water, flashlight...",
      "canadian_example": "Rainbow at Niagara Falls"
    }
  ]
}
```
**Content**: 16 hands-on activities

#### canadian_examples.json
**Path**: `content/canadian_examples.json`  
**Purpose**: Canadian contextual examples  
**Structure**:
```json
{
  "canadian_examples": {
    "light_examples": [...],
    "sound_examples": [...]
  }
}
```
**Content**: 27 examples (13 Light, 14 Sound) from all provinces/territories

#### story_characters.json
**Path**: `content/story_characters.json`  
**Purpose**: Narrative mode characters  
**Structure**:
```json
{
  "story_characters": [
    {
      "character_name": "Maple",
      "character_type": "Main Guide",
      "personality_traits": ["curious", "helpful"],
      "home_province": "Ontario",
      "special_ability": "Can sense vibrations"
    }
  ]
}
```
**Content**: 8 Canadian animal characters

#### airtable_structure.md
**Path**: `content/airtable_structure.md`  
**Purpose**: Complete Airtable database schema documentation  
**Tables Documented**:
- Grade4_Science_Curriculum
- Learning_Objectives
- Activity_Templates
- Canadian_Examples
- Story_Characters
- Content_Adaptations

---

### Configuration Components

#### Config
**Path**: `backend/app/config.py`  
**Purpose**: Environment variable management  
**Settings**:
```python
class Settings(BaseSettings):
    openai_api_key: Optional[str]
    anthropic_api_key: Optional[str]
    airtable_api_key: Optional[str]
    airtable_base_id: Optional[str]
    airtable_table_name: str = "Content"
    debug: bool = False
```

#### Prompts
**Path**: `backend/app/prompts.py`  
**Purpose**: Load and manage system prompts from YAML  
**Functions**:
- `load_prompts()` - Load from YAML with caching
- `get_system_prompt(mode: ConversationMode)` - Get mode-specific prompt
- `get_activity_prompt()` - Get TODO activity prompt
- `reload_prompts()` - Force reload (debug mode)

**YAML Configuration**:
**Path**: `backend/app/prompts.yaml`  
- Base prompt (Maple personality)
- Four mode configurations
- Activity prompt template

---

### Model Definitions

#### Pydantic Models
**Path**: `backend/app/models.py`  
**Purpose**: Request/response validation  

**Models**:
```python
class ConversationMode(Enum):
    LEARNING = "learning"
    EXPLANATORY = "explanatory"
    STORY = "story"
    DISCOVERY = "discovery"

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime
    mode: Optional[ConversationMode]

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str]
    mode: Optional[ConversationMode]

class ChatResponse(BaseModel):
    response: str
    mode: ConversationMode
    provider: str
    session_id: str
    message_id: str
```

---

## 📊 Backend Impact Assessment

### High-Impact Components (Core Functionality)
- AIOrchestrator - Central logic for all AI interactions
- SessionManager - Required for all conversations
- Config - Environment settings affect entire system

### Medium-Impact Components (Feature-Specific)
- ClaudeService - Primary AI provider
- OpenAIService - Fallback/technical provider
- Prompts system - Behavior customization

### Low-Impact Components (Optional)
- AirtableService - Curriculum enhancement
- Activity prompt generation

---

## 🔧 Backend Utilities

### Testing
**Path**: `backend/tests/test_main.py`  
**Purpose**: API endpoint testing  
**Coverage**:
- Health check endpoint
- Chat endpoint with mock
- Session management
- Error handling

### Development Tools
**Path**: `backend/test_prompts_yaml.py`  
**Purpose**: YAML prompt validation  
**Features**:
- Load verification
- Mode enumeration
- Prompt length checking

---

## 🔄 Version History

### Issue #6 - Airtable Curriculum Content
**Date**: 2024  
**Components Added**:
- Content API endpoints (/api/content/*)
- Content Pydantic models (CurriculumTopic, ActivityTemplate, etc.)
- Airtable service with caching
- JSON content data files (curriculum, activities, examples, characters)
- Database schema documentation
- 14 curriculum topics aligned with Ontario expectations
- 16 hands-on activities with TODO markers
- 27 Canadian examples from all provinces/territories
- 8 narrative mode characters

### Issue #5 - Backend AI Orchestration
**Date**: 2024  
**Components Added**:
- AI service integrations (Claude, OpenAI)
- AI Orchestrator with mode detection
- Session management system
- Prompt configuration (YAML-based)
- Airtable service integration
- API endpoints (chat, health, session)
- Pydantic models
- Configuration management

### Issue #4 - Frontend Chat Interface
**Date**: 2024  
**Components Added**: 
- All layout components (Header)
- All chat components (ChatInterface, MessageList, MessageItem, MessageInput)
- Error handling (ErrorBoundary, Loading)
- Type definitions
- Design system setup

---

## 📌 Notes for Developers

1. **Component Reusability**: All components are designed to be reusable. Check this inventory before creating new components.

2. **Type Safety**: Always use the TypeScript interfaces from `types/chat.ts` for consistency.

3. **Styling**: Use Tailwind utilities. Custom CSS should be rare and well-documented.

4. **State Management**: Currently using React state. Will migrate to Redux/Zustand if complexity grows.

5. **Performance**: Components use React.memo where beneficial. Monitor re-renders in development.

6. **Accessibility**: All interactive components have ARIA labels and keyboard support.

7. **Mobile-First**: Design for mobile, enhance for desktop.

8. **Testing**: Each component should have corresponding test file in `__tests__` directory.

---

## 📊 Content Component Summary

### Component Organization by Type

#### **Data Models** (7 total)
- **Core Models**: CurriculumTopic, ActivityTemplate, CanadianExample, StoryCharacter
- **Support Models**: ContentAdaptation, LearningObjective, ContentSearchResult
- **Enums**: DifficultyLevel, ActivityType, AIMode, BloomLevel, LearningStyle, ProvinceTerritory

#### **API Endpoints** (4 total)
- **Content Retrieval**: /api/content/curriculum/topics, /api/content/activities
- **Examples**: /api/content/canadian-examples
- **Health Check**: /api/content/health

#### **Data Files** (5 total)
- **Curriculum**: curriculum_data.json (14 topics)
- **Activities**: activity_templates.json (16 activities)
- **Examples**: canadian_examples.json (27 examples)
- **Characters**: story_characters.json (8 characters)
- **Schema**: airtable_structure.md (6 tables)

#### **Services** (1 total)
- **AirtableService**: Complete CRUD operations with caching and fallback

### Content Statistics
- **Total Curriculum Topics**: 14 (7 Light, 7 Sound)
- **Total Activities**: 16 hands-on experiments
- **Total Canadian Examples**: 27 from all provinces/territories
- **Total Story Characters**: 8 Canadian animals
- **Provincial Coverage**: All 13 provinces and territories represented
- **Indigenous Perspectives**: Integrated in 100% of topics
- **French Connections**: Included in all examples

### Integration Points
- **Backend**: AirtableService integrates with AI Orchestrator for content delivery
- **Frontend**: Content will be displayed through MessageItem components with TODO highlighting
- **Caching**: In-memory cache with configurable TTL for performance
- **Fallback**: Static content ensures operation without Airtable connection