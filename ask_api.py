from google import genai
from dotenv import load_dotenv
import os


class KeyNotFoundError(Exception):
    pass


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise KeyNotFoundError("No API key is found.")

client = genai.Client(api_key=api_key)


def ask(question):

    response = client.models.generate_content(
        model="gemini-3.6-flash", contents=question
    )
    return response.text


if __name__ == "__main__":
    while True:
        user_input = input("Enter a question... ").strip()
        if user_input.lower() == "quit":
            break
        if not user_input:
            continue
        try:
            print(ask(user_input))
        except genai.errors.APIError as e:
            print(e.message)
