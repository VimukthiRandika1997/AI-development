from abc import ABC, abstractmethod


class LLM(ABC):
    """Abstract class for handling LLM based operations"""
    @abstractmethod
    async def ask_llm(self, mode: str, payload: dict):
        pass