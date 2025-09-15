"""Core Orchestrator for handling Chatbot's Operations"""

from copy import deepcopy
from loguru import logger
from api.schemas import SessionState, Recipe, SpooncularRecipe, Ingredient, Step
from api.services.memory import (
    get_state, 
    add_user_utterance, 
    add_bot_response, 
    update_session_state,
    update_delay_count,
    reset_delay_count
)
from api.services.llm_gemini import parse_user_intent_using_gemini, ask_dynamic_question_from_gemini, innovate_new_recipe_using_gemini
from api.tools import spoonacular as spoon
from api.tools.culinary_rules import adjust_with_rules
from api.config.settings import Settings


# -----------------------------
# Helper functions: Handling custom business logics
# -----------------------------

def is_ready_for_recipe(user_intent_state: dict) -> bool:
    """Decide if the user has provided enough information to generate a recipe"""

    #! consider only a few topics for now!!!
    slots_to_consider = ["ingredients_on_hand", 
                         "dietary_rules", 
                         "equipment", 
                         "time_budget_minutes", 
                         ]
    
    for topic in slots_to_consider:
        current_value = user_intent_state[topic]
        if isinstance(current_value, list): # at least 3 ingredient + 1 constraints
            if len(user_intent_state["ingredients_on_hand"]) >= 3 and len(user_intent_state["dietary_rules"]) >= 1: 
                return True
        elif current_value is not None:
            return True
    return False


async def dynamic_question_handle(session_id: str):
    """Ask dynamic questions from the user based on current session state"""

    state = await get_state(session_id)
    return await ask_dynamic_question_from_gemini(mode="ask_follow_up_questions", payload=state.model_dump())


############ - Orchestrator - ##################
# ----------------------------------------------
# Conversation Handling: Chaining the operations
#   1. Parsing User Intention
#   2. Dynamic Questioning
#   3. API calling for recipe generation
#   4. LLM calling for recipe innovation
#   5. API calling for recipe validation
# ----------------------------------------------
async def handle_turn(session_id: str, user_utterance: str):
    """handles the moment of the session's conversation/chat"""

    logger.info("Storing the initial session data")
    state = await get_state(session_id)                             # get the session data, if doesn't  exit, then create a new session
    state = await add_user_utterance(session_id, user_utterance)    # save the session data in memory-bank
    print("delay_count", state.delay_count)
    logger.success("Storing event is successful...")

    # Step 1: parse the user-intent
    logger.info("Parsing the user-intention using the LLM...")
    resp = await parse_user_intent_using_gemini("parse_user_intent", state.model_dump())
    logger.success("Parsing event is successfull!!!")

    logger.info("Updating the session data...")
    await update_session_state(session_id, resp["user_intent"]) # update the session metadata in the memory-bank
    logger.success("Updating session event is successfull!!!")
    updated_state = await get_state(session_id) 

    # Step 2: check for readiness
    user_intent_state = deepcopy(updated_state).model_dump()
    del user_intent_state["session_id"]

    if Settings().DELAY_WAITS <= updated_state.delay_count:
        if is_ready_for_recipe(user_intent_state=user_intent_state):
            logger.info("Started generating a recipe...")
            msg = "Great!, I have enough details, Let me create your recipe!"
            await add_bot_response(session_id, msg)

            # call the API for creating a recipe
            recipe = await generate_recipe(session_id=session_id) 

            # call the llm to innovate a recipe
            new_recipe = await innovate_recipe(spooncular_recipe=recipe) 

            await reset_delay_count(session_id=session_id)

            #! validate the new recipe with the API for fact-check
            return {"bot_message": msg, "recipe": new_recipe.model_dump()}

    # Step 3: otherwise ask clarifying questions from the user
    logger.info("Asking dynamic follow-up questions...")
    resp_follow_up = await dynamic_question_handle(session_id=session_id)
    logger.success("Asking dynamic is successful!!!")

    await update_delay_count(session_id=session_id)

    logger.info("Saving bot response to the session state...")
    await add_bot_response(session_id, resp_follow_up["question"]) # save the bot's response in the memory-bank
    logger.success("Saving bot response is successful!!!")

    return {"bot_message": resp_follow_up["question"]}


async def generate_recipe(session_id: str) -> SpooncularRecipe:
    """Generate a recipe using the Spooncular API based on the user-intent"""
    
    state = await get_state(session_id)
    state_obj = state.model_dump()
    del state_obj["session_id"]
    del state_obj["chat"]
    del state_obj["missing_slots"]

    # call the spooncular api to generate a recipe
    recipes = await spoon.fetch_recipes(state_obj)
    if recipes:
        recipe_id = recipes[0]["id"]
        info = await spoon.get_recipe_information(recipe_id)
        logger.info("Recipe Info:", info)
    else:
        info = {
            "title": "",
            "ingredients": [],
            "instructions": "",
            "cookingTechniques": [],
        }
        logger.error("Recipe generation using Spooncular API failed!!!")

    return SpooncularRecipe(**info)


async def innovate_recipe(spooncular_recipe: SpooncularRecipe) -> Recipe:
    """Innovate a new recipe by LLM using the recipe created from Spooncular API"""

    # handle sending recipe to LLM when recipe-generation fails using Spooncular API
    if not spooncular_recipe.title:
        logger.error("Recipe Innovation failed before sending to the LLM!!!")

        ingredients_list = [Ingredient(ingredient="Null")]
        steps_list = [Step(step_number=0, instruction="Null", explanation="Null")] 

        return Recipe(
            recipe_title="Error Innovating A Recipe, Try Again Later!!!",
            ingredients=ingredients_list,
            steps=steps_list,
            tips=[]
        ) 
    
    # call the LLM for recipe innovation
    resp = await innovate_new_recipe_using_gemini("draft_recipe", spooncular_recipe.model_dump())

    if resp:
        # convert ingredients list of strings to list of Ingredient objects
        ingredients_list = [Ingredient(ingredient=ing) for ing in resp['ingredients']]
        # convert steps list of dicts to list of Step objects
        steps_list = [Step(**step) for step in resp['steps']]
    else:
        ingredients_list = [Ingredient(ingredient="Null")]
        steps_list = [Step(step_number=0, instruction="Null", explanation="Null")] 
        logger.error("Recipe Innovation failed using the LLM!!!")


    # create the Recipe object
    return Recipe(
        recipe_title=resp.get('recipe_title', "Error Innovating A Recipe, Try Again Later!!!"),
        ingredients=ingredients_list if ingredients_list else [],
        cooking_time=resp.get('cooking_time', ''),
        cooking_temperature=resp.get('cooking_temperature', ''),
        steps=steps_list if steps_list else [],
        tips=resp.get('tips', [])
    )

    #! Validation calls
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
