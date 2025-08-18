import { FC } from 'react';
import { Message } from '../types/chat';
import clsx from 'clsx';

interface MessageItemProps {
  message: Message;
}

const MessageItem: FC<MessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isTyping = message.metadata?.isTyping;
  
  return (
    <div className={clsx('flex', isUser ? 'justify-end' : 'justify-start')}>
      <div className={clsx(
        'max-w-[70%] rounded-lg px-4 py-2.5',
        isUser ? 'bg-maple-500 text-white' : 'bg-gray-100 text-gray-900'
      )}>
        {isTyping ? (
          <TypingIndicator />
        ) : (
          <>
            <div className="whitespace-pre-wrap break-words">{message.content}</div>
            
            {message.metadata?.hasTodo && message.metadata.todoItems && (
              <TodoMarkers items={message.metadata.todoItems} />
            )}
            
            <div className={clsx(
              'text-xs mt-1',
              isUser ? 'text-maple-100' : 'text-gray-500'
            )}>
              {formatTime(message.timestamp)}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

const TypingIndicator: FC = () => {
  return (
    <div className="flex space-x-1 py-2">
      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
    </div>
  );
};

interface TodoMarkersProps {
  items: string[];
}

const TodoMarkers: FC<TodoMarkersProps> = ({ items }) => {
  return (
    <div className="mt-3 pt-3 border-t border-gray-200">
      <div className="text-sm font-semibold mb-2 flex items-center">
        <span className="text-yellow-600">📝</span>
        <span className="ml-1">Learning Tasks:</span>
      </div>
      <ul className="space-y-1">
        {items.map((item, index) => (
          <li key={index} className="text-sm flex items-start">
            <span className="text-yellow-500 mr-2">•</span>
            <span className="flex-1">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

function formatTime(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(date);
}

export default MessageItem;