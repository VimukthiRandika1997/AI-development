import os
import httpx
from typing import List, Dict, Any, Optional

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com"


# ------------------------------
# 1. Fetch recipes matching user inputs
# ------------------------------
async def fetch_recipes(
    ingredients: Optional[List[str]] = None,
    cuisine: Optional[str] = None,
    diet: Optional[str] = None,
    number: int = 1,
) -> List[Dict[str, Any]]:
    """
    Search for recipes based on user inputs.
    """
    url = f"{BASE_URL}/recipes/complexSearch"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "number": number,
    }
    if ingredients:
        params["includeIngredients"] = ",".join(ingredients)
    if cuisine:
        params["cuisine"] = cuisine
    if diet:
        params["diet"] = diet

    print("*****************")
    print(params)
    print("*****************")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("results", [])


# ------------------------------
# 2. Retrieve cooking techniques and preparation times
# ------------------------------
async def get_recipe_information(recipe_id: int) -> Dict[str, Any]:
    """
    Get detailed recipe info including cooking techniques, prep times, etc.
    """
    url = f"{BASE_URL}/recipes/{recipe_id}/information"
    params = {"apiKey": SPOONACULAR_API_KEY}

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


# ------------------------------
# 3. Retrieve ingredient pairings
# ------------------------------
async def get_ingredient_pairings(ingredient: str) -> Dict[str, Any]:
    """
    Get ingredient pairings (what goes well with a given ingredient).
    """
    url = f"{BASE_URL}/food/ingredients/{ingredient}/information"
    params = {"apiKey": SPOONACULAR_API_KEY, "amount": 1}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    return {
        "ingredient": data.get("name"),
        "pairings": data.get("pairings", []),
        "flavors": data.get("flavors", {}),
    }


import asyncio

async def main():
    # Fetch recipes
    recipes = await fetch_recipes(ingredients=["chicken", "butter"])
    print("Recipes:", recipes)

    # Get recipe info
    if recipes:
        recipe_id = recipes[0]["id"]
        info = await get_recipe_information(recipe_id)
        print("Recipe Info:", info)

    # # Ingredient pairings
    # pairings = await get_ingredient_pairings("tomato")
    # print("Pairings:", pairings)


if __name__ == "__main__":
    asyncio.run(main())

# {'apiKey': 'ce4f136685c24c88bc3a312c319cc055', 'number': 1, 'includeIngredients': 'chicken,butter'}
# {'apiKey': 'ce4f136685c24c88bc3a312c319cc055', 'number': 1, 'includeIngredients': 'chicken,curry', 'cuisine': 'indian', 'maxReadyTime': 10}