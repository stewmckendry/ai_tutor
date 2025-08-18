"""
Pydantic models for curriculum content
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    INTRODUCTORY = "Introductory"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class ActivityType(str, Enum):
    EXPERIMENT = "Experiment"
    INVESTIGATION = "Investigation"
    CREATIVE_ACTIVITY = "Creative Activity"
    ENGINEERING = "Engineering"
    PROBLEM_SOLVING = "Problem Solving"
    GROUP_ACTIVITY = "Group Activity"
    OUTDOOR_INVESTIGATION = "Outdoor Investigation"
    SENSORY_ACTIVITY = "Sensory Activity"
    ART_SCIENCE = "Art & Science"
    MUSIC_CREATION = "Music Creation"
    COMMUNICATION_CHALLENGE = "Communication Challenge"


class AIMode(str, Enum):
    LEARNING = "learning"
    EXPLANATORY = "explanatory"
    STORY = "story"


class BloomLevel(str, Enum):
    REMEMBERING = "Remembering"
    UNDERSTANDING = "Understanding"
    APPLYING = "Applying"
    ANALYZING = "Analyzing"
    EVALUATING = "Evaluating"
    CREATING = "Creating"


class LearningStyle(str, Enum):
    VISUAL = "Visual"
    AUDITORY = "Auditory"
    KINESTHETIC = "Kinesthetic"
    READING_WRITING = "Reading/Writing"


class ProvinceTerritory(str, Enum):
    ONTARIO = "Ontario"
    QUEBEC = "Quebec"
    BRITISH_COLUMBIA = "British Columbia"
    ALBERTA = "Alberta"
    MANITOBA = "Manitoba"
    SASKATCHEWAN = "Saskatchewan"
    NOVA_SCOTIA = "Nova Scotia"
    NEW_BRUNSWICK = "New Brunswick"
    PRINCE_EDWARD_ISLAND = "Prince Edward Island"
    NEWFOUNDLAND_LABRADOR = "Newfoundland and Labrador"
    NORTHWEST_TERRITORIES = "Northwest Territories"
    YUKON = "Yukon"
    NUNAVUT = "Nunavut"


class CurriculumTopic(BaseModel):
    topic_id: Optional[int] = None
    topic_name: str
    subtopic: str
    curriculum_expectation: str
    description: str
    key_concepts: List[str]
    difficulty_level: DifficultyLevel
    prerequisite_topics: Optional[List[str]] = []
    canadian_connection: str
    indigenous_perspective: str
    estimated_duration: int = Field(..., ge=10, le=60)
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class LearningObjective(BaseModel):
    objective_id: Optional[int] = None
    curriculum_topic_id: str
    objective_text: str
    bloom_level: BloomLevel
    success_criteria: str
    assessment_type: List[str]
    skills_developed: List[str]


class ActivityTemplate(BaseModel):
    activity_id: Optional[int] = None
    activity_name: str
    curriculum_topic: str
    activity_type: ActivityType
    mode: AIMode
    materials_needed: str
    instructions: str
    safety_notes: str
    duration_minutes: int = Field(..., ge=10, le=60)
    todo_markers: Optional[str] = None
    discussion_prompts: str
    canadian_example: str
    difficulty: DifficultyLevel
    group_size: str
    is_active: bool = True


class CanadianExample(BaseModel):
    example_id: Optional[int] = None
    curriculum_topic: str
    example_title: str
    province_territory: ProvinceTerritory
    description: str
    indigenous_connection: str
    french_connection: str
    visual_description: str
    fun_fact: str
    related_activities: Optional[List[str]] = []


class StoryCharacter(BaseModel):
    character_id: Optional[int] = None
    character_name: str
    character_type: str
    personality_traits: List[str]
    backstory: str
    catchphrase: str
    home_province: ProvinceTerritory
    special_ability: str
    curriculum_connection: List[str]
    visual_description: str


class ContentAdaptation(BaseModel):
    adaptation_id: Optional[int] = None
    base_content_id: str
    learning_style: LearningStyle
    adaptation_type: str
    modified_instructions: str
    additional_supports: List[str]
    time_adjustment: int = Field(default=0, ge=-30, le=30)
    success_modifications: str


class ContentSearchResult(BaseModel):
    query: str
    total_results: int
    results: Dict[str, List[Dict[str, Any]]]


class ActivityWithContext(BaseModel):
    activity: ActivityTemplate
    curriculum_details: Optional[CurriculumTopic] = None
    canadian_example_detail: Optional[CanadianExample] = None
    learning_objectives: Optional[List[LearningObjective]] = []
    adaptations: Optional[List[ContentAdaptation]] = []


class CurriculumContentRequest(BaseModel):
    topic: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    activity_type: Optional[ActivityType] = None
    mode: Optional[AIMode] = None
    province: Optional[ProvinceTerritory] = None
    duration_max: Optional[int] = Field(None, le=60)
    include_adaptations: bool = False
    include_examples: bool = True


class CurriculumContentResponse(BaseModel):
    topics: List[CurriculumTopic]
    activities: List[ActivityTemplate]
    examples: Optional[List[CanadianExample]] = []
    characters: Optional[List[StoryCharacter]] = []
    total_items: int
    cached: bool = False