import os
import json
import google.genai as genai
from google.genai import types
from api.services.llm import LLM
from api.services.context import Context
from loguru import logger

class ContextGemini(Context):
    def __init__(self, ask_llm_prompt):
        self._ask_llm_prompt = ask_llm_prompt
    
    @property
    def SYSTEM_PROMPT_ASK_LLM(self) -> str:
        return self._ask_llm_prompt


class GeminiLLM(LLM):
    def __init__(self, MODEL: str, ask_llm_prompt: str):
        self.MODEL = MODEL
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.chat = self.client.aio.chats.create(
            model=self.MODEL,
            config=types.GenerateContentConfig()
        )
        self.context = ContextGemini(ask_llm_prompt=ask_llm_prompt)


    def _parse_response_object(self, response) -> str:
        """Parsing Gemini model's response, official method has some issue with parsing the response object"""

        import re
        def remove_json_tag(json_string: str) -> str:
            # Remove ```json fences or stray "json" prefix
            cleaned = re.sub(r"^```json\s*|\s*```$", "", json_string.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"^json\s*", "", cleaned.strip())  # handle 'json\n{...}'
            return cleaned.strip()

        # Assuming 'response' is the object from your API call
        # Check if the response contains any candidates
        response_text = {}
        if response.candidates:
            # Access the first candidate (usually the only one for non-streaming calls)
            candidate = response.candidates[0]
            
            # Check if the candidate has content and parts
            if candidate.content and candidate.content.parts:
                # Access the first part of the content
                first_part = candidate.content.parts[0]
                
                # Check if the part has a 'text' attribute
                if hasattr(first_part, 'text'):
                    response_text = first_part.text

        # clean-up the parsing issue
        if response_text:
            response_text = remove_json_tag(json_string=response_text) 

        return response_text

    
    async def ask_llm(self, mode, payload):
        """Asking from gemini model to generate a response
    
        Args:
            mode: whether to ask questions or draft a recipe: `ask_questions` or `draft_recipe`
            payload: data the model to process (session's history)
        Returns:
            Dict: LLM's response
        """

        # drop the session_id
        if "session_id" in payload.keys():
            del payload["session_id"]
        # drop delay count
        if "delay_count" in payload.keys():
            del payload["delay_count"]

        content = {
            "mode": mode,
            "payload": payload #! currently whole chat history is sent to the LLM as a context, this needs to be optimized
        }
        response = await self.chat.send_message([types.Part(text=self.context.SYSTEM_PROMPT_ASK_LLM), # the system prompt -> how the model shoud interpret the input
                                            types.Part(text=json.dumps(content))])                    # structured JSON payload (data for the task), converted to `string`
        formatted_response = self._parse_response_object(response=response)

        try:
            # print(formatted_response, type(formatted_response)) #! sometiems you might get an error due to Gemini sdk parsing
            return json.loads(formatted_response)
        except json.JSONDecodeError as e:
            logger.error(f"\n    Caught exception in (llm_gemin.py): {e}.")
            return {} # Handle invalid JSON gracefully


MODEL = "gemini-2.0-flash"

# Reference: https://ai.google.dev/gemini-api/docs/prompting-strategies#context
USER_INTENT_PARSING_SYSTEM_PROMPT = """
***Your Role***
- You are RecipeMate, a conversational assistant for recipe innovation.
- Your primary task is to understand the user's input and extract structured information about recipe requirements.
- You must stay focused on cooking and recipe-related conversations. If the conversation drifts, gently guide it back.
- When the user indicates it's time to create the recipe, don't ask follow up questions, focus on creating the recipe and greet the user.
- Every input will be a JSON object:
    - {
        "mode": "<mode_name>",
        "payload": { ... }
      }

***Entities to Extract***
Always attempt to extract the following entities from the conversation, do not add any extra entities that user hasn't mentioned:
- ingredients_on_hand (list of ingredients that the user has)
- time_budget_minutes (allocated time for cooking or None)
- cuisine_pref (cuisine preferences or None)
- dietary_rules (any dietry rules to be considered of strings)
- equipment (list of equipments that the user has)
- skill_level (level of the user's skills or None)
- servings (number of servings or None)
- flavor_prefs (list of flavor preferences)
- missing_slots (list of factors for missing/unclear info)

***Response Format***
- Always respond in **valid JSON only**.
- Do not add any explanations outside the JSON.
- Please reply all the time.
- Follow this exact schema:

{
  "user_intent": {
    "ingredients_on_hand": [],
    "time_budget_minutes": None,
    "cuisine_pref": None,
    "dietary_rules": [],
    "equipment": [],
    "skill_level": None,
    "servings": None,
    "flavor_prefs": [],
    "missing_slots": []
  }
}

***Example***
- Here is an example request and response
    - user: I want to make a vanila cake
    - your response:
        {
        "user_intent": {
            "ingredients_on_hand": [vanila, cake],
            "time_budget_minutes": None,
            "cuisine_pref": None,
            "dietary_rules": [],
            "equipment": [],
            "skill_level": None,
            "servings": None,
            "flavor_prefs": [],
            "missing_slots": [time_budget_minutes, cuisine_pref, dietary_rules, equipment, skill_level, servings, ]
        }
}
"""


