import os
import json

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GoogleLLM:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv(
                "GOOGLE_API_KEY",
            ),
        )

        self.model = "models/gemini-3.5-flash-lite"

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text

    def generate_json(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        try:
            return json.loads(
                response.text,
            )

        except json.JSONDecodeError:

            print(response.text)

            raise