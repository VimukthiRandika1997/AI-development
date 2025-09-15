import streamlit as st
from pydantic import BaseModel
import requests
import os
import uuid


# Helper functions
def display_recipe(recipe):
    print(recipe)
    st.title(recipe["recipe_title"])

    with st.expander("Ingredients"):
        for ing in recipe["ingredients"]:
            line = ing["ingredient"]
            if ing["amount"]:
                amount = ing["amount"]
                unit = ing["unit"]
                line = f"{amount} {unit or ''} {line}"
            if ing["notes"]:
                note = ing["notes"]
                line += f" ({note})"
            st.write(f"• {line.strip()}")

    # Display cooking info side by side
    col1, col2 = st.columns(2)
    with col1:
        if recipe["cooking_time"]:
            st.subheader("Cooking Time")
            st.write(recipe["cooking_time"])
    with col2:
        if recipe["cooking_temperature"]:
            st.subheader("Cooking Temperature")
            st.write(recipe["cooking_temperature"])

    st.subheader("Steps")
    for step in recipe["steps"]:
        _step = step["step_number"]
        _instruction = step["instruction"] 
        st.markdown(f"**Step {_step}:** {_instruction}")
        if step["explanation"]:
            with st.expander("Explanation"):
                st.write(step["explanation"])

    if recipe["tips"]:
        st.subheader("Tips")
        for tip in recipe["tips"]:
            st.write(f"• {tip}")


### - Settings - ###
API = os.getenv("API_URL", "http://localhost:8080")
API_VERSION = os.getenv("API_VERSION", "dev")


### - UI - ###
st.title("🍳 RecipeMate")

# Initialize sessions dictionary
if "sessions" not in st.session_state:
    st.session_state.sessions = {}  # {session_id: {"name": str, "messages": []}}
if "active_session" not in st.session_state:
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"name": f"Session {len(st.session_state.sessions)+1}", "messages": []}
    st.session_state.active_session = sid

# Sidebar: Session manager
st.sidebar.header("💬 Sessions")

# Button to create new session
if st.sidebar.button("✨ New Session"):
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"name": f"Session {len(st.session_state.sessions)+1}", "messages": []}
    st.session_state.active_session = sid
    st.rerun()

# Session selector with friendly names
session_options = [f"{data['name']} ({sid[:8]})" for sid, data in st.session_state.sessions.items()]
session_ids = list(st.session_state.sessions.keys())

selected_idx = st.sidebar.selectbox(
    "Select a session",
    range(len(session_ids)),
    format_func=lambda i: session_options[i],
    index=session_ids.index(st.session_state.active_session),
)
st.session_state.active_session = session_ids[selected_idx]

# Rename active session
active_session_data = st.session_state.sessions[st.session_state.active_session]
new_name = st.sidebar.text_input("Rename session", value=active_session_data["name"])
if new_name.strip() and new_name != active_session_data["name"]:
    active_session_data["name"] = new_name

st.sidebar.markdown(f"**Active Session ID:** `{st.session_state.active_session}`")

# Get active session messages
messages = active_session_data["messages"]

# Render chat history
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("What would you like to cook?"):
    # Add user message
    messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call API
    resp = requests.post(
        f"{API}/{API_VERSION}/chat/turn",
        params={
            "session_id": st.session_state.active_session,
            "user_utterance": user_input,
        },
    ).json()

    bot_reply = resp.get("bot_message", "⚠️ No reply from bot")
    recipe = resp.get("recipe", None)

    # Add bot reply
    messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
        if recipe:
            display_recipe(recipe=recipe)

    

# Generate Recipe button
# if st.button("Generate Recipe"):
#     recipe_resp = requests.post(
#         f"{API}/{API_VERSION}/recipe/generate",
#         params={"session_id": st.session_state.active_session},
#     ).json()

#     recipe_title = recipe_resp.get("recipe_title", "Generated Recipe")
#     recipe_content = f"### {recipe_title}\n\n```json\n{recipe_resp}\n```"

#     # Add recipe as assistant message
#     messages.append({"role": "assistant", "content": recipe_content})
#     with st.chat_message("assistant"):
#         st.markdown(recipe_content)
