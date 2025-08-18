# AI Tutor Prompts Configuration

## Overview

The AI tutor's personality and behavior are configured through the `prompts.yaml` file. This allows for easy customization of the AI's teaching style without modifying code.

## File Structure

```yaml
base_prompt: |
  # The core personality and guidelines for Maple

modes:
  learning:
    name: "Mode Display Name"
    description: "Brief description"
    prompt: |
      # Mode-specific instructions
  
  explanatory:
    # Similar structure
  
  story:
    # Similar structure
  
  discovery:
    # Similar structure

activity_prompt: |
  # Instructions for generating TODO activities
```

## Available Modes

### 1. **Learning Mode** (Socratic Method)
- Guides students through questions rather than direct answers
- Encourages critical thinking and self-discovery
- Best for: Deep understanding and concept exploration

### 2. **Explanatory Mode** (Direct Teaching)
- Provides clear, step-by-step explanations
- Uses analogies and examples
- Best for: When students are confused or stuck

### 3. **Story Mode** (Narrative Learning)
- Teaches through engaging stories and characters
- Makes abstract concepts concrete
- Best for: Memorable learning experiences

### 4. **Discovery Mode** (Exploration)
- Encourages curiosity and wonder
- Open-ended exploration of topics
- Best for: Fostering natural interest in science

## Customization Guide

### Editing Prompts

1. Open `app/prompts.yaml`
2. Modify the relevant section
3. Save the file
4. If DEBUG=true, changes are loaded automatically
5. Otherwise, restart the server

### Adding Custom Modes

To add a new mode:

```yaml
modes:
  custom_mode:
    name: "My Custom Mode"
    description: "Description of what this mode does"
    prompt: |
      Your custom instructions here...
```

Then update `app/models.py` to add the enum value if needed.

### Best Practices

1. **Keep it Grade-Appropriate**: Remember the target audience is Grade 4 (9-10 years old)
2. **Canadian Context**: Include references to Canadian geography, culture, and examples
3. **Encourage Activities**: Use TODO markers for hands-on activities
4. **Positive Reinforcement**: Always be encouraging and celebrate learning

## Environment Variables

- `PROMPTS_FILE_PATH`: Override default prompts.yaml location
- `DEBUG=true`: Enable hot-reloading of prompts

## Development Tips

### Testing Prompt Changes

```python
from app.prompts import reload_prompts, get_system_prompt
from app.models import ConversationMode

# Reload prompts after changes
reload_prompts()

# Get updated prompt
prompt = get_system_prompt(ConversationMode.LEARNING)
print(prompt)
```

### Debug Mode

When `DEBUG=true` in `.env`, prompts reload on every request, allowing real-time testing of changes.

## Examples

### Customizing Maple's Personality

Edit the `base_prompt` section:

```yaml
base_prompt: |
  You are Maple, a friendly and patient AI tutor...
  # Add your customizations here
  - Always use hockey analogies when possible
  - Reference Tim Hortons occasionally
  - Mention Canadian wildlife examples
```

### Adjusting Learning Techniques

Modify mode-specific prompts:

```yaml
modes:
  learning:
    prompt: |
      # Add custom Socratic techniques
      - Start with "I wonder what would happen if..."
      - Use "That's interesting! Why do you think..."
      - Always validate student thinking
```

## Prompt Length Guidelines

- **Base Prompt**: ~1,500 characters
- **Mode Prompts**: ~1,000-1,500 characters each
- **Total Context**: Keep under 4,000 tokens for efficiency

## Related Files

- `app/prompts.py`: Python module that loads and serves prompts
- `app/ai_orchestrator.py`: Uses prompts for mode selection
- `app/models.py`: Defines ConversationMode enum