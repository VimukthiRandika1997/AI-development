from api.schemas import Recipe

SAFE_TEMPS = {
    "chicken": 74,   # Celsius
    "pork": 63,
    "beef": 63
}

def adjust_with_rules(recipe: Recipe, sim: dict, nutrition: dict, analyzed: dict) -> Recipe:
    # Example: Ensure chicken isn’t below safe temp
    if "chicken" in [i.ingredient for i in recipe.ingredients]:
        if recipe.cooking_temperature:
            try:
                temp_val = int("".join([c for c in recipe.cooking_temperature if c.isdigit()]))
                if temp_val < SAFE_TEMPS["chicken"]:
                    recipe.cooking_temperature = f"{SAFE_TEMPS['chicken']} °C"
            except:
                recipe.cooking_temperature = f"{SAFE_TEMPS['chicken']} °C"
    # Add a nutrition tip
    if nutrition:
        cal = sum([i.get("nutrition", {}).get("nutrients", [{}])[0].get("amount", 0)
                   for i in nutrition if "nutrition" in i])
        recipe.tips.append(f"Approx calories: {int(cal)} kcal per serving")
    return recipe
