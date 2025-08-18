import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from app.models import ConversationMode

# Cache for loaded prompts
_prompts_cache: Optional[Dict[str, Any]] = None

def load_prompts() -> Dict[str, Any]:
    """Load prompts from YAML file with caching"""
    global _prompts_cache
    
    if _prompts_cache is not None:
        return _prompts_cache
    
    # Find the prompts.yaml file
    current_dir = Path(__file__).parent
    prompts_file = current_dir / "prompts.yaml"
    
    # Fallback to environment variable if needed
    if not prompts_file.exists():
        prompts_path = os.getenv("PROMPTS_FILE_PATH", str(prompts_file))
        prompts_file = Path(prompts_path)
    
    if not prompts_file.exists():
        raise FileNotFoundError(f"Prompts file not found at {prompts_file}")
    
    with open(prompts_file, 'r', encoding='utf-8') as file:
        _prompts_cache = yaml.safe_load(file)
    
    return _prompts_cache

def reload_prompts():
    """Force reload of prompts from file (useful for development)"""
    global _prompts_cache
    _prompts_cache = None
    return load_prompts()

def get_system_prompt(mode: ConversationMode) -> str:
    """Get the appropriate system prompt based on conversation mode"""
    prompts = load_prompts()
    
    base_prompt = prompts.get('base_prompt', '')
    
    # Map conversation modes to prompt keys
    mode_mapping = {
        ConversationMode.LEARNING: 'learning',
        ConversationMode.EXPLANATORY: 'explanatory',
        ConversationMode.STORY: 'story',
        ConversationMode.DISCOVERY: 'discovery'
    }
    
    mode_key = mode_mapping.get(mode, 'discovery')
    mode_config = prompts.get('modes', {}).get(mode_key, {})
    mode_prompt = mode_config.get('prompt', '')
    
    return base_prompt + "\n\n" + mode_prompt

def get_activity_prompt() -> str:
    """Get prompt for generating TODO activities"""
    prompts = load_prompts()
    return prompts.get('activity_prompt', '')

def get_mode_info(mode: ConversationMode) -> Dict[str, str]:
    """Get mode name and description for a given conversation mode"""
    prompts = load_prompts()
    
    mode_mapping = {
        ConversationMode.LEARNING: 'learning',
        ConversationMode.EXPLANATORY: 'explanatory',
        ConversationMode.STORY: 'story',
        ConversationMode.DISCOVERY: 'discovery'
    }
    
    mode_key = mode_mapping.get(mode, 'discovery')
    mode_config = prompts.get('modes', {}).get(mode_key, {})
    
    return {
        'name': mode_config.get('name', mode.value.title()),
        'description': mode_config.get('description', '')
    }

def get_all_modes() -> Dict[str, Dict[str, str]]:
    """Get information about all available modes"""
    prompts = load_prompts()
    modes = prompts.get('modes', {})
    
    result = {}
    for key, config in modes.items():
        result[key] = {
            'name': config.get('name', key.title()),
            'description': config.get('description', '')
        }
    
    return result

# Convenience functions for getting specific prompts
def get_base_prompt() -> str:
    """Get the base Maple personality prompt"""
    prompts = load_prompts()
    return prompts.get('base_prompt', '')

def get_mode_prompt(mode_key: str) -> str:
    """Get a specific mode prompt by key"""
    prompts = load_prompts()
    mode_config = prompts.get('modes', {}).get(mode_key, {})
    return mode_config.get('prompt', '')

# For development: Hot reload capability
if os.getenv('DEBUG') == 'true':
    # In debug mode, reload prompts on each access
    def get_system_prompt(mode: ConversationMode) -> str:
        reload_prompts()  # Reload in debug mode
        prompts = load_prompts()
        
        base_prompt = prompts.get('base_prompt', '')
        
        mode_mapping = {
            ConversationMode.LEARNING: 'learning',
            ConversationMode.EXPLANATORY: 'explanatory',
            ConversationMode.STORY: 'story',
            ConversationMode.DISCOVERY: 'discovery'
        }
        
        mode_key = mode_mapping.get(mode, 'discovery')
        mode_config = prompts.get('modes', {}).get(mode_key, {})
        mode_prompt = mode_config.get('prompt', '')
        
        return base_prompt + "\n\n" + mode_prompt