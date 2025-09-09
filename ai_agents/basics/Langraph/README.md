# LangGraph

- LangGraph is an extension of LangChain that support graphs.
- Single and Multi-agent flows are described and represented as graphs.
- Allows for extremely controlled "flows".
- Built-in persistence allows for human-in-the-loop workflows.

# LangGraph Components

- **Nodes**: Agent or functions
- **Edges**: connect nodes
- **Conditional edges**: decisions

- **Agent State**:
    - Agent state is accessible to all parts of the graph
    - It is local to the graph
    - Can be stored in a persistence layer
