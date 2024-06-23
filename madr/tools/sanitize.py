import string
from unicodedata import normalize


def sanitize_str(input_str: str):
    sanitized = ' '.join(normalize('NFKC', input_str).split()).lower()
    return sanitized.translate(str.maketrans('', '', string.punctuation))
