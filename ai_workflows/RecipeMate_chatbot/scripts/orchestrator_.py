"""Core orchestrator for handling operations"""

from api.schemas import SessionState, Recipe
from api.services.memory import get_state, set_state
from api.services.llm_gemini import ask_gemini
from api.tools import spoonacular as spoon
from api.tools.culinary_rules import adjust_with_rules


async def handle_turn(session_id: str, user_utterance: str):
    """handles the moment of the session's conversation"""

    state = await get_state(session_id)

    # simple heuristic: parse ingredients
    if "ingredients" in user_utterance.lower():
        state.ingredients_on_hand.extend(user_utterance.lower().split()[1:])
    await set_state(session_id, state)

    resp = await ask_gemini("ask_questions", state.model_dump())

    # check whether in state contains ingredients_on_hand or not
    # if it doesn't then fallback to answering the questions from the user
    if "questions" in resp:
        return {"bot_message": "\n".join(resp["questions"]), 
                "state_snapshot": state.model_dump()}
    
    return {"bot_message": "Ready to draft recipe?", 
            "state_snapshot": state.model_dump()}


async def generate_recipe(session_id: str) -> Recipe:
    """Generate a recipe using the LLM based on the state in the session"""
    
    state = await get_state(session_id)
    resp = await ask_gemini("draft_recipe", state.model_dump())
    print("*****")
    print(resp)
    print("*****")
    draft = Recipe.model_validate(resp.get("draft_recipe"))

    return draft

    # Validation calls
    # sim = await spoon.search_similar(draft.ingredients, state.cuisine_pref)
    # subs = [await spoon.substitutions(i.ingredient) for i in draft.ingredients]
    # nutrition = await spoon.nutrition(draft.ingredients)
    # analyzed = await spoon.analyze_recipe(draft)

    # validated = adjust_with_rules(draft, sim, nutrition, analyzed)

    # return validated


async def validate_recipe(recipe: Recipe) -> dict:
    """Validate a given recipe"""

    sim = await spoon.search_similar(recipe.ingredients, None)
    nutrition = await spoon.nutrition(recipe.ingredients)
    analyzed = await spoon.analyze_recipe(recipe)
    corrected = adjust_with_rules(recipe, sim, nutrition, analyzed)

    return {"recipe": corrected, "validation_report": {
            "similar_found": bool(sim),
            "nutrition_ok": bool(nutrition),
            "analysis_ok": bool(analyzed)}}
