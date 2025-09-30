import os
from pydantic import BaseModel
from functools import lru_cache

class Setting(BaseModel):
    GOOGLE_API_KEY : str = os.getenv("GOOGLE_API_KEY ")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


@lru_cache
def get_settings():
    return Setting()