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


def ask(history, system_prompt):
    counter = 0
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=history,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt
                ),
            )
            return response.text
        except genai.errors.APIError as e:
            if counter != 3 and e.code in (429, 500, 503):
                print(f"Server busy, retrying in {2**counter}s")
                time.sleep(2**counter)
                counter += 1
            else:
                raise


def load_prompt(name):
    if name + ".txt" not in os.listdir("./prompts"):
        raise FileNotFoundError
    with open(f"./prompts/{name}.txt") as f:
        return f.read()


if __name__ == "__main__":
    system_prompt = load_prompt("default")
    while True:
        user_input = input("Enter a question... ").strip()
        if not user_input:
            print("Please enter a question.")
        else:
            parts = user_input.split()
            if user_input.lower() == "quit":
                break
            elif user_input.lower() == "/reset":
                history.clear()
                print("History has been reset.")
            elif parts[0] == "/persona":
                if len(parts) != 2:
                    print("Need one type of persona (/persona <name>)")
                else:
                    persona = parts[1].lower()
                    try:
                        system_prompt = load_prompt(persona)
                        history.clear()
                        print("Persona loaded successfully.")
                    except FileNotFoundError:
                        print(
                            "Entered persona is not available.\nTo check available personas, use '/personas'"
                        )
            elif parts[0] == "/personas":
                for persona in os.listdir("./prompts"):
                    print(persona.split(".")[0])
            else:
                history.append(make_message("user", user_input))
                try:
                    response = ask(history, system_prompt)
                    print(response)
                    history.append(make_message("model", response))
                    print(f"Number of messages in history: {len(history)}")
                except genai.errors.APIError as e:
                    print(e.message)
                    history.pop()
