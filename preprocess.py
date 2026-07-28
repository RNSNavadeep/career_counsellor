import nltk

# Ensure necessary NLTK data packages exist before tokenizing/lemmatizing
def _ensure_nltk_data():
    packages = ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass

_ensure_nltk_data()

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

try:
    stop_words = set(stopwords.words("english"))
except Exception:
    stop_words = set()

lemmatizer = WordNetLemmatizer()

# Words that must NOT be removed even if they appear in stopwords
IMPORTANT_WORDS = {
    "not", "no", "but", "love", "like", "enjoy", "want", "art", "ui", "ux", "seo", "ba", "fa"
}


def preprocess_text(text):
    """
    Clean and normalize a user sentence for the scoring engine.

    Steps:
      1. Lowercase
      2. Tokenize using NLTK word_tokenize with fallback
      3. Remove punctuation tokens
      4. Remove stopwords (preserving key domain words)
      5. Lemmatize words using NLTK WordNetLemmatizer
    """
    text = text.lower()

    try:
        tokens = word_tokenize(text)
    except Exception:
        # Fallback basic whitespace/punctuation splitting if NLTK tokenizer encounters an issue
        import re
        tokens = re.findall(r'\b\w+\b', text)

    cleaned_tokens = []

    for token in tokens:
        if not token.isalpha():
            continue

        if token in stop_words and token not in IMPORTANT_WORDS:
            continue

        try:
            lemmatized = lemmatizer.lemmatize(token)
        except Exception:
            lemmatized = token

        cleaned_tokens.append(lemmatized)

    return " ".join(cleaned_tokens)


if __name__ == "__main__":
    sample = "I love Machine Learning, Figma UI design, and Financial Modeling!"
    print("Preprocessed output:", preprocess_text(sample))
