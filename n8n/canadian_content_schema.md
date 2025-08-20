# Airtable Schema for Canadian Content Sources

## Table: Canadian_Content

This table stores educational content generated from various Canadian data sources.

### Field Definitions

| Field Name | Field Type | Description | Example |
|------------|------------|-------------|---------|
| **record_id** | Autonumber | Auto-generated unique ID | 1, 2, 3... |
| **source_type** | Single select | Type of Canadian data source | "CBC_NEWS", "STATS_CANADA", "ONTARIO_EDU", "CBC_KIDS", "INGENIUM" |
| **source_url** | URL | Original source URL | "https://www.cbc.ca/news/..." |
| **source_title** | Single line text | Original content title | "How planets align in the night sky" |
| **source_category** | Single line text | Content category | "Science", "Technology", "Nature" |
| **source_date** | Date and time | Publication date | 2024-01-15 14:30:00 |
| **simplified_content** | Long text | Grade 4 level explanation | "Six planets are lining up in the sky..." |
| **curriculum_connection** | Long text | Ontario Grade 4 curriculum link | "Science: Earth and Space Systems" |
| **activity_suggestion** | Long text | Hands-on activity | "Create a model solar system using balls..." |
| **canadian_fact** | Long text | Related Canadian fact | "The Northern Lights can be seen from..." |
| **vocabulary_word** | Long text | Key term with definition | "Orbit: the path a planet takes around the sun" |
| **discovery_questions** | Long text | JSON array of questions | ["Why do planets move?", "What makes Earth special?"] |
| **content_score** | Number | Educational value score (0-1) | 0.95 |
| **has_educational_value** | Checkbox | Educational content flag | ✓ |
| **appropriateness_score** | Number | Age appropriateness (0-1) | 1.0 |
| **reading_level** | Single select | Target reading level | "Grade 4", "Grade 3-5" |
| **canadian_context** | Checkbox | Contains Canadian content | ✓ |
| **curriculum_aligned** | Checkbox | Aligns with Ontario curriculum | ✓ |
| **workflow_version** | Single line text | Pipeline version | "cbc-v1.0" |
| **pipeline_timestamp** | Date and time | Processing timestamp | 2024-01-15 14:35:00 |
| **validation_status** | Single select | Content validation status | "Approved", "Pending", "Rejected" |
| **rejection_reason** | Long text | Why content was rejected | "Contains complex political themes" |
| **created_at** | Created time | Auto-generated creation time | (automatic) |
| **updated_at** | Last modified time | Auto-generated update time | (automatic) |

### Additional Metadata Fields

| Field Name | Field Type | Description |
|------------|------------|-------------|
| **subject_areas** | Multiple select | Academic subjects | ["Science", "Math", "Language Arts", "Social Studies"] |
| **skill_focus** | Multiple select | Skills developed | ["Critical Thinking", "Problem Solving", "Observation"] |
| **activity_type** | Multiple select | Type of activity | ["Hands-on", "Discussion", "Research", "Creative"] |
| **materials_needed** | Long text | Required materials | "Paper, pencil, ruler" |
| **time_estimate** | Single select | Activity duration | "5-10 min", "10-20 min", "20-30 min" |
| **season_relevant** | Multiple select | Seasonal relevance | ["Spring", "Summer", "Fall", "Winter", "All Year"] |

## Table: Content_Metrics

Track performance metrics for content generation.

| Field Name | Field Type | Description |
|------------|------------|-------------|
| **metric_id** | Autonumber | Auto-generated ID |
| **date** | Date | Metric date |
| **source_type** | Single select | Data source |
| **total_fetched** | Number | Articles fetched |
| **total_filtered** | Number | After content filtering |
| **total_enriched** | Number | Successfully enriched |
| **total_approved** | Number | Final approved content |
| **rejection_rate** | Formula | (total_filtered - total_approved) / total_filtered |
| **processing_time_avg** | Number | Average processing time (seconds) |
| **api_costs** | Currency | OpenAI API costs |

## Table: Source_Configuration

Store configuration for each data source.

| Field Name | Field Type | Description |
|------------|------------|-------------|
| **config_id** | Autonumber | Auto-generated ID |
| **source_name** | Single line text | Source identifier |
| **source_url** | URL | RSS/API endpoint |
| **fetch_frequency** | Single select | "Hourly", "Every 2 Hours", "Daily" |
| **active** | Checkbox | Is source active |
| **filter_keywords** | Long text | Keywords to filter |
| **priority_keywords** | Long text | Keywords to prioritize |
| **max_items_per_fetch** | Number | Maximum items to process |
| **last_fetch** | Date and time | Last successful fetch |
| **notes** | Long text | Configuration notes |

## Sample Data

### Canadian_Content Record Example
```json
{
  "source_type": "CBC_NEWS",
  "source_url": "https://www.cbc.ca/news/science/planet-parade-1.7611658",
  "source_title": "How to see the 'planet parade' on now",
  "source_category": "Science",
  "source_date": "2024-01-18T16:39:37Z",
  "simplified_content": "Six planets are lining up in the night sky this week! It's like a cosmic parade where Mercury, Venus, Mars, Jupiter, Saturn, and Uranus are all visible at once.",
  "curriculum_connection": "Grade 4 Science - Earth and Space Systems: Students learn about the solar system, planet movements, and celestial observations.",
  "activity_suggestion": "Go outside before dawn with an adult and try to spot the planets! Draw what you see and compare the brightness of each planet.",
  "canadian_fact": "The best viewing locations in Canada are areas with less light pollution, like Jasper National Park - the world's largest Dark Sky Preserve!",
  "vocabulary_word": "Alignment: when objects line up in a straight line or pattern",
  "discovery_questions": [
    "Why do planets appear to line up sometimes?",
    "How can we tell the difference between a planet and a star?",
    "What makes some planets brighter than others?"
  ],
  "content_score": 1.0,
  "has_educational_value": true,
  "appropriateness_score": 1.0,
  "reading_level": "Grade 4",
  "canadian_context": true,
  "curriculum_aligned": true,
  "subject_areas": ["Science"],
  "skill_focus": ["Observation", "Critical Thinking"],
  "activity_type": ["Hands-on", "Research"],
  "time_estimate": "20-30 min",
  "season_relevant": ["Winter"]
}
```

## Implementation Notes

1. **Content Validation Rules**
   - All content must pass appropriateness_score >= 0.8
   - Reading level must be Grade 3-5 range
   - Must have canadian_context = true
   - Rejection rate target < 5%

2. **Data Source Priorities**
   - Phase 1: CBC RSS feeds (News, Science)
   - Phase 2: Statistics Canada API
   - Phase 3: Ontario Education resources
   - Phase 4: CBC Kids content
   - Phase 5: Ingenium Science Collections

3. **Success Metrics**
   - Generate 50+ educational activities weekly
   - Maintain < 5% content rejection rate
   - Ensure 100% Canadian context
   - Achieve Grade 4 reading level compliance

4. **API Rate Limits**
   - CBC RSS: No explicit limit (be respectful)
   - OpenAI: Based on tier (monitor usage)
   - Airtable: 5 requests/second per base
   - Stats Canada: 1000 requests/day

5. **Monitoring Dashboard Fields**
   - Daily content generation count
   - Rejection rate by source
   - Average processing time
   - API cost tracking
   - Content quality scores