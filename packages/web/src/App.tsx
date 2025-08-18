import { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import Header from './components/Header';
import Loading from './components/Loading';
import { Message, ChatSession } from './types/chat';
import { apiService } from './services/api';

function App() {
  const [session, setSession] = useState<ChatSession | null>(null);
  const [isConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load session from localStorage on mount
    const savedSession = localStorage.getItem('chatSession');
    if (savedSession) {
      try {
        const parsed = JSON.parse(savedSession);
        // Convert date strings back to Date objects
        parsed.startedAt = new Date(parsed.startedAt);
        parsed.lastActivityAt = new Date(parsed.lastActivityAt);
        parsed.messages = parsed.messages.map((msg: any) => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        }));
        setSession(parsed);
      } catch (error) {
        console.error('Failed to load saved session:', error);
        initNewSession();
      }
    } else {
      initNewSession();
    }
    setIsLoading(false);
  }, []);

  useEffect(() => {
    // Save session to localStorage whenever it changes
    if (session) {
      localStorage.setItem('chatSession', JSON.stringify(session));
    }
  }, [session]);

  const initNewSession = () => {
    const newSession: ChatSession = {
      id: generateSessionId(),
      messages: [
        {
          id: generateMessageId(),
          content: "Hello! I'm Maple, your Grade 4 learning buddy! 🍁 What would you like to learn about today? We can explore science, math, language arts, or anything else you're curious about!",
          role: 'assistant',
          timestamp: new Date(),
        }
      ],
      startedAt: new Date(),
      lastActivityAt: new Date(),
      title: 'New Learning Session'
    };
    setSession(newSession);
  };

  const handleSendMessage = async (content: string) => {
    if (!session) return;

    const userMessage: Message = {
      id: generateMessageId(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    const updatedSession = {
      ...session,
      messages: [...session.messages, userMessage],
      lastActivityAt: new Date(),
    };

    setSession(updatedSession);

    // Add typing indicator
    setTimeout(async () => {
      const typingMessage: Message = {
        id: generateMessageId(),
        content: '',
        role: 'assistant',
        timestamp: new Date(),
        metadata: { isTyping: true }
      };

      setSession(prev => prev ? {
        ...prev,
        messages: [...prev.messages, typingMessage],
        lastActivityAt: new Date(),
      } : null);

      // Call actual API
      try {
        const response = await apiService.sendMessage(content, session.id);
        
        const assistantMessage: Message = {
          id: generateMessageId(),
          content: response.response,
          role: 'assistant',
          timestamp: new Date(),
          metadata: response.metadata,
        };

        setSession(prev => {
          if (!prev) return null;
          // Remove typing indicator and add real message
          const filteredMessages = prev.messages.filter(msg => !msg.metadata?.isTyping);
          return {
            ...prev,
            messages: [...filteredMessages, assistantMessage],
            lastActivityAt: new Date(),
          };
        });
      } catch (error) {
        console.error('Failed to send message:', error);
        
        // Remove typing indicator and show error message
        const errorMessage: Message = {
          id: generateMessageId(),
          content: 'Sorry, I had trouble processing that. Please try again.',
          role: 'assistant',
          timestamp: new Date(),
          metadata: { isError: true }
        };

        setSession(prev => {
          if (!prev) return null;
          const filteredMessages = prev.messages.filter(msg => !msg.metadata?.isTyping);
          return {
            ...prev,
            messages: [...filteredMessages, errorMessage],
            lastActivityAt: new Date(),
          };
        });
      }
    }, 500);
  };

  const handleNewSession = () => {
    if (confirm('Start a new session? Your current chat will be saved.')) {
      initNewSession();
    }
  };

  if (isLoading) {
    return <Loading message="Initializing Maple..." />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header 
        isConnected={isConnected}
        onNewSession={handleNewSession}
        sessionTitle={session?.title}
      />
      <main className="flex-1 container mx-auto px-4 py-4 max-w-4xl">
        {session && (
          <ChatInterface
            messages={session.messages}
            onSendMessage={handleSendMessage}
          />
        )}
      </main>
    </div>
  );
}

function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function generateMessageId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function getSimulatedResponse(userMessage: string): string {
  const responses = [
    "That's a great question! Let me help you understand that better.",
    "Interesting! Here's what I know about that topic...",
    "Let's explore this together! First, we should understand...",
    "Excellent thinking! To answer your question...",
    "I love your curiosity! Here's something cool about that...",
  ];
  
  const lowerMessage = userMessage.toLowerCase();
  
  if (lowerMessage.includes('light') || lowerMessage.includes('sound')) {
    return "Great! Light and sound are fascinating topics in Grade 4 science! 🔦🔊 Would you like to learn about how light travels, how we see colors, or maybe how sound waves work?";
  }
  
  if (lowerMessage.includes('math')) {
    return "Math is awesome! 🔢 In Grade 4, we can work on multiplication, division, fractions, or geometry. What would you like to practice?";
  }
  
  if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
    return "Hello there! I'm excited to learn with you today! What subject interests you most?";
  }
  
  return responses[Math.floor(Math.random() * responses.length)];
}

function maybeAddTodoMarkers(content: string): any {
  const lowerContent = content.toLowerCase();
  if (lowerContent.includes('homework') || lowerContent.includes('practice') || lowerContent.includes('learn')) {
    return {
      hasTodo: true,
      todoItems: [
        'Practice multiplication tables (3x and 4x)',
        'Read Chapter 5 in science textbook',
        'Complete worksheet on light properties',
      ]
    };
  }
  return {};
}

export default App;