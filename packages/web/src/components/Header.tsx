import { FC } from 'react';

interface HeaderProps {
  isConnected: boolean;
  onNewSession: () => void;
  sessionTitle?: string;
}

const Header: FC<HeaderProps> = ({ isConnected, onNewSession, sessionTitle }) => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3 max-w-4xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">🍁</span>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Maple</h1>
              <p className="text-xs text-gray-600">Grade 4 AI Tutor</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-gray-400'} animate-pulse`} />
              <span className="text-sm text-gray-600">
                {isConnected ? 'Connected' : 'Offline Mode'}
              </span>
            </div>
            
            <button
              onClick={onNewSession}
              className="px-3 py-1.5 text-sm bg-maple-500 text-white rounded-lg hover:bg-maple-600 transition-colors"
            >
              New Session
            </button>
          </div>
        </div>
        
        {sessionTitle && (
          <div className="mt-2 text-sm text-gray-600">
            Current session: {sessionTitle}
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;