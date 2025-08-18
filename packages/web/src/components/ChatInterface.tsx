import { FC, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import TopicPills from './TopicPills';
import { Message } from '../types/chat';

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (content: string) => void;
}

const ChatInterface: FC<ChatInterfaceProps> = ({ messages, onSendMessage }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-[calc(100vh-140px)] flex flex-col">
      {/* Show topic pills only when there are no messages or just started */}
      {messages.length <= 2 && (
        <TopicPills onTopicClick={onSendMessage} />
      )}
      
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} />
        <div ref={messagesEndRef} />
      </div>
      
      <div className="border-t border-gray-200 p-4">
        <MessageInput onSendMessage={onSendMessage} />
      </div>
    </div>
  );
};

export default ChatInterface;