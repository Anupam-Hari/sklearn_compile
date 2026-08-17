from dotenv import load_dotenv

from transpiler.llm.google import (
    GoogleLLM,
)


load_dotenv()

llm = GoogleLLM()

response = llm.generate(
    "Say hello.",
)

print(response)