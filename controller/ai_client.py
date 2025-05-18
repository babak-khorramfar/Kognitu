# controller/ai_client.py

from transformers import pipeline
from utils.config import MODEL_NAME


class AIClient:
    """
    A simple client to interact with a language model
    for generating board layouts.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        # Initialize the text generation pipeline
        self.generator = pipeline("text-generation", model=model_name)

    def generate(self, prompt: str, max_length: int = 100) -> str:
        """
        Generate text based on the given prompt.
        Returns the generated text string.
        """
        result = self.generator(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]["generated_text"]
