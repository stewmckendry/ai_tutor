from pydantic_settings import BaseSettings
from typing import List, Optional
import json


class Settings(BaseSettings):
    claude_api_key: str
    openai_api_key: str
    airtable_api_key: str
    airtable_base_id: str
    
    allowed_origins: List[str] = ["http://localhost:3000"]
    debug: bool = True
    
    app_name: str = "Grade 4 AI Tutor"
    app_version: str = "0.1.0"
    
    session_ttl_minutes: int = 60
    max_conversation_length: int = 50
    
    cache_ttl_seconds: int = 300
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "allowed_origins":
                try:
                    return json.loads(raw_val)
                except json.JSONDecodeError:
                    return [raw_val]
            return raw_val


settings = Settings()