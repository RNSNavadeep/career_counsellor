from spellchecker import SpellChecker

# Create spell checker and add known domain words (tech, design, commerce)
# so they are not incorrectly "corrected"
spell = SpellChecker()

DOMAIN_WORDS = [
    # Tech
    "python", "tensorflow", "pytorch", "numpy", "pandas",
    "matplotlib", "seaborn", "sklearn", "scikit", "keras",
    "fastapi", "flask", "django", "nodejs", "reactjs", "vuejs",
    "angular", "typescript", "javascript", "mongodb", "postgresql",
    "redis", "kubernetes", "docker", "terraform", "ansible",
    "jenkins", "mlflow", "kubeflow", "airflow",
    "tableau", "powerbi", "nextjs", "tailwind",
    "nlp", "cv", "ai", "ml", "dl", "bi", "pbi",
    "devops", "mlops", "cicd", "aws", "gcp", "azure",
    "mern", "mean", "api", "sql", "nosql", "llm",
    "chatbot", "rasa", "transformers", "bert", "gpt",
    "cybersecurity", "pentest", "pentesting", "kali", "burpsuite",
    "owasp", "siem", "soc", "xgboost", "lightgbm",

    # Arts & Design
    "figma", "uiux", "wireframing", "prototyping", "canva",
    "photoshop", "illustrator", "indesign", "behance", "dribbble",
    "sketching", "typography", "branding",

    # Commerce & Business
    "seo", "sem", "semrush", "ahrefs", "cro", "copywriting",
    "swot", "bpmn", "jira", "confluence", "lucidchart",
    "dcf", "lbo", "valuation", "gaap", "ifrs", "bloomberg",
    "agile", "scrum", "kanban"
]

spell.word_frequency.load_words(DOMAIN_WORDS)


def correct_spelling(text):
    """
    Correct spelling mistakes in the given text.
    Unknown words that cannot be corrected fall back to the original word.
    Whitelisted domain terms are preserved as-is.
    """
    corrected_words = []

    for word in text.split():
        correction = spell.correction(word)

        # spell.correction() returns None when no suggestion is found
        # In that case, keep the original word
        if correction is None:
            corrected_words.append(word)
        else:
            corrected_words.append(correction)

    return " ".join(corrected_words)


if __name__ == "__main__":
    sentence = "I want to lern pyhton and machne learnng or design in fgma"
    print(correct_spelling(sentence))