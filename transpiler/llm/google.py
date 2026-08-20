import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class GoogleLLM:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY"),
        )

        self.model = "gemini-3.7-flash"

    def generate(self, prompt, tools=None):

        config = types.GenerateContentConfig(
            tools=tools or [],
        )

        return self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )