"""
Content API endpoints for Airtable curriculum data
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict
from app.airtable_service import AirtableService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


# Dependency to get AirtableService instance
async def get_airtable_service():
    """Get initialized Airtable service"""
    service = AirtableService()
    await service.initialize()
    return service


@router.get("/curriculum/topics")
async def get_curriculum_topics(
    topic: Optional[str] = Query(None, description="Filter by topic name"),
    service: AirtableService = Depends(get_airtable_service)
):
    """Get curriculum content for a specific topic"""
    try:
        if topic:
            content = await service.get_content_for_topic(topic)
            if not content:
                raise HTTPException(
                    status_code=404,
                    detail=f"Topic '{topic}' not found"
                )
            return {"data": content, "cached": False}
        else:
            # Return available topics from fallback
            topics = ['light', 'sound', 'structures', 'habitats', 'rocks', 'pulleys']
            return {"data": topics, "cached": False}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching curriculum topics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activities")
async def get_activities(
    topic: str = Query(..., description="Curriculum topic"),
    service: AirtableService = Depends(get_airtable_service)
):
    """Get activities for a specific topic"""
    try:
        activities = await service.get_activities(topic)
        return {"data": activities, "count": len(activities)}
    except Exception as e:
        logger.error(f"Error fetching activities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/canadian-examples")
async def get_canadian_examples(
    topic: str = Query(..., description="Curriculum topic"),
    service: AirtableService = Depends(get_airtable_service)
):
    """Get Canadian examples for a topic"""
    try:
        examples = await service.get_canadian_examples(topic)
        if not examples:
            raise HTTPException(
                status_code=404, 
                detail="No Canadian examples found"
            )
        return {"data": examples}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching Canadian examples: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check(
    service: AirtableService = Depends(get_airtable_service)
):
    """Check if Airtable service is healthy"""
    try:
        is_healthy = await service.check_health()
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "service": "airtable",
            "initialized": service.is_initialized
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "airtable",
            "error": str(e)
        }