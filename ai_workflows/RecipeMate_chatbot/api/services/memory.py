"""Handls the memory layer through Redis:

- Currently this acts has a short-term memory
"""

import os
from redis import Redis
from api.schemas import SessionState


import os
from redis import Redis
from api.schemas import SessionState, Turn
from loguru import logger


# Connection
redis = Redis.from_url(os.getenv("REDIS_URL"))


async def get_state(session_id: str) -> SessionState:
    """Get the session data given session id"""

    session = redis.get(session_id)
    if session:
        return SessionState.parse_raw(session)
    return SessionState(session_id=session_id)


async def set_state(session_id: str, state: SessionState):
    """Persist session state to Redis"""

    redis.set(session_id, state.model_dump_json(), ex=3600)


async def add_user_utterance(session_id: str, utterance: str) -> SessionState:
    """Add a user utterance as a new turn"""

    state = await get_state(session_id)
    turn_id = len(state.chat) + 1

    state.chat.append(Turn(
        turn_id=turn_id,
        user=utterance
    ))

    await set_state(session_id, state)
    return state


async def add_bot_response(session_id: str, response: str) -> None:
    """Attach bot response to the latest turn"""

    state = await get_state(session_id)

    if not state.chat:
        # Defensive: if bot speaks first (rare case), create a turn
        turn_id = 1
        state.chat.append(Turn(turn_id=int(turn_id), bot=response))
    else:
        # Update the last turn with bot response
        state.chat[-1].bot = response

    await set_state(session_id, state)


async def update_session_state(session_id: str, response: dict) -> None:
    """Update the session state (metadata) based on the bot's response"""

    state = await get_state(session_id)

    for key, value in response.items():
        if not hasattr(state, key):
            # Ignore unknown keys
            continue

        current_value = getattr(state, key)

        if isinstance(current_value, list) and isinstance(value, list):
            # Merge lists without duplicates
            updated_list = list(dict.fromkeys(current_value + value))
            setattr(state, key, updated_list)
        elif value is not None:
            # Only update scalars if not None
            setattr(state, key, value)

    await set_state(session_id, state)


async def update_delay_count(session_id: str) -> None:
    """Update the session's delay count by 1"""

    state = await get_state(session_id)
    state.delay_count += 1
    logger.info("Delay-count: ", state.delay_count)
    await set_state(session_id, state)
    

async def reset_delay_count(session_id: str) -> None:
    """Reset the session's delay count to zero"""

    state = await get_state(session_id)
    state.delay_count = 0
    await set_state(session_id, state)
