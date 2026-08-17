import os

from google import genai


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