from functools import lru_cache
from pydantic import BaseSettings

# Environment setting 
class ConfigSettings(BaseSettings):
    env_name : str = "local"
    base_url : str = "http://127.0.0.1:8000/"
    db_url = str = "sqlite:///shortened_url.db"
    class config:
        env_file = ".env"

@lru_cache(maxsize=16)
def base_settings() -> ConfigSettings:
    settings = ConfigSettings()
    print(f"Loading settings for:{settings.env_name}")
    return settings
