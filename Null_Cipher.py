# hidden_message_extractor.py
import re

def extract_hidden_message(text: str, every_nth_word: int = 3, every_mth_char: int = 2) -> str:
    """
    Implements a Null Cipher: extracts hidden letters from a text
    by taking every `every_mth_char` character of every `every_nth_word`.
    """
    all_words = re.findall(r'\S+', text)
    secret_chars = []

    for idx, word in enumerate(all_words, start=1):
        if idx % every_nth_word == 0:
            secret_chars.extend(word[1::every_mth_char])

    return ''.join(secret_chars)


if __name__ == "__main__":
    sample_text = (
        "Here is a completely normal looking paragraph, "
        "but cleverly hidden inside are some secret letters "
        "you might not notice at first glance."
    )
    hidden = extract_hidden_message(sample_text, every_nth_word=4, every_mth_char=2)
    print("Recovered hidden message:", hidden)
