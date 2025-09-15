import os
from fastapi import FastAPI
from api.orchestrator import handle_turn, dynamic_question_handle, generate_recipe, innovate_recipe, validate_recipe
from api.schemas import Recipe

app = FastAPI()
API_VERSION = os.getenv("API_VERSION", "dev")


@app.post(f"/{API_VERSION}/chat/turn")
async def chat_turn(session_id: str, user_utterance: str):
    return await handle_turn(session_id, user_utterance)


@app.post(f"/{API_VERSION}/chat/dynamic_question")
async def dynamic_question_generation(session_id: str):
    return await dynamic_question_handle(session_id)


@app.post(f"/{API_VERSION}/recipe/generate", response_model=Recipe)
async def recipe_generate(session_id: str):
    return await generate_recipe(session_id)


@app.post(f"/{API_VERSION}/recipe/generate", response_model=Recipe)
async def recipe_innovate(recipe: Recipe):
    return await innovate_recipe(recipe)


@app.post(f"/{API_VERSION}/validate")
async def recipe_validate(recipe: Recipe):
    return await validate_recipe(recipe)
