from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    _SYSTEM_PROMPT = """
        You are a technical assistant. 
        Answer in a concise way, and relying ONLY on the provided extracts. 
        If the information is not present in those, TELL 'I did not find anything in my database to answer that'.
    """

    @abstractmethod
    def ask(self: BaseGenerator, question: str, context: list[str]) -> str:
        pass