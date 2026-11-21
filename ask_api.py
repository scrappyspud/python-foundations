from google import genai
from dotenv import load_dotenv
import os
import time
import json


class KeyNotFoundError(Exception):
    pass


class SaveError(Exception):
    pass


class PersonaNotFoundError(Exception):
    pass


class ChatNotFoundError(Exception):
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
        raise PersonaNotFoundError("Persona is not available.")
    with open(f"./prompts/{name}.txt") as f:
        return f.read()


def save_chat(name, persona, history):
    if not name.isalnum():
        raise SaveError(
            "Invalid name format for chat. Only use alphanumeric characters."
        )
    os.makedirs("chats", exist_ok=True)
    chat = {"persona": persona, "history": history}
    with open(f"./chats/{name}.json", mode="w") as f:
        json.dump(chat, f)


def load_chat(name):
    if not os.path.isdir("./chats"):
        raise ChatNotFoundError("No chats have been saved yet.")
    if name + ".json" not in os.listdir("./chats"):
        raise ChatNotFoundError("No chat is saved with the entered name.")
    with open(f"./chats/{name}.json") as f:
        return json.load(f)


def restore_chat(name):
    loaded_chat = load_chat(name)
    return (
        load_prompt(loaded_chat["persona"]),
        loaded_chat["persona"],
        loaded_chat["history"],
    )


if __name__ == "__main__":
    system_prompt = load_prompt("default")
    current_persona = "default"
    try:
        system_prompt, current_persona, history = restore_chat("autosave")
        print("Last chat loaded successfully")
    except (json.JSONDecodeError, KeyError):
        print("Corrupted autosaved chat. Starting a fresh conversation.")
    except ChatNotFoundError:
        print("No autosaved chat found. Starting a fresh conversation.")
    except PersonaNotFoundError:
        print(
            "Persona not available from the autosaved chat. Starting a fresh conversation."
        )

    while True:
        user_input = input("Enter a question... ").strip()
        if not user_input:
            print("Please enter a question.")
        else:
            parts = user_input.split()
            if user_input.lower() == "quit":
                try:
                    save_chat("autosave", current_persona, history)
                    print("Chat saved successfully.")
                except SaveError as e:
                    print(e)
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
                        current_persona = persona
                        print("Persona loaded successfully.")
                    except PersonaNotFoundError:
                        print(
                            "Entered persona is not available.\nTo check available personas, use '/personas'"
                        )
            elif parts[0] == "/personas":
                for persona in os.listdir("./prompts"):
                    print(persona.split(".")[0])
            elif parts[0] == "/save":
                if len(parts) != 2:
                    print("Enter name for the saved chat (/save <name>)")
                else:
                    save_name = parts[1].lower()
                    try:
                        save_chat(save_name, current_persona, history)
                        print("Chat saved successfully.")
                    except SaveError as e:
                        print(e)
            elif parts[0] == "/load":
                if len(parts) != 2:
                    print("Enter name for the chat to be loaded (/load <name>)")
                else:
                    load_name = parts[1].lower()
                    try:
                        system_prompt, current_persona, history = restore_chat(
                            load_name
                        )
                        print("Chat loaded successfully")
                    except (json.JSONDecodeError, KeyError):
                        print("Invalid JSON format. Could not load the chat.")
                    except (
                        ChatNotFoundError,
                        PersonaNotFoundError,
                    ) as e:
                        print(e)

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
