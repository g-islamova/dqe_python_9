import re
from typing import List


def capitalize_first_word(text: str) -> str:
    """
    Capitalizes the first word of each sentence in the given text.

    Args:
    text (str): The text to capitalize.

    Returns:
    str: The capitalized text.
    """
    # Split the text into sentences
    sentences = re.split(r'(?<=[.?!:\n])\s*', text)

    # Capitalize the first word of each sentence
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]

    # Join the sentences back into a single string
    capitalized_text = ' '.join(capitalized_sentences)

    return capitalized_text


def normalize_text(text: str) -> str:
    """
    Normalizes the text by converting it to lowercase and fixing the misspelling 'iz' to 'is'.

    Args:
    text (str): The text to normalize.

    Returns:
    str: The normalized text.
    """
    return text.lower().replace(" iz ", " is ")


def count_whitespace_characters(text: str) -> int:
    """
    Counts the number of whitespace characters (spaces, tabs, and newlines) in the given text.

    Args:
    text (str): The text to count whitespace characters in.

    Returns:
    int: The count of whitespace characters.
    """
    return sum(1 for char in text if char in ' \t\n')


def get_last_words(text: str) -> List[str]:
    """
    Extracts the last word from each sentence in the given text.

    Args:
    text (str): The text to extract last words from.

    Returns:
    list: A list of last words.
    """
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
    return [sentence.split()[-1] for sentence in sentences]


def add_last_words_sentence(text: str, last_words: List[str]) -> str:
    """
    Adds a new sentence containing the last words of each sentence to the end of the given text.

    Args:
    text (str): The original text.
    last_words (list): A list of last words from each sentence.

    Returns:
    str: The text with the new sentence added.
    """
    new_sentence = " ".join(last_words) + "."
    return text + "\n\n" + new_sentence.capitalize()


def main(text_to_format: str):
    """
    Main function to execute the script.
    :param text_to_format: text to be normalised
    """

    normalized_text = normalize_text(text_to_format)
    capitalized_text = capitalize_first_word(normalized_text)

    print("Normalized and capitalized text:\n", capitalized_text)