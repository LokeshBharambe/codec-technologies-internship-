import re

def auto_punctuate(text: str) -> str:
    """
    Simple auto-punctuation:
    - capitalizes sentences
    - adds missing periods
    """

    text = text.strip()

    if not text:
        return text

    # split into sentences by pauses or probable breaks
    sentences = re.split(r'(?<=[a-zA-Z0-9])\s+(?=[A-Z])|(?<=[.!?])\s+', text)

    cleaned = []
    for s in sentences:
        s = s.strip()

        if not s:
            continue

        # capitalize first letter
        s = s[0].upper() + s[1:]

        # add period if none
        if s[-1] not in ".!?":
            s += "."

        cleaned.append(s)

    return " ".join(cleaned)
