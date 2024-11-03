import os
import json
import requests
import openai # Version: 1.53.0

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

DEFAULT_MODEL = "text-davinci-003"

class OpenAIService:
    def __init__(self):
        pass 

    async def execute_request(self, request_text: str, model: str = DEFAULT_MODEL) -> str:
        """
        Processes a user request, generates an OpenAI API call, executes it, and returns the formatted response.

        Args:
            request_text: The user's natural language request.
            model: The OpenAI model to use (default: text-davinci-003).

        Returns:
            The formatted response from OpenAI.

        Raises:
            openai.error.APIError: If there is an error communicating with OpenAI.
            ValueError: If the request text is invalid or the model is not supported.
        """
        if not request_text or len(request_text) < 5:
            raise ValueError("Invalid request text: Must be at least 5 characters long")

        try:
            response = openai.Completion.create(
                model=model,
                prompt=request_text,
                temperature=0.7,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            return response.choices[0].text.strip()
        except openai.error.APIError as e:
            raise openai.error.APIError(f"Error communicating with OpenAI API: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid request text or model: {e}")