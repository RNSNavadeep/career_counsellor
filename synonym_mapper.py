import re

SYNONYMS = {

    # ── Longer / more specific entries FIRST ─────────────────────────────────
    # BI / Analytics — pbi MUST come before bi
    "pbi": "power bi",
    "powerbi": "power bi",
    "power bi": "power bi",
    "bi": "business intelligence",
    "predictive analytics": "predictive analytics",
    "predictive modeling": "predictive analytics",
    "predictive analysis": "predictive analytics",
    "analyzing datasets": "data analysis",
    "analyzing data": "data analysis",
    "datasets": "dataset",

    # AI / ML / DL shortcuts
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",

    # Data Science & Analytics
    "ds": "data science",
    "datascience": "data science",
    "data analytics": "data analysis",

    # Web & Software
    "web": "web development",
    "webdev": "web development",
    "frontend": "frontend",
    "backend": "backend",
    "fullstack": "full stack",
    "full-stack": "full stack",
    "software": "software development",

    # Security
    "cyber": "cyber security",
    "cybersec": "cyber security",
    "infosec": "cyber security",
    "ethical hacking": "cyber security",

    # Cloud / DevOps
    "cloud": "cloud computing",
    "devops": "devops",
    "k8s": "kubernetes",
    "cicd": "ci cd",
    "ci/cd": "ci cd",

    # Arts & Design
    "ui": "user interface",
    "ux": "user experience",
    "ui/ux": "ui ux designer",
    "uiux": "ui ux designer",
    "figma": "figma",
    "sketching": "drawing",
    "graphic": "graphic design",
    "photoshop": "photoshop",
    "illustrator": "illustrator",

    # Commerce & Business
    "digital marketing": "digital marketing",
    "seo": "search engine optimization",
    "sem": "search engine marketing",
    "marketing": "digital marketing",
    "business analyst": "business analyst",
    "business analysis": "business analysis",
    "ba": "business analyst",
    "financial analyst": "financial analyst",
    "financial analysis": "financial analysis",
    "fa": "financial analyst",
    "financial modeling": "financial modeling",
    "dcf": "financial modeling",
    "valuation": "valuation",
    "accounting": "accounting",

    # Frameworks & Tools
    "tf": "tensorflow",
    "pt": "pytorch",
    "sklearn": "scikit-learn",
}

# Pre-sort synonyms by key length descending
_SORTED_SYNONYMS = sorted(SYNONYMS.items(), key=lambda x: len(x[0]), reverse=True)


def map_synonyms(text):
    """
    Replace known abbreviations and alternate terms with their standard forms.
    Uses a placeholder technique so replaced text is not processed again.
    """
    text = text.lower()

    placeholders = {}   # index → replacement string
    idx = 0

    for word, replacement in _SORTED_SYNONYMS:
        pattern = r'(?<![a-z])' + re.escape(word) + r'(?![a-z])'
        if re.search(pattern, text):
            ph = f'##PLACEHOLDER{idx}##'
            placeholders[ph] = replacement
            text = re.sub(pattern, ph, text)
            idx += 1

    # Restore placeholders in the order they appear
    for ph, value in placeholders.items():
        text = text.replace(ph, value)

    return text


if __name__ == "__main__":
    tests = [
        "I like AI and ML",
        "I enjoy UI/UX design with Figma",
        "I want to learn SEO and Digital Marketing",
        "I like financial modeling and DCF valuation",
    ]
    for t in tests:
        print(f"  IN : {t}")
        print(f"  OUT: {map_synonyms(t)}")
        print()