# 🍁 Maple AI Tutor - Airtable Content Structure

## Overview
This document outlines the complete Airtable database structure for the Ontario Grade 4 Science curriculum content, focusing on the Light and Sound unit for the v0 MVP.

## Base Configuration

**Base Name**: `Maple_Grade4_Science`
**Primary Focus**: Ontario Grade 4 Science & Technology Curriculum
**Language**: Canadian English
**Reading Level**: Grade 4 (4.0-5.0 Flesch-Kincaid)

## Tables Structure

### 1. Grade4_Science_Curriculum
**Purpose**: Core curriculum mapping aligned with Ontario expectations

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| topic_id | Autonumber | Unique identifier | 1 |
| topic_name | Single line text | Main topic area | "Light" |
| subtopic | Single line text | Specific subtopic | "Properties of Light" |
| curriculum_expectation | Long text | Ontario expectation code | "3.1 - Identify sources of light" |
| description | Long text | Student-friendly description | "Learn how light travels and bounces off objects" |
| key_concepts | Multiple select | Core concepts covered | ["reflection", "refraction", "light sources"] |
| difficulty_level | Single select | Complexity level | "Introductory" |
| prerequisite_topics | Link to another record | Required prior knowledge | [Link to "Energy Sources"] |
| canadian_connection | Long text | Canadian context | "Northern Lights in Yukon" |
| indigenous_perspective | Long text | Indigenous knowledge | "Traditional use of sunlight for navigation" |
| estimated_duration | Number | Learning time in minutes | 30 |

### 2. Learning_Objectives
**Purpose**: Detailed learning outcomes with Bloom's taxonomy alignment

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| objective_id | Autonumber | Unique identifier | 1 |
| curriculum_topic | Link to Grade4_Science_Curriculum | Related topic | [Link to "Light Properties"] |
| objective_text | Long text | Learning outcome | "Students will identify natural and artificial light sources" |
| bloom_level | Single select | Bloom's taxonomy level | "Understanding" |
| success_criteria | Long text | How to measure success | "Can list 5+ light sources and categorize them" |
| assessment_type | Multiple select | Assessment methods | ["observation", "discussion", "hands-on"] |
| skills_developed | Multiple select | Skills practiced | ["critical thinking", "observation", "classification"] |

### 3. Activity_Templates
**Purpose**: Hands-on learning activities with TODO markers

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| activity_id | Autonumber | Unique identifier | 1 |
| activity_name | Single line text | Activity title | "Rainbow Creation Lab" |
| curriculum_topic | Link to Grade4_Science_Curriculum | Related topic | [Link to "Light Properties"] |
| activity_type | Single select | Type of activity | "Experiment" |
| mode | Single select | AI interaction mode | "learning" |
| materials_needed | Long text | Required materials | "Glass of water, flashlight, white paper, mirror" |
| instructions | Long text | Step-by-step guide | "TODO(student): Fill glass with water..." |
| safety_notes | Long text | Safety considerations | "Adult supervision for handling glass" |
| duration_minutes | Number | Time required | 20 |
| todo_markers | Long text | Student tasks | "TODO(student): Observe and draw the rainbow pattern" |
| discussion_prompts | Long text | Thinking questions | "Why do you think the light splits into colors?" |
| canadian_example | Long text | Local connection | "Like rainbows over Niagara Falls" |
| difficulty | Single select | Challenge level | "Beginner" |
| group_size | Single select | Individual/group | "Individual or pairs" |

### 4. Canadian_Examples
**Purpose**: Canadian-specific content and cultural connections

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| example_id | Autonumber | Unique identifier | 1 |
| curriculum_topic | Link to Grade4_Science_Curriculum | Related topic | [Link to "Sound Waves"] |
| example_title | Single line text | Example name | "Thunder over Lake Superior" |
| province_territory | Single select | Location | "Ontario" |
| description | Long text | Detailed explanation | "Thunder echoes across the Great Lakes..." |
| indigenous_connection | Long text | Indigenous perspective | "Ojibwe thunder teachings" |
| french_connection | Long text | French-Canadian aspect | "Tonnerre sur le fleuve Saint-Laurent" |
| visual_description | Long text | For image generation | "Lightning over Canadian Shield forest" |
| fun_fact | Long text | Interesting detail | "Lake Superior can create its own weather!" |
| related_activities | Link to Activity_Templates | Connected activities | [Links to relevant activities] |

### 5. Story_Characters
**Purpose**: Characters for narrative/story mode

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| character_id | Autonumber | Unique identifier | 1 |
| character_name | Single line text | Character name | "Maple the Beaver" |
| character_type | Single select | Role | "Main Guide" |
| personality_traits | Multiple select | Character traits | ["curious", "helpful", "brave"] |
| backstory | Long text | Character background | "Lives near Algonquin Park..." |
| catchphrase | Single line text | Signature phrase | "Let's explore, eh!" |
| home_province | Single select | Location | "Ontario" |
| special_ability | Single line text | Unique skill | "Can sense vibrations through water" |
| curriculum_connection | Multiple select | Topics they help with | ["Sound", "Vibrations", "Water"] |
| visual_description | Long text | For consistency | "Brown beaver with maple leaf marking" |

### 6. Content_Adaptations
**Purpose**: Alternative content for different learning styles

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| adaptation_id | Autonumber | Unique identifier | 1 |
| base_content | Link to Activity_Templates | Original activity | [Link to activity] |
| learning_style | Single select | Target style | "Visual" |
| adaptation_type | Single select | Modification type | "Simplified" |
| modified_instructions | Long text | Adapted instructions | "Use pictures instead of written steps..." |
| additional_supports | Multiple select | Extra help needed | ["visual aids", "movement breaks"] |
| time_adjustment | Number | Extra time needed | 10 |
| success_modifications | Long text | Adjusted expectations | "Complete 3 of 5 steps independently" |

## Content Requirements

### Curriculum Coverage
- **Light Unit Topics**:
  - Properties of light
  - Natural vs artificial light sources
  - How light travels
  - Reflection and mirrors
  - Shadows and opacity
  - Colors and prisms
  - Light and materials (transparent, translucent, opaque)

- **Sound Unit Topics**:
  - Properties of sound
  - How sound travels
  - Vibrations and sound production
  - Pitch and volume
  - Musical instruments
  - Echo and sound reflection
  - Sound and materials

### Canadian Content Requirements
- Representation from all 13 provinces/territories
- Minimum 20 Canadian examples per major topic
- Indigenous perspectives for each unit
- French-Canadian cultural connections
- Regional diversity (urban, rural, northern)

### Activity Requirements
- 15+ hands-on activities minimum
- Materials from common household items
- Clear TODO(student) markers
- Safety notes for each activity
- Time estimates (10-30 minutes typically)
- Both individual and group options

### Story Mode Requirements
- 5+ recurring characters
- Canadian settings and contexts
- Curriculum-aligned adventures
- Decision points for students
- Characters from diverse backgrounds

## API Integration Fields

### System Fields (All Tables)
| Field Name | Type | Description |
|------------|------|-------------|
| created_at | Created time | Record creation timestamp |
| updated_at | Last modified time | Last update timestamp |
| is_active | Checkbox | Whether content is live |
| review_status | Single select | "Draft", "Review", "Approved" |
| notes | Long text | Internal notes |

## Content Guidelines

### Language Requirements
- Grade 4 reading level (ages 9-10)
- Canadian spelling (colour, centre, favourite)
- Metric measurements only
- Positive, encouraging tone
- Avoid complex scientific jargon

### Cultural Sensitivity
- Include diverse Canadian perspectives
- Respect Indigenous knowledge systems
- Acknowledge French-Canadian heritage
- Represent newcomer experiences
- Include accessibility considerations

### Safety Standards
- All activities must be safe for Grade 4 students
- Clear safety warnings where needed
- Adult supervision notes when required
- No dangerous chemicals or tools
- Consider allergies and sensitivities

## Implementation Notes

### Phase 1: Core Content (Days 1-2)
1. Create base and tables
2. Populate Grade4_Science_Curriculum with Light & Sound
3. Add 20+ Canadian examples
4. Create 15+ activity templates

### Phase 2: Enhancement (Day 2-3)
1. Add story characters
2. Create content adaptations
3. Link all relationships
4. Review and validate content

### API Access Setup
```python
# Required environment variables
AIRTABLE_API_KEY=your_key_here
AIRTABLE_BASE_ID=base_id_here

# API endpoints needed
GET /v0/{baseId}/{tableName}
POST /v0/{baseId}/{tableName}
PATCH /v0/{baseId}/{tableName}/{recordId}
```

## Success Metrics
- ✅ 100% curriculum expectation coverage
- ✅ All 13 provinces/territories represented
- ✅ 20+ Canadian examples per topic
- ✅ 15+ hands-on activities
- ✅ Reading level 4.0-5.0
- ✅ Safety review completed
- ✅ API integration tested