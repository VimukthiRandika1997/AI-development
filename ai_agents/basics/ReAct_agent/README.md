# ReAct Agent

A simple agent that runs in a loop.

```psql
    [User]
      |
      |   (System Prompt)
      |
    [LLM] (Thought -> Pause -> Action -> Observation)<---------
      |                                                       |
      |                                                       |
      |                                                       |
    /   \                                                     |
   /     \                                                    |
 return  action (tool) ---------------------------------------|

```