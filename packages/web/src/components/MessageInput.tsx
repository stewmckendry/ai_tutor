import { FC, useState, KeyboardEvent, FormEvent } from 'react';

interface MessageInputProps {
  onSendMessage: (content: string) => void;
}

const MessageInput: FC<MessageInputProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [isComposing, setIsComposing] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    sendMessage();
  };

  const sendMessage = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage) {
      onSendMessage(trimmedMessage);
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Allow Enter to send message (unless composing or Shift is held)
    if (e.key === 'Enter' && !e.shiftKey && !isComposing) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleTextAreaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    
    // Auto-resize textarea
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 150) + 'px';
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <textarea
        value={message}
        onChange={handleTextAreaChange}
        onKeyDown={handleKeyDown}
        onCompositionStart={() => setIsComposing(true)}
        onCompositionEnd={() => setIsComposing(false)}
        placeholder="Ask me anything about Grade 4 topics..."
        className="flex-1 resize-none rounded-lg border border-gray-300 px-3 py-2 
                   focus:outline-none focus:ring-2 focus:ring-maple-500 focus:border-transparent
                   placeholder-gray-400 min-h-[44px] max-h-[150px]"
        rows={1}
      />
      
      <button
        type="submit"
        disabled={!message.trim()}
        className="px-4 py-2 bg-maple-500 text-white rounded-lg hover:bg-maple-600 
                   disabled:opacity-50 disabled:cursor-not-allowed transition-all
                   flex items-center justify-center min-w-[80px]"
      >
        <SendIcon />
        <span className="ml-2 hidden sm:inline">Send</span>
      </button>
    </form>
  );
};

const SendIcon: FC = () => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width="20" 
    height="20" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round"
  >
    <line x1="22" y1="2" x2="11" y2="13"></line>
    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
  </svg>
);

export default MessageInput;