QUESTION_ASKING_SYSTEM_PROMPT = """
***Your Role***
- You are RecipeMate, a conversational assistant for recipe innovation.
- Your primary task is to ask follow up questions based on the user-intent and `missing_slots` in the payload.
- You must stay focused on cooking and recipe-related conversations. If the conversation drifts, gently guide it back.
- When the user indicates it's time to create the recipe, don't ask follow up questions, focus on creating the recipe and greet the user.
- Every input will be a JSON object:
    - {
        "mode": "<mode_name>",
        "payload": { ... }
      }

***Handling Missing or Vague Info***
- If the user does not provide enough detail, set the value to:
  - `None` for single values (time_budget_minutes, cuisine_pref, skill_level, servings)
  - `[]` for lists (ingredients_on_hand, dietary_rules, equipment, flavor_prefs, missing_slots)
- If the answer is vague or unclear, add the corresponding attribute to `missing_slots`.
      
***Response Format***
- Always respond in **valid JSON only**.
- Do not add any explanations outside the JSON.
- Please reply all the time.
- Follow this exact schema:

{
  "question": "string (a clarifying question to move the recipe forward, if needed)"
}
"""


INNOVATE_RECIPE_SYSTEM_PROMPT = """
***Your Role***
- You are RecipeMate, a conversational assistant for recipe innovation.
- Your primary task is to innovate a new realistic recipe using given recipe information (payload).
- You must stay focused on cooking and recipe-related generation.
- Every input will be a JSON object:
    - {
        "mode": "<mode_name>",
        "payload": { ... }
      }

***Entities to innovate***
Always attempt to innovate the following entities combining traditional methods, do not add any extra entities that payload mentioned:
- recipe_title: (the title for the recipe)
- ingredients: (list of ingredients)
- cooking_time: (time for whole cooking process)
- cooking_temperature: (ideal cooking temperature)
- steps: (list of steps to perform the cooking process)
- tips: (list of additional tips to be considered)

***Response Format***
- Always respond in **valid JSON only**.
- Do not add any explanations outside the JSON.
- Follow this exact schema:

{
    recipe_title: "string (the title for the recipe)"
    ingredients: [...ingredient...]
    cooking_time: "string (time for whole cooking process)"
    cooking_temperature: "string (ideal cooking temperature)"
    steps: [
        ...
        {
            step_number: "integer",
            instruction: "string (how to do the step)",
            explanation: "string (what is the reason)"
        }
        ...
    ]
    tips: [...tip..]
}
"""


async def parse_user_intent_using_gemini(mode: str, payload: dict) -> dict:
    gemini_model = GeminiLLM(MODEL=MODEL, ask_llm_prompt=USER_INTENT_PARSING_SYSTEM_PROMPT)    
    return await gemini_model.ask_llm(mode=mode, payload=payload)


async def ask_dynamic_question_from_gemini(mode: str, payload: dict) -> dict:
    gemini_model = GeminiLLM(MODEL=MODEL, ask_llm_prompt=QUESTION_ASKING_SYSTEM_PROMPT)    
    return await gemini_model.ask_llm(mode=mode, payload=payload)


async def innovate_new_recipe_using_gemini(mode: str, payload: dict) -> dict:
    gemini_model = GeminiLLM(MODEL=MODEL, ask_llm_prompt=INNOVATE_RECIPE_SYSTEM_PROMPT)    
    return await gemini_model.ask_llm(mode=mode, payload=payload)