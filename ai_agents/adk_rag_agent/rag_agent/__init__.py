"""
Vertex AI RAG Agent

A package for interacting with GCP Vertex AI RAG capabilities
"""

import os
import vertexai
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Get Vertex AI configuration from environment
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")

# Initialize the Vertex AI at package load time
try:
    if PROJECT_ID and LOCATION:
        logger.info(f"Initializing Vertex AI with project={PROJECT_ID} and location={LOCATION}")
        vertexai.init(project=PROJECT_ID, location=LOCATION)
    else:
        logger.error(f"Missing Vertex AI configuration, Project{PROJECT_ID}, LOCATION={LOCATION}",
                     "Tools require Vertex AI to proceed")

except Exception as e:
    logger.error(f"Failed to initialize Vertex AI: {str(e)}")
    logger.debug("Please check your GCP credentials and project settings")

# Import agent after initialization is complete
from . import agent