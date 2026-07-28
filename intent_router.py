ROADMAP = [
    "roadmap",
    "path",
    "learning path",
    "steps"
]

SKILLS = [
    "skills",
    "skill",
    "technologies",
    "technology"
]

SALARY = [
    "salary",
    "package",
    "income",
    "pay"
]

PROJECTS = [
    "projects",
    "project"
]

COMPANIES = [
    "companies",
    "company",
    "hiring"
]

COURSES = [
    "courses",
    "course"
]

DESCRIPTION = [
    "description",
    "about"
]

FUTURE = [
    "future",
    "scope"
]

def detect_followup(text):

    text = text.lower()

    if any(word in text for word in ROADMAP):
        return "roadmap"

    if any(word in text for word in SKILLS):
        return "skills"

    if any(word in text for word in SALARY):
        return "salary"

    if any(word in text for word in PROJECTS):
        return "projects"

    if any(word in text for word in COMPANIES):
        return "companies"

    if any(word in text for word in COURSES):
        return "courses"

    if any(word in text for word in DESCRIPTION):
        return "description"

    if any(word in text for word in FUTURE):
        return "future"

    return None