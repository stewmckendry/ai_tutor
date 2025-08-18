from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional, Union
import json


class Settings(BaseSettings):
    claude_api_key: str = Field(default="")
    openai_api_key: str = Field(default="")
    airtable_api_key: str = Field(default="")
    airtable_base_id: str = Field(default="")
    
    allowed_origins: Union[List[str], str] = Field(default='["http://localhost:3000", "http://localhost:5173"]')
    debug: bool = True
    port: int = Field(default=8000)
    
    app_name: str = "Grade 4 AI Tutor"
    app_version: str = "0.1.0"
    
    session_ttl_minutes: int = 60
    max_conversation_length: int = 50
    
    cache_ttl_seconds: int = 300
    
    @validator('allowed_origins', pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()