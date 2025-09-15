import os, httpx
from api.schemas import Ingredient, Recipe
from typing import List, Optional

BASE = "https://api.spoonacular.com"
KEY = os.environ["SPOONACULAR_API_KEY"]


async def fetch_recipes(
    state_dict: dict
):
    """
    Search for recipes based on user inputs.
    """
    
    url = f"{BASE}/recipes/complexSearch"
    params = {
        "apiKey": KEY,
        "number": 1, # get only one recipe for now!
    }

    # fact checking: #! adding some combinations (like maxReadyTime, minServing) could result empty response from the api
    if state_dict.get("ingredients_on_hand", None):
        params["includeIngredients"] = ",".join(state_dict["ingredients_on_hand"])
    if state_dict.get("cuisine_pref", None):
        params["cuisine"] = state_dict["cuisine_pref"]
    # if state_dict.get("dietary_rules", None):
    #     params["diet"] = state_dict["dietary_rules"][0]
    if state_dict.get("equipment", None):
        params["equipment"] = state_dict["equipment"]
    # if state_dict.get("time_budget_minutes", None):
    #     params["maxReadyTime"] = int(state_dict["time_budget_minutes"])
    # if state_dict.get("servings", None):
    #     params["minServings"] = state_dict["servings"]
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("results", [])


async def get_recipe_information(recipe_id: int):
    """
    Get detailed recipe info including cooking techniques, prep times, etc.
    """
    url = f"{BASE}/recipes/{recipe_id}/information"
    params = {"apiKey": KEY}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    return {
        "title": data.get("title"),
        "readyInMinutes": data.get("readyInMinutes"),
        "servings": data.get("servings"),
        "instructions": data.get("instructions"),
        "cookingTechniques": [
            step.get("step") for analyzed in data.get("analyzedInstructions", [])
            for step in analyzed.get("steps", [])
            if step.get("step")
        ],
        "ingredients": [
            ing.get("original") for ing in data.get("extendedIngredients", [])
        ]
    }


async def search_similar(ingredients: list[Ingredient], cuisine: str | None = None):
    """Search for similar recipe based on ingredients and cusine"""

    q = ",".join([i.ingredient for i in ingredients])
    params = {"apiKey": KEY, "includeIngredients": q, "number": 3}
    if cuisine:
        params["cuisine"] = cuisine
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE}/recipes/complexSearch", params=params)
        return r.json()


async def substitutions(ingredient: str):
    """Loook up for ingredient substitution"""

    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE}/food/ingredients/substitutes", 
                             params={"apiKey": KEY, "ingredientName": ingredient})
        return r.json()


async def nutrition(ingredients: list[Ingredient]):
    """Retrieve nutritional information"""

    # Spoonacular wants formatted strings like "2 cups rice"
    ing_str = [f"{i.amount or ''} {i.unit or ''} {i.ingredient}".strip()
               for i in ingredients]
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/recipes/parseIngredients",
                              params={"apiKey": KEY, "includeNutrition": "true"},
                              json=ing_str)
        return r.json()


async def analyze_recipe(recipe: Recipe):
    """Analyze and validate a recipe"""    

    payload = {
        "title": recipe.recipe_title,
        "ingredients": [f"{i.amount or ''} {i.unit or ''} {i.ingredient}".strip()
                        for i in recipe.ingredients],
        "instructions": [s.instruction for s in recipe.steps]
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/recipes/analyze", params={"apiKey": KEY}, json=payload)
        return r.json()
