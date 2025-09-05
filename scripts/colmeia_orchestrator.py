#!/usr/bin/env python3
"""
colmeia_orchestrator.py: Script to coordinate calls between Biel, Bruno and Martinho in the Colmeia ecosystem.
This script orchestrates tasks such as health checks, SafePoints, and chapter generation using Notion and OpenAI APIs.
It can be invoked via CLI with subcommands to run routines or by other automation tools.
"""

import argparse
from datetime import datetime
import os
import requests


def call_biel(prompt: str, api_key: str) -> str:
    """Send a prompt to Biel (ChatGPT) and return the response."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are Biel, a creative AI in the Colmeia ecosystem."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def call_bruno(text: str):
    """Placeholder for Bruno's organizational functions."""
    # For now, just return the text
    return text


def call_martinho(task: str):
    """Placeholder for Martinho's execution logic."""
    # For now, just print the task
    return f"Executing task: {task}"


def main():
    parser = argparse.ArgumentParser(description="Colmeia orchestrator for Biel, Bruno, Martinho.")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand to generate chapter using Biel and Bruno
    gen_chapter = subparsers.add_parser("generate_chapter", help="Generate a chapter using Biel and Bruno")
    gen_chapter.add_argument("--title", required=True, help="Title of the chapter")
    gen_chapter.add_argument("--content", required=True, help="Conversation content to transform into chapter")
    gen_chapter.add_argument("--api-key", required=False, default=os.getenv("OPENAI_API_KEY"), help="OpenAI API key")

    # Subcommand to run health check (Martinho)
    health_check = subparsers.add_parser("health_check", help="Run a health check routine")
    health_check.add_argument("--description", default="Routine health check", help="Description for the health check")

    args = parser.parse_args()

    if args.command == "generate_chapter":
        if not args.api_key:
            raise SystemExit("OpenAI API key required via --api-key or OPENAI_API_KEY environment variable")
        # Call Biel to summarize/generate ideas
        summary = call_biel(args.content, args.api_key)
        # Call Bruno to structure summary
        structured = call_bruno(summary)
        # Output the result
        print(f"# {args.title}\n\n{structured}")

    elif args.command == "health_check":
        result = call_martinho(args.description)
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
