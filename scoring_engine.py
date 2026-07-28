import re
from rapidfuzz import fuzz
from career_data.career_database import career_data


def find_mentioned_career(user_text):
    """
    Check if the user explicitly mentioned a specific career name in their message.
    e.g. 'salary for ai engineer', 'roadmap of ui ux designer', 'skills for business analyst'
    Returns the career dict if found, else None.
    """
    text = user_text.lower()

    # Sort careers by name length descending so 'full stack developer' matches before 'developer'
    for name, career in sorted(career_data.items(), key=lambda x: len(x[0]), reverse=True):
        c_name = name.lower()

        # Check exact career name or common variants
        if c_name in text:
            return career

        # Check keyword aliases for exact career names
        aliases = [
            c_name.replace(" ", ""),
            c_name.replace("developer", "dev"),
            c_name.replace("engineer", "eng"),
            c_name.replace("designer", "design"),
            c_name.replace("analyst", "analytics"),
            c_name.replace("marketer", "marketing")
        ]
        for alias in aliases:
            if len(alias) > 3 and alias in text:
                return career

    return None


def calculate_score(user_text, career):
    score = 0
    matched = []

    text = user_text.lower()
    c_name = career["career"].lower()

    # Direct career name match (e.g. "I want to be an AI Engineer" or "UI UX Designer")
    if c_name in text:
        score += 100
        matched.append(career["career"])

    # Keywords scoring
    for keyword in career.get("keywords", []):
        key = keyword.lower()

        # For short abbreviations (<= 3 chars e.g. 'ui', 'ai', 'ml', 'bi', 'seo'), enforce exact word boundary match
        if len(key) <= 3:
            if re.search(r'\b' + re.escape(key) + r'\b', text):
                score += 80
                matched.append(key)
            continue

        # Exact sentence or phrase match
        if text == key:
            score += 100
            matched.append(key)

        # Substring keyword match with word boundaries
        elif re.search(r'\b' + re.escape(key) + r'\b', text):
            score += 90
            matched.append(key)

        # Fuzzy similarity for minor variations (only for longer words)
        else:
            similarity = fuzz.ratio(text, key)
            if similarity >= 80:
                score += similarity * 0.4
                matched.append(key)

    # Interests scoring
    for interest in career.get("interests", []):
        int_key = interest.lower()
        if re.search(r'\b' + re.escape(int_key) + r'\b', text):
            score += 25
            matched.append(interest)

    return score, list(set(matched))


def recommend_best_career(user_text):

    best_score = -1
    best = None
    matches = []

    for career in career_data.values():

        score, matched = calculate_score(
            user_text,
            career
        )

        if score > best_score:
            best_score = score
            best = career
            matches = matched

    if best is None:
        return None

    result = best.copy()

    # Cap confidence at 100%
    result["confidence"] = min(int(best_score), 100)
    result["matched_keywords"] = matches

    return result