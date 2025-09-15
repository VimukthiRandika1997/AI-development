
from abc import ABC, abstractmethod

class Context(ABC):
    """Context Engineering for the LLM"""
    
    @property
    @abstractmethod
    def SYSTEM_PROMPT_ASK_LLM(self) -> str:
        pass