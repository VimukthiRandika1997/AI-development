"""Configurations for the API"""

import os
from pydantic import BaseModel

class Settings(BaseModel):

    API_VERSION: str = os.environ["API_VERSION"]

    GEMINI_API_KEY: str = os.environ["GEMINI_API_KEY"]
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    SPOONACULAR_API_KEY: str = os.environ["SPOONACULAR_API_KEY"]
    SPOONACULAR_BASE: str = "https://api.spoonacular.com"

    DELAY_WAITS: int = 4 # No.of waites before generating a recipe