# Curriculum Content System

## Overview

The curriculum content system provides structured access to Ontario Grade 4 Science curriculum data stored in Airtable. This system delivers curriculum-aligned content, activities, Canadian examples, and narrative characters to support the Maple AI Tutor's educational objectives.

## Architecture

### Data Storage
- **Platform**: Airtable
- **Base ID**: Configured via environment variable `AIRTABLE_BASE_ID`
- **API Access**: Personal Access Token (PAT) with full token format
- **Caching**: In-memory caching with JSON file fallback
- **Integration**: Content fetched during chat when topics detected

### Database Schema

The Airtable base consists of 6 interconnected tables:

#### 1. Grade4_Science_Curriculum
Primary curriculum content aligned with Ontario expectations.

**Note**: Table uses underscore format, field names use spaces (e.g., "Topic Name")

| Field | Type | Description |
|-------|------|-------------|
| Topic Name | Single line text | Main topic (e.g., "Light", "Sound") |
| subtopic | Single line text | Specific subtopic |
| curriculum_expectation | Long text | Ontario curriculum code and expectation |
| description | Long text | Topic description |
| key_concepts | Multiple select | Core concepts to learn |
| difficulty_level | Single select | Introductory/Intermediate/Advanced |
| prerequisite_topics | Link to records | Required prior knowledge |
| canadian_connection | Long text | Canadian context and examples |
| indigenous_perspective | Long text | Indigenous knowledge integration |
| estimated_duration | Number | Minutes for lesson |
| is_active | Checkbox | Content availability flag |

#### 2. Learning_Objectives
Specific learning goals linked to curriculum topics.

| Field | Type | Description |
|-------|------|-------------|
| curriculum_topic | Link to records | Related curriculum topic |
| objective_text | Long text | Learning objective statement |
| bloom_level | Single select | Bloom's taxonomy level |
| success_criteria | Long text | How to measure achievement |
| assessment_type | Multiple select | Assessment methods |
| skills_developed | Multiple select | Skills practiced |

#### 3. Activity_Templates
Hands-on activities with TODO markers for student engagement.

| Field | Type | Description |
|-------|------|-------------|
| activity_name | Single line text | Activity title |
| curriculum_topic | Single line text | Related topic |
| activity_type | Single select | Type of activity |
| mode | Single select | AI interaction mode |
| materials_needed | Long text | Required materials |
| instructions | Long text | Step-by-step instructions with TODO markers |
| safety_notes | Long text | Safety considerations |
| duration_minutes | Number | Activity duration |
| discussion_prompts | Long text | Reflection questions |
| canadian_example | Long text | Canadian context |
| difficulty | Single select | Difficulty level |
| group_size | Single line text | Individual/pairs/group |

#### 4. Canadian_Examples
Real-world Canadian examples for contextual learning.

| Field | Type | Description |
|-------|------|-------------|
| curriculum_topic | Single line text | Related topic |
| example_title | Single line text | Example name |
| province_territory | Single select | Location in Canada |
| description | Long text | Detailed description |
| indigenous_connection | Long text | Indigenous perspectives |
| french_connection | Long text | French-Canadian connections |
| visual_description | Long text | Visual description for AI |
| fun_fact | Long text | Engaging fact |
| related_activities | Link to records | Connected activities |

#### 5. Story_Characters
Narrative mode characters for storytelling engagement.

| Field | Type | Description |
|-------|------|-------------|
| character_name | Single line text | Character's name |
| character_type | Single select | Role in stories |
| personality_traits | Multiple select | Character traits |
| backstory | Long text | Character background |
| catchphrase | Single line text | Signature phrase |
| home_province | Single select | Canadian province/territory |
| special_ability | Long text | Unique abilities |
| curriculum_connection | Multiple select | Related topics |
| visual_description | Long text | Appearance description |

#### 6. Content_Adaptations
Modified content for different learning styles.

| Field | Type | Description |
|-------|------|-------------|
| base_content | Link to records | Original activity |
| learning_style | Single select | Visual/Auditory/Kinesthetic/Reading-Writing |
| adaptation_type | Single line text | Type of modification |
| modified_instructions | Long text | Adapted instructions |
| additional_supports | Multiple select | Extra resources |
| time_adjustment | Number | Time modification (minutes) |
| success_modifications | Long text | Adjusted success criteria |

## API Endpoints

### Base URL
```
/api/content
```

### Available Endpoints

#### GET /curriculum/topics
Retrieve curriculum topics with optional filtering.

**Query Parameters:**
- `topic` (optional): Filter by topic name

**Response:**
```json
{
  "data": {
    "topic": "Light",
    "content": "Light travels in straight lines...",
    "grade_level": "Grade 4",
    "learning_objectives": [...],
    "key_concepts": [...],
    "canadian_examples": [...]
  },
  "cached": false
}
```

#### GET /activities
Get activities for a specific curriculum topic.

**Query Parameters:**
- `topic` (required): Curriculum topic name

**Response:**
```json
{
  "data": [
    {
      "name": "Rainbow Creation Lab",
      "description": "Create rainbows using water and light",
      "materials": ["Glass", "Water", "Flashlight"],
      "steps": ["Fill glass...", "TODO(student): ..."],
      "learning_outcome": "Understanding refraction"
    }
  ],
  "count": 5
}
```

#### GET /canadian-examples
Retrieve Canadian examples for a topic.

**Query Parameters:**
- `topic` (required): Curriculum topic

**Response:**
```json
[
  "Northern Lights in Yukon",
  "Sunrise over Lake Ontario",
  "Reflections on Lake Louise"
]
```

