# Python Foundations

Hands-on Python exercises covering file handling, object-oriented programming, error handling, REST API integration and LLM applications, built while preparing for AI engineering work.

## What's inside
| File | What it does | Concepts |
|---|---|---|
| `top_players.py` | Reads players from a JSON file, ranks them by score, prints the top 3 and saves them to a new JSON file | File I/O, JSON, sorting with key functions, lambda, enumerate |
| `bank_account.py` | `BankAccount` class with deposits, withdrawals and input validation | Classes, custom exceptions, exception handling, guard clauses |
| `github_profile.py` | Fetches a GitHub user's profile via the GitHub REST API and shows their top 3 repos by stars | REST APIs, `requests`, HTTP status codes, timeouts, network error handling |
| `ask_ai.py` | Terminal AI chat app (Gemini API) with conversation memory, switchable personas, and saved chat sessions | LLM APIs, conversation history, system prompts, retries with exponential backoff, environment variables, input validation, path traversal protection, custom exception handling |

## Setup
```
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

## Run
```
python top_players.py
python bank_account.py
python github_profile.py
python ask_ai.py
```

## `ask_ai.py` commands
| Command | What it does |
|---|---|
| `/persona <name>` | Switch to a persona from `prompts/` (clears the current conversation) |
| `/personas` | List available personas |
| `/save <name>` | Save the current conversation to `chats/<name>.json` (letters and numbers only) |
| `/load <name>` | Restore a saved conversation and its persona |
| `/reset` | Clear the conversation history |
| `quit` | Auto-save to `chats/autosave.json` and exit (restored on next start) |

Add your own personas by dropping a `.txt` file with a system prompt into `prompts/`. `default.txt` is loaded at startup and must always exist.