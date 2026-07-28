"""
app.py — Standalone CLI Chatbot for AI Career Counsellor

Run this to use the chatbot without Rasa:
    python app.py

The full NLP pipeline is used:
    Spell Correction → Synonym Mapping → Preprocessing → Scoring Engine → Response

Follow-up questions are also supported:
    After a recommendation, type: roadmap / salary / skills / companies / projects
"""

import sys
import io

# Fix Windows terminal encoding so emojis print correctly
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stdin  = io.TextIOWrapper(sys.stdin.buffer,  encoding="utf-8", errors="replace")

from recommendation import recommend_career
from response_generator import build_response

BANNER = """
╔══════════════════════════════════════════════════════════╗
  🤖  AI Virtual Career Counsellor
  Powered by NLP + RapidFuzz Scoring Engine
╚══════════════════════════════════════════════════════════╝

  Tell me about your interests or skills, and I'll
  recommend the best career path for you!

  Examples:
    • I love machine learning
    • I enjoy making dashboards using Power BI
    • I like ethical hacking and networks
    • I want to work with cloud computing on AWS

  After a recommendation, ask:
    roadmap / salary / skills / companies / projects

  Type 'quit' or 'exit' to leave.
══════════════════════════════════════════════════════════
"""

GREETINGS = {"hi", "hello", "hey", "good morning", "good evening", "good afternoon"}
GOODBYES  = {"bye", "goodbye", "exit", "quit", "q", "thanks", "thank you"}


def format_response(result):
    """Convert a result from recommend_career() into a printable string."""

    if result is None:
        return (
            "\n⚠️  I couldn't find a matching career.\n"
            "   Try describing your interests in more detail.\n"
            "   Example: 'I love Python and deep learning'\n"
        )

    if isinstance(result, str):
        return f"\n{result}\n"

    if isinstance(result, dict):
        return build_response(result)

    return "\n❓ Unknown response type.\n"


def run():
    print(BANNER)

    while True:
        try:
            user_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  👋 Goodbye! Best of luck with your career! 🌟\n")
            break

        if not user_input:
            continue

        lower = user_input.lower()

        # Handle exits
        if lower in GOODBYES:
            print("\n  👋 Goodbye! Best of luck with your career! 🌟\n")
            break

        # Handle greetings
        if lower in GREETINGS:
            print(
                "\n  Bot: 👋 Hello! Tell me about your interests or skills\n"
                "       and I'll find the perfect career for you! 🚀\n"
            )
            continue

        # Process through the full recommendation pipeline
        result = recommend_career(user_input)

        response = format_response(result)

        print(f"\n  Bot: {response}")


if __name__ == "__main__":
    run()