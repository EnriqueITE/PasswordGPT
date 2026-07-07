import argparse
import os
import sys
from typing import Any

import requests


BANNER = r"""
    ____                                          ____________  ______
   / __ \____ ____________      ______  _________/ / ____/ __ \/_  __/
  / /_/ / __ `/ ___/ ___/ | /| / / __ \/ ___/ __  / / __/ /_/ / / /
 / ____/ /_/ (__  |__  )| |/ |/ / /_/ / /  / /_/ / /_/ / ____/ / /
/_/    \__,_/____/____/ |__/|__/\____/_/   \__,_/\____/_/     /_/
"""

DEFAULT_MODEL = "gpt-5.5"
MAX_WORDS = 500
OUTPUT_FILE = "passwords.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a password dictionary for authorized security audits "
            "using the OpenAI API."
        )
    )
    parser.add_argument(
        "-a",
        "--amount",
        nargs="?",
        default=20,
        type=int,
        help="Number of passwords to generate.",
    )
    parser.add_argument(
        "-w",
        "--words",
        nargs="+",
        help="Base words separated by commas.",
    )
    return parser.parse_args()


def normalize_words(raw_words: list[str] | None) -> list[str]:
    if not raw_words:
        return []

    # Accept both "finance,2023" and "finance, 2023" without changing the CLI.
    words_text = " ".join(raw_words)
    return [word.strip() for word in words_text.split(",") if word.strip()]


def build_prompt(amount: int, words: list[str]) -> str:
    return (
        f"Create {amount} password dictionary candidates for an authorized "
        f"security audit using this context: {', '.join(words)}. "
        "Return only the candidates, one per line, without numbering or extra text."
    )


def extract_output_text(response_data: dict[str, Any]) -> str:
    if isinstance(response_data.get("output_text"), str):
        return response_data["output_text"].strip()

    output_parts: list[str] = []
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                output_parts.append(content["text"])

    if output_parts:
        return "\n".join(output_parts).strip()

    raise ValueError("The API response did not include text output.")


def chat_with_gpt(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not configured.")
        print("Set it in your environment before running PasswordGPT.")
        sys.exit(1)

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    sys.stdout.write(" -> Requesting the wordlist from OpenAI... ")
    sys.stdout.flush()

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model,
        "instructions": (
            "You generate password dictionary candidates only for authorized "
            "security auditing. Return plain text only."
        ),
        "input": prompt,
        "temperature": 0.3,
        "max_output_tokens": 1000,
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
    except requests.RequestException as exc:
        print(f"ERROR: Could not connect to OpenAI: {exc}")
        sys.exit(1)

    if response.status_code != 200:
        print(f"ERROR: OpenAI API returned HTTP {response.status_code}.")
        try:
            error_data = response.json().get("error", {})
            if error_data.get("message"):
                print(f"Details: {error_data['message']}")
        except ValueError:
            pass
        sys.exit(1)

    try:
        response_data = response.json()
        word_list = extract_output_text(response_data)
    except (KeyError, TypeError, ValueError) as exc:
        print(f"ERROR: Could not read the OpenAI response: {exc}")
        sys.exit(1)

    if not word_list:
        print("ERROR: OpenAI returned an empty wordlist.")
        sys.exit(1)

    sys.stdout.write("Received!\n")
    sys.stdout.flush()
    return word_list


def main() -> None:
    print(BANNER)
    args = parse_args()

    if args.amount <= 0:
        print("ERROR: Amount must be greater than 0.")
        sys.exit(1)

    words = normalize_words(args.words)
    if not words:
        print("ERROR: Please provide information to generate the password dictionary.")
        sys.exit(1)

    if len(words) > MAX_WORDS:
        print(f"ERROR: Word list too long. The current limit is {MAX_WORDS} words.")
        sys.exit(1)

    prompt = build_prompt(args.amount, words)
    chat_gpt_results = chat_with_gpt(prompt)

    # The default output path is kept for compatibility with the original CLI.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(chat_gpt_results)
        if not chat_gpt_results.endswith("\n"):
            file.write("\n")

    file_path = os.path.abspath(OUTPUT_FILE)
    sys.stdout.write(f"\n -> Password list created on: {file_path}\n\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
