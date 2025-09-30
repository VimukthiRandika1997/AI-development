# Knowledge Graph Creation For Ecommerce Product Shots

This application extracts information in a graph format (nodes and relationships) from the text input:

- Identifies the environmental settings of the product packshot:
    - Person who're interacting
    - Environment settings: Light, Location, Surface

![product packshot](/ai_workflows/knowledge_graphs/assets/product_description.png)

Here is the corresponding Closed-domain Knowledge Graph:

![knowledge graph](/ai_workflows/knowledge_graphs/assets/knowledge_graph_closed_domain.png)

## Current Workflow

1. Given an image containing the product packshot, text prompt is generated throught an LLM
2. This generated text prompt is given to the pipeline (contains an LLM) to create the knowledge graph

## How To Run

1. Install the dependencies usinig `uv` package manager:

    ```bash
    uv sync
    ```

2. Set the API Keys:

    ```bash
    cp .env.sample .env
    # add `GOOGLE_API_KEY=`
    ```

3. Run the script

    ```bash
    streamlit app.y
    ```