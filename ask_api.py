from google import genai
from dotenv import load_dotenv
import os
import time


class KeyNotFoundError(Exception):
    pass


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise KeyNotFoundError("No API key is found.")

client = genai.Client(api_key=api_key)
history = []


def make_message(role, message):
    return {"role": role, "parts": [{"text": message}]}


def ask(history):
    counter = 0
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite", contents=history
            )
            return response.text
        except genai.errors.APIError as e:
            if counter != 3 and e.code in (429, 500, 503):
                print(f"Server busy, retrying in {2**counter}s")
                time.sleep(2**counter)
                counter += 1
            else:
                raise


if __name__ == "__main__":
    while True:
        user_input = input("Enter a question... ").strip()
        if user_input.lower() == "quit":
            break
        elif user_input.lower() == "/reset":
            history.clear()
            print("History has been reset.")
        elif user_input:
            history.append(make_message("user", user_input))
            try:
                response = ask(history)
                print(response)
                history.append(make_message("model", response))
                print(f"Number of messages in history: {len(history)}")
            except genai.errors.APIError as e:
                print(e.message)
                history.pop()
