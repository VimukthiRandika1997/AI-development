"""Schema definitions for requests and responses """

from pydantic import BaseModel
from typing import List, Optional


class Ingredient(BaseModel):
    ingredient: str
    amount: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None


class Step(BaseModel):
    step_number: int
    instruction: str
    explanation: str


class Recipe(BaseModel):
    recipe_title: str
    ingredients: List[Ingredient]
    cooking_time: Optional[str]
    cooking_temperature: Optional[str]
    steps: List[Step]
    tips: List[str] = []


class SpooncularRecipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str 
    cookingTechniques: List[str]
    readyInMinutes: Optional[int] = None
    servings: Optional[int] = None
    

class Turn(BaseModel):
    turn_id: int
    user: Optional[str] = None
    bot: Optional[str] = None


class SessionState(BaseModel):
    session_id: str
    chat: List[Turn] = []
    delay_count: int = 0
    ingredients_on_hand: List[str] = []
    cuisine_pref: Optional[str] = None
    dietary_rules: List[str] = []
    equipment: List[str] = []
    time_budget_minutes: Optional[int] = None
    skill_level: Optional[str] = None
    servings: Optional[int] = None
    flavor_prefs: List[str] = []
    missing_slots: List[str] = []