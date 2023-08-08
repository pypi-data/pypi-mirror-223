import re
from unidecode import unidecode


def clean_text(text: str) -> str:
    """[This function converts characters to ascii and keeps only letters and numbers.]

    Args:
        text (str): [Text that has to be cleaned]

    Returns:
        str: [Cleaned text]
    """
    try:
        text = str(text) if text is not None else ''
        if isinstance(text, str):
            text = unidecode(text.lower())
            text = re.sub('[^a-z0-9]+', ' ', text)
            return text.strip()
        else:
            raise ValueError('text is not a string')
    except:
        return ''
    