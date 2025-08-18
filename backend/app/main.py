from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
import logging
import uuid

from app.config import settings
from app.models import (
    ChatRequest, 
    ChatResponse, 
    HealthResponse, 
    ErrorResponse,
    SessionData
)
from app.session_manager import SessionManager
from app.ai_orchestrator import AIOrchestrator
from app.airtable_service import AirtableService

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Tutor backend for Ontario Grade 4 students"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_manager = SessionManager()
ai_orchestrator = AIOrchestrator()
airtable_service = AirtableService()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    try:
        await ai_orchestrator.initialize()
        await airtable_service.initialize()
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application")
    await ai_orchestrator.cleanup()
    await airtable_service.cleanup()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.debug else None,
            status_code=500
        ).dict()
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"{settings.app_name} API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services_status = {
        "claude": await ai_orchestrator.check_claude_health(),
        "openai": await ai_orchestrator.check_openai_health(),
        "airtable": await airtable_service.check_health(),
        "session_manager": True
    }
    
    return HealthResponse(
        status="healthy" if all(services_status.values()) else "degraded",
        version=settings.app_version,
        timestamp=datetime.utcnow(),
        services=services_status
    )


@app.post("/api/chat/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Main chat endpoint"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        session = session_manager.get_or_create_session(session_id)
        
        session_manager.add_message(
            session_id, 
            role="user",
            content=request.message
        )
        
        curriculum_content = None
        topic = ai_orchestrator.extract_topic(request.message)
        if topic:
            curriculum_content = await airtable_service.get_content_for_topic(topic)
            session_manager.update_session_metadata(
                session_id, 
                {"current_topic": topic}
            )
        
        ai_response = await ai_orchestrator.process_message(
            message=request.message,
            session=session,
            curriculum_content=curriculum_content,
            force_provider=request.force_provider,
            force_mode=request.force_mode
        )
        
        session_manager.add_message(
            session_id,
            role="assistant",
            content=ai_response["response"],
            provider=ai_response["provider"],
            mode=ai_response["mode"]
        )
        
        activity_markers = ai_orchestrator.extract_activity_markers(
            ai_response["response"]
        )
        
        return ChatResponse(
            response=ai_response["response"],
            session_id=session_id,
            provider=ai_response["provider"],
            mode=ai_response["mode"],
            has_activity=len(activity_markers) > 0,
            activity_markers=activity_markers if activity_markers else None,
            curriculum_content=curriculum_content
        )
        
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )


@app.get("/api/session/{session_id}", response_model=SessionData)
async def get_session(session_id: str):
    """Get session data"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )
    return session


@app.delete("/api/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a session"""
    if session_manager.clear_session(session_id):
        return {"message": f"Session {session_id} cleared successfully"}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )