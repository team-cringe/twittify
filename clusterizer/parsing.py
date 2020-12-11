from regex import match, search
from string import punctuation
from emoji import UNICODE_EMOJI


def is_symbol(word) -> bool:
    """
    Return True if a word contains only symbols.

    Parameters:
        word (str): A word to check.
    """
    return bool(match(fr'[{punctuation} \n_`«»“”️–]', word))


def is_emoji(word) -> bool:
    """
    Return True if a word contains only emojis.

    Parameters:
        word (str): A word to check.
    """
    return word in UNICODE_EMOJI


def is_latin(word):
    """
    Return True if a word contains only letters of the latin alphabet.

    Parameters:
        word (str): A word to check.
    """
    return bool(match(r'\p{IsLatin}', word))


def is_number(word):
    """
    Return True if a word is a number.

    Parameters:
        word (str): A word to check.
    """
    return word.replace('.', '', 1).isdigit()


def is_url(word):
    """
    Return True if a word is URL.

    Parameters:
        word (str): A word to check.
    """
    return bool(match(r'http[s]?://\S+', word))


def is_mention(word):
    """
    Return True if a word is Twitter mention.
    e.g., `@realDonaldTrump`.

    Parameters:
        word (str): A word to check.
    """
    return bool(match(r'@\p{IsLatin}+', word))


def has_postfix(word):
    """
    Return True if a word has a russian postfix.

    Parameters:
        word (str): A word to check.
    """
    return bool(search(r'(-то|-за|-либо|-нибудь)', word))


def remove_word_if(sentence, f) -> str:
    """
    Remove word from a sentence that match a specified condition.

    Parameters:
        sentence (str): Sentence represented as string.
        f ((str) -> str): Remove `w` if `f(w)` is True.

    Return:
        Sentence (str) with words removed.
    """
    return ' '.join([
        w if not f(w) else ''
        for w in sentence.split(' ')
    ])
