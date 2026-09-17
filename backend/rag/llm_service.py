from langchain_ollama import ChatOllama


class LLMService:
    """
    Handles communication with the local Ollama LLM.
    """

    MODEL_NAME = "llama3"

    def __init__(self):
        self.llm = ChatOllama(
            model=self.MODEL_NAME,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and return its response.
        """

        response = self.llm.invoke(prompt)

        return response.content