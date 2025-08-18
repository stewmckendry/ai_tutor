from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
import logging
from app.models import SessionData, ChatMessage, AIProvider, ConversationMode
from app.config import settings

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages in-memory session storage and lifecycle"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
        self.session_expiry: Dict[str, datetime] = {}
    
    def get_or_create_session(self, session_id: str) -> SessionData:
        """Get existing session or create new one"""
        self._cleanup_expired_sessions()
        
        if session_id in self.sessions:
            self._update_session_expiry(session_id)
            self.sessions[session_id].last_activity = datetime.utcnow()
            logger.debug(f"Retrieved existing session: {session_id}")
            return self.sessions[session_id]
        
        new_session = SessionData(
            session_id=session_id,
            messages=[],
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            current_topic=None,
            student_level="grade-4",
            metadata={}
        )
        
        self.sessions[session_id] = new_session
        self._update_session_expiry(session_id)
        
        logger.info(f"Created new session: {session_id}")
        return new_session
    
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session by ID"""
        self._cleanup_expired_sessions()
        
        if session_id in self.sessions:
            self._update_session_expiry(session_id)
            self.sessions[session_id].last_activity = datetime.utcnow()
            return self.sessions[session_id]
        
        return None
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        provider: Optional[AIProvider] = None,
        mode: Optional[ConversationMode] = None
    ):
        """Add message to session"""
        session = self.get_or_create_session(session_id)
        
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            provider=provider,
            mode=mode
        )
        
        session.messages.append(message)
        
        if len(session.messages) > settings.max_conversation_length * 2:
            system_messages = [m for m in session.messages if m.role == "system"]
            other_messages = [m for m in session.messages if m.role != "system"]
            
            other_messages = other_messages[-(settings.max_conversation_length * 2 - len(system_messages)):]
            
            session.messages = system_messages + other_messages
            logger.debug(f"Trimmed session {session_id} to max length")
        
        self.sessions[session_id].last_activity = datetime.utcnow()
        self._update_session_expiry(session_id)
        
        logger.debug(f"Added {role} message to session {session_id}")
    
    def update_session_metadata(self, session_id: str, metadata: Dict[str, Any]):
        """Update session metadata"""
        session = self.get_session(session_id)
        if session:
            session.metadata.update(metadata)
            
            if 'current_topic' in metadata:
                session.current_topic = metadata['current_topic']
            
            self.sessions[session_id].last_activity = datetime.utcnow()
            self._update_session_expiry(session_id)
            
            logger.debug(f"Updated metadata for session {session_id}")
    
    def clear_session(self, session_id: str) -> bool:
        """Clear a specific session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if session_id in self.session_expiry:
                del self.session_expiry[session_id]
            logger.info(f"Cleared session: {session_id}")
            return True
        return False
    
    def get_all_sessions(self) -> Dict[str, SessionData]:
        """Get all active sessions"""
        self._cleanup_expired_sessions()
        return self.sessions.copy()
    
    def get_session_count(self) -> int:
        """Get count of active sessions"""
        self._cleanup_expired_sessions()
        return len(self.sessions)
    
    def _update_session_expiry(self, session_id: str):
        """Update session expiry time"""
        self.session_expiry[session_id] = datetime.utcnow() + timedelta(minutes=settings.session_ttl_minutes)
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        for session_id, expiry_time in self.session_expiry.items():
            if current_time > expiry_time:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
            del self.session_expiry[session_id]
            logger.info(f"Cleaned up expired session: {session_id}")
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            'session_id': session.session_id,
            'created_at': session.created_at.isoformat(),
            'last_activity': session.last_activity.isoformat(),
            'message_count': len(session.messages),
            'current_topic': session.current_topic,
            'student_level': session.student_level,
            'providers_used': list(set([m.provider for m in session.messages if m.provider])),
            'modes_used': list(set([m.mode for m in session.messages if m.mode]))
        }
    
    def clear_all_sessions(self):
        """Clear all sessions (for testing/admin purposes)"""
        count = len(self.sessions)
        self.sessions.clear()
        self.session_expiry.clear()
        logger.warning(f"Cleared all {count} sessions")
        return count