#### GET /health
Check Airtable service health status.

**Response:**
```json
{
  "status": "healthy",
  "airtable_connected": true,
  "cache_size": 6,
  "last_refresh": "2025-08-18T12:00:00Z"
}
```

## Service Implementation

### AirtableService Class

Located at: `backend/app/airtable_service.py`

Key methods:
- `initialize()`: Connect to Airtable API
- `get_content_for_topic(topic)`: Retrieve curriculum content
- `get_activities(topic)`: Get topic-specific activities
- `get_canadian_examples(topic)`: Fetch Canadian examples
- `check_health()`: Verify service connectivity

### Caching Strategy

- **TTL**: Configurable via `CACHE_TTL_SECONDS` (default: 3600)
- **Strategy**: In-memory caching with automatic expiration
- **Invalidation**: Manual cache clearing via API endpoint

### Error Handling

The service includes comprehensive error handling:
- **Fallback Content**: Static content when Airtable is unavailable
- **Graceful Degradation**: Service continues with cached/fallback data
- **Logging**: All errors logged for monitoring

## Content Management

### Adding New Content

Content creators can add new curriculum content directly in Airtable:

1. **Curriculum Topics**: Add to Grade4_Science_Curriculum table
2. **Activities**: Create in Activity_Templates with TODO markers
3. **Examples**: Add to Canadian_Examples with provincial context
4. **Characters**: Define in Story_Characters for narrative mode

### Content Guidelines

#### Activity Instructions
Include TODO markers for student actions:
```
TODO(student): Fill a glass with water
TODO(student): Shine the flashlight through the glass
TODO(student): Draw what you observe
```

#### Canadian Context
Every topic should include:
- Provincial/territorial examples
- Indigenous perspectives
- French-Canadian connections
- Local phenomena or landmarks

#### Difficulty Levels
- **Introductory**: Basic concepts, 15-25 minutes
- **Intermediate**: Applied learning, 25-35 minutes
- **Advanced**: Complex exploration, 35-45 minutes

## Integration with AI Orchestrator

### Content Flow in Chat
1. **User Message**: "Can you help me understand how light works?"
2. **Topic Extraction**: AI orchestrator detects "light" topic
3. **Content Fetching**: System fetches:
   - Curriculum data (learning objectives, key concepts)
   - Activities (Shadow Puppet Theatre)
   - Canadian examples (Northern Lights, Lake Ontario)
4. **LLM Context**: Content passed to Claude/OpenAI as context
5. **Natural Integration**: LLM weaves content into response:
   - "Speaking of reflections, have you ever heard of the Northern Lights..."
   - "Now, how about we try an activity to see how light and shadows work..."
6. **Metadata Response**: Structured data returned for frontend use

### Authentication Configuration
```env
# Full PAT format required
AIRTABLE_API_KEY=pat[prefix].[suffix]
AIRTABLE_BASE_ID=app[id]
```

## Current Implementation Status
- ✅ Airtable authentication fixed (full PAT token)
- ✅ Table names corrected (Grade4_Science_Curriculum)
- ✅ Field mappings updated (Topic Name with space)
- ✅ Content APIs exposed and functional
- ✅ Natural content integration in LLM responses
- ✅ Fallback content for resilience

The curriculum content integrates with the AI orchestrator to:

1. **Mode Selection**: Choose appropriate AI mode based on content type
2. **Context Provision**: Supply relevant Canadian examples
3. **Activity Guidance**: Provide structured activities with TODO markers
4. **Assessment Support**: Offer success criteria and evaluation methods

## Environment Configuration

Required environment variables:

```bash
# Airtable Configuration
AIRTABLE_API_KEY=pat****  # Personal Access Token
AIRTABLE_BASE_ID=app****  # Base identifier

# Cache Settings
CACHE_TTL_SECONDS=3600    # Cache duration
```

## Testing

### Manual Testing
1. Verify Airtable connectivity: `GET /api/content/health`
2. Test topic retrieval: `GET /api/content/curriculum/topics?topic=light`
3. Check activities: `GET /api/content/activities?topic=sound`
4. Validate examples: `GET /api/content/canadian-examples?topic=light`

### Automated Tests
```bash
pytest backend/tests/test_airtable_service.py
pytest backend/tests/test_content_api.py
```

## Monitoring

### Key Metrics
- API response times
- Cache hit/miss ratios
- Airtable API quota usage
- Error rates by endpoint

### Health Checks
- Periodic connectivity verification
- Content availability monitoring
- Cache performance tracking

## Troubleshooting

### Common Issues

#### Airtable Connection Failed
- Verify API key is valid
- Check base ID is correct
- Ensure network connectivity
- Validate API scopes

#### Empty Content Response
- Confirm table names match schema
- Check field names in Airtable
- Verify content is marked as active
- Review filter formulas

#### Cache Issues
- Clear cache via API endpoint
- Check TTL configuration
- Monitor memory usage
- Verify cache key generation

## Future Enhancements

### Planned Features
1. **Multi-language Support**: French content translations
2. **Adaptive Difficulty**: Dynamic difficulty adjustment
3. **Progress Tracking**: Student progress monitoring
4. **Content Versioning**: Track content changes
5. **Offline Mode**: Local content caching

### Content Expansion
- Additional grade levels (3-6)
- More science units
- Cross-curricular connections
- Seasonal activities
- Virtual field trips

## References

- [Ontario Science Curriculum Grade 4](https://www.dcp.edu.gov.on.ca/en/curriculum/science-technology/grades/4)
- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Indigenous Ways of Knowing](https://www.oise.utoronto.ca/abed/indigenous-ways-of-knowing/)