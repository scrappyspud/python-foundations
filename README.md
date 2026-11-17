# Python Foundations

Hands-on Python exercises covering file handling, object-oriented programming, error handling and REST API integration, built while preparing for AI engineering work.

## What's inside
| File | What it does | Concepts |
|---|---|---|
| `top_players.py` | Reads players from a JSON file, ranks them by score, prints the top 3 and saves them to a new JSON file | File I/O, JSON, sorting with key functions, lambda, enumerate |
| `bank_account.py` | `BankAccount` class with deposits, withdrawals and input validation | Classes, custom exceptions, exception handling, guard clauses |
| `github_profile.py` | Fetches a GitHub user's profile via the GitHub REST API and shows their top 3 repos by stars | REST APIs, `requests`, HTTP status codes, timeouts, network error handling |

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
```