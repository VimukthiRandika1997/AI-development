# High Level Components of The Conversational Chatbot

```bash
                  [ User (Web) ]
                        ║
                        ║
                        ▼
                    [ UI Layer ]
                        ║
                        ║
                        ▼
        [ NLP Layer: NLU + Dialogue Manager + NLG ]
                        ║
            ╔════════════════════════════════════╗
            ║                ║                   ║
            ▼                ▼                   ▼
        [ KB / FAQ ]   [ Vector DB ]   [ Business Logic / APIs(Spooncular) ]
                            ║
                            ║
                            ▼
                [ Response Generation ]
                            ║
                            ║
                            ▼
                [ User Interface (Response back to user) ]
```

1. **User Interface**

    - **Text Interface** - Chat widget (Streamlit)

2. **Conversation Management Layer**

    - **NLU**
        - Intent recognition (what the user wants)
        - Entity extraction  (identifying useful keywords)
        - This is done by using an LLM  (Gemini Model)

    - **Dialogue Management**
        - Keeps track of context (past history of conversations: using Redis database)
        - Decides next action (ask for clarification, fetch data, respond)

    - **NLG**
        - Generates human-like responses (LLM-based: Gemini Model)

3. **Business Logic Layer**

    - Orchestrates workflows 
    - Connects with APIs (Spooncular API)
    - Applies rules (for decision-making)

4. **Knowledge & Data Layer**

    - **Static knowledge base** (FAQs, Reciepies)
    - **Dynamic knowledge base** (vector stores for semantic search, databases, currently using only Redis database)


5. **Integration Layer**

    - Backend systems (databases, analytics)
    - This is for handling user data and analytical services

6. **Monitoring**

    - Logs of conversations
    - User satisfaction metrics
    - This is not implemented yet


# Tech Stack

1. Front-end: Streamlit

2. Backend:
    - Custom orchestrator: built with python for running the application including busiiness logic and handling operations
    - Session Handling and memory: Redis Database
    - API: FastAPI
    - LLM: Gemini Model ( gemini-2.0-flash)


# How to run 

1. Set the API keys:

```bash
cp .env.sample .env
# within .env file, set the required keys:
GEMINI_API_KEY=<your_gemini_api_key>
SPOONACULAR_API_KEY=<your_spooncular_api_key>
```

2. Locally:

```bash
# Run the application
make run-all

# Reset session-data
make run-reset
```

3. Docker based approach:

```bash
# for building docker containers and running containers
make run-build
# for removing containers
make run-down
# for running containers
make run-up
```

After that visit: `http://0.0.0.0:8501`

# Notes:

- Currently entire chat-history for the user-session is sent to the LLM for coherent user-intent parsing.
    - This can be further optimized with different techniqeus:
        1. Summarizing the chat-history and attach it to the LLM call
        2. Sending only the most recent chat through a sliding window technique, etc

- If certain attributes are filled by the user, the recipe-generation is triggered:
    - Attributes to be considered: `ingredients_on_hand`, `dietary_rules`, `equipment`, `time_budget_minutes`
    - If these attributes are semantically given by the user (semantic mapping through LLM), then only the recipe is generated

- A Custom messaging window (no.of messages the bot waits before generating a recipe) is implemented to  

- Spooncular API may result empty results when searching with some attributes:
    - Attributes:
        - `maxReadyTime`, `servings`, `diet`
    - Hence those attributes were omitted during the developement

- Currently validation step is not implemented due to the time-contraints

- Possible upgrades:
    1. Provide the recipe in streaming fashion
    2. Generate an image for each of the steps given by the LLM