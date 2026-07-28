import re
from preprocess import preprocess_text
from spell_corrector import correct_spelling
from synonym_mapper import map_synonyms
from scoring_engine import recommend_best_career, find_mentioned_career
from intent_router import detect_followup
from memory import memory

# Minimum confidence score required to return a recommendation
MIN_SCORE_THRESHOLD = 35


def _format_list_item(obj):
    """Format a single item from a list field (roadmap / projects / companies)."""
    if isinstance(obj, dict):
        if "step" in obj:
            return f"{obj['step']}. {obj['title']}"
        elif "difficulty" in obj:
            return f"• {obj['title']} ({obj['difficulty']})"
    return f"• {obj}"


def _format_followup(intent, career):
    """
    Build a nicely formatted response for a follow-up intent
    (roadmap, salary, skills, companies, projects, description).
    """

    if intent == "roadmap":
        lines = [f"📍 Roadmap — {career['career']}:", ""]
        for step in career["roadmap"]:
            lines.append(f"  {step['step']}. {step['title']}")
        return "\n".join(lines)

    if intent == "salary":
        sal = career["salary"]
        return (
            f"💰 Salary — {career['career']}:\n\n"
            f"  Entry Level : {sal.get('entry', 'N/A')}\n"
            f"  Mid Level   : {sal.get('mid', 'N/A')}\n"
            f"  Senior Level: {sal.get('senior', 'N/A')}"
        )

    if intent == "skills":
        lines = [f"🛠️ Skills — {career['career']}:", ""]
        for category, skill_list in career["skills"].items():
            lines.append(f"  {category}:")
            for skill in skill_list:
                lines.append(f"    • {skill}")
        return "\n".join(lines)

    if intent == "companies":
        lines = [f"🏢 Top Companies — {career['career']}:", ""]
        for company in career["companies"]:
            lines.append(f"  • {company}")
        return "\n".join(lines)

    if intent == "projects":
        lines = [f"💡 Project Ideas — {career['career']}:", ""]
        for project in career["projects"]:
            lines.append(f"  • {project['title']} ({project['difficulty']})")
        return "\n".join(lines)

    if intent == "description":
        return (
            f"📖 About — {career['career']}:\n\n"
            f"  {career['description']}"
        )

    return None


def recommend_career(user_text):
    """
    Main entry point called by Rasa actions and Streamlit app.

    Returns:
      - dict  → new career recommendation (has 'career', 'confidence', etc.)
      - str   → follow-up answer or error message
      - None  → no match found
    """

    # ── Step 1: Check for follow-up intent ──
    followup_intent = detect_followup(user_text)

    if followup_intent:
        # Check if user explicitly mentioned a career in the follow-up sentence
        # e.g. "how much salary i can expect for ai engineer" or "need web development roadmap"
        target_career = find_mentioned_career(user_text)

        if not target_career:
            # Strip follow-up intent trigger words to analyze the target domain/career
            intent_keywords = [
                "roadmap", "path", "learning path", "steps",
                "skills", "skill", "technologies", "technology",
                "salary", "package", "income", "pay", "ctc",
                "projects", "project", "companies", "company", "hiring",
                "courses", "course", "description", "about", "future", "scope",
                "need", "give", "show", "tell", "what", "how", "is", "the", "for", "me", "i", "a", "an"
            ]
            clean_query = user_text.lower()
            for kw in intent_keywords:
                clean_query = re.sub(r'\b' + re.escape(kw) + r'\b', '', clean_query)
            clean_query = clean_query.strip()

            if clean_query:
                corrected = correct_spelling(clean_query)
                mapped    = map_synonyms(corrected)
                processed = preprocess_text(mapped)
                scored_res = recommend_best_career(processed)
                if scored_res and scored_res.get("confidence", 0) >= 30:
                    target_career = scored_res

        # Fallback to active career in session memory
        if not target_career:
            target_career = memory.get_career()

        if target_career is None:
            return "Please ask for a career recommendation first! 😊"

        # Update memory to the newly identified target career
        memory.set_career(target_career)
        return _format_followup(followup_intent, target_career)

    # ── Step 2: Full NLP pipeline ──
    corrected = correct_spelling(user_text)
    mapped    = map_synonyms(corrected)
    processed = preprocess_text(mapped)

    # ── Step 3: Score against career database ──
    result = recommend_best_career(processed)

    if result is None or result.get("confidence", 0) < MIN_SCORE_THRESHOLD:
        return None

    # ── Step 4: Store in memory for follow-up questions ──
    memory.set_career(result)

    return result


if __name__ == "__main__":
    tests = [
        "I love machine learning",
        "need ai web development roadmap",
        "salary for business analyst",
        "skills for ui ux designer",
    ]
    for msg in tests:
        print(f"\n>>> {msg}")
        resp = recommend_career(msg)
        if isinstance(resp, dict):
            print(f"Career: {resp['career']}  |  Confidence: {resp['confidence']}")
        else:
            print(resp)