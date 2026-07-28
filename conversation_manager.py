"""
conversation_manager.py

Handles follow-up question routing using memory + intent_router.
This module is used by app.py for the standalone CLI chatbot.
"""

from memory import memory
from intent_router import detect_followup


def handle_followup(user_message):
    """
    Check if the user's message is a follow-up question.
    If it is, return the appropriate info from the last recommended career.
    Returns None if the message is NOT a follow-up.
    """

    intent = detect_followup(user_message)

    if intent is None:
        return None

    career = memory.get_career()

    if career is None:
        return "Please ask for a career recommendation first. 😊"

    if intent == "roadmap":
        lines = [f"\n📍 Roadmap — {career['career']}:\n"]
        for step in career["roadmap"]:
            lines.append(f"  {step['step']}. {step['title']}")
        return "\n".join(lines)

    if intent == "skills":
        lines = [f"\n🛠️  Skills — {career['career']}:\n"]
        for category, skill_list in career["skills"].items():
            lines.append(f"  {category}:")
            for skill in skill_list:
                lines.append(f"    • {skill}")
        return "\n".join(lines)

    if intent == "salary":
        sal = career["salary"]
        return (
            f"\n💰 Salary — {career['career']}:\n\n"
            f"  Entry Level  : {sal.get('entry', 'N/A')}\n"
            f"  Mid Level    : {sal.get('mid', 'N/A')}\n"
            f"  Senior Level : {sal.get('senior', 'N/A')}"
        )

    if intent == "companies":
        lines = [f"\n🏢 Top Companies — {career['career']}:\n"]
        for company in career["companies"]:
            lines.append(f"  • {company}")
        return "\n".join(lines)

    if intent == "projects":
        lines = [f"\n💡 Project Ideas — {career['career']}:\n"]
        for project in career["projects"]:
            lines.append(f"  • {project['title']} ({project['difficulty']})")
        return "\n".join(lines)

    if intent == "description":
        return (
            f"\n📖 About — {career['career']}:\n\n"
            f"  {career['description']}"
        )

    if intent == "future":
        return f"\n🔮 Future Scope — {career['career']}:\nThis field has strong growth prospects globally."

    if intent == "courses":
        return (
            f"\n📚 Courses for {career['career']}:\n\n"
            "  • Coursera / edX — University-level courses\n"
            "  • Udemy — Practical hands-on projects\n"
            "  • YouTube — Free tutorials\n"
            "  • Official Docs — Always the most accurate source"
        )

    return None