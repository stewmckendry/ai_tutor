export interface Message {
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

export interface ChatSession {
  id: string;
  messages: Message[];
  startedAt: Date;
  lastActivityAt: Date;
  title?: string;
}

export interface TodoMarker {
  id: string;
  text: string;
  completed: boolean;
  messageId: string;
}