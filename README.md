# Building and Experimenting Production Grade AI Applications

<!-- ## RAGs

Production grade RAG for business-usecases: [check-this](/ai_workflows/Document_analysis_RAG/README.md) -->

<div align="center">
    <picture>
        <img alt="Building AI Applications" height="200px" src="https://github.com/VimukthiRandika1997/AI-development/blob/main/assets/building_production_grade.png?raw=true">
    </picture> 
    
Formulate → Build → Iterate
</div>

## AI Agents

- ### Basic Concepts

    - Concepts for Building and Deploying AI Agents: [more details](/ai_agents/basics/README.md) 

- ### Building AI Agents with Google ADK (Agent Development Kit)

    - RAG Agent with Google ADK: [more details](/ai_agents/Google_ADK/adk_rag_agent/README.md)
    - Deploying Agents to GCP: [more details](/ai_agents/Google_ADK/deploying_agents_to_GCP/README.md)


## AI Workflows

- ### Chatbots

    - End-to-End Chatbot for generating Recipes: [more details](/ai_workflows/RecipeMate_chatbot/README.md)

## Finetuning Foundational Models

- ### LLMs
    - Text classification with LLMs: [more details](/finetuning_foundational_models/llms/text_classification/README.md)

- ### Computer Vision
    - AI Background Generation For Ecommerce Products: [more details](/finetuning_foundational_models/computer_vision/ai_background_generator/README.md)
    - AI Background Remover: [more details](/finetuning_foundational_models/computer_vision/ai_background_remover/README.md)


## Classical ML

- Hyper-parameter Tuning with XGBoost 3.0 and Optuna: CPU based vs GPU: [more details](/classical_ml/gpu_accelerated_pipeline/README.md)

## API Design

Architecting the FastAPI for different use-cases. 

- ### Design Patterns

    - Common design patterns: [more details](/api_design/design_patterns/1-Intro.md)

- ### FastAPI

    - #### Clean Architecture for FastAPI

        - Introduction to Clean Architecture - Level-1: [more details](/api_design/FastAPI/clean_architecture/README.md)
        - Introduction to Clean Architecture - Level-2: [more details](/api_design/FastAPI/clean_architecture/level-2/README.md)

    - #### Handling Long Running Jobs with FastAPI

        - A non-blocking, async-safe job-system to handle long-running background tasks: [more details](/api_design/FastAPI/long_running_jobs_with_fastapi/README.md)

        ![system-architecture](/api_design/FastAPI/long_running_jobs_with_fastapi/assets/long_running_task_overview.png)

    - #### Event Driven Notification System with Webhooks

        - A FastAPI-based webhook dispatcher with worker support. Here we are designing a complete system for learning purpose: [more details](/api_design/FastAPI/event_driven_notification_system/README.md)

    - #### API Design For AI-Background Generation

        - A production grade FastAPI service for AI Background Generation using fine-tuned diffusion models:

        - [api-design](/ai-background-generation/README.md)
        - [product-development](https://github.com/VimukthiRandika1997/AI-background-generation)

        ![Sample generated product-shots](/ai-background-generation/assets/sample_image.png)

    - #### Handling Memory Leaks With Data Ingestion Workloads

        - Python tends to exihibit memory leaks during data ingestion workloads ( like upoloading files, processing files)
        - This needs to be addressed in an efficient and safe way: [more details](/api_design/FastAPI/handling_memory_leaks/README.md)
