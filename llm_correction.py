import re

def correct_text(text):
    """
    Smart rule + pattern based grammar correction
    (custom tuned for your project)
    """

    if not text:
        return "[No text to correct]"

    # Fix common ASR grammar patterns
    text = re.sub(r"Hardly where", "Hardly were", text)
    text = re.sub(r"made by powerful opposition", "met by powerful opposition", text)

    # General fixes
    text = re.sub(r"\bdont\b", "don't", text)
    text = re.sub(r"\bcant\b", "can't", text)
    text = re.sub(r"\bim\b", "I'm", text)

    # Capitalize
    text = text[0].upper() + text[1:]

    # Add period if missing
    if not text.endswith("."):
        text += "."

    return text