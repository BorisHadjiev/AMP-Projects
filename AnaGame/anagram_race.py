from itertools import permutations
from valid_anagame_words import get_valid_word_list
#from TimingProfiler import TimingProfiler


def basic_checks(word1: str, word2: str) -> tuple[bool, str, str]:
    """
    Performs basic top-level checks on two words to prepare them for anagram testing.
    Removes characters other than A-Z, a-z from each word.

    Basic top-level checks include ensuring the two input words:
        -aren't be the same word
        -are compared in a case insensitive manner
        -have the same length, with at least three letters

    Args:
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        tuple[bool, str, str]: A tuple containing:
            - A boolean indicating if the words pass the basic checks.
            - The lowercase, cleansed version of word1.
            - The lowercase, cleansed version of word2.

    Examples:
    >>> basic_checks("Listen", "Silent")
    (True, 'listen', 'silent')
    >>> basic_checks("1_Apple", "Pale5")
    (False, 'apple', 'pale')
    >>> basic_checks("abc", "abc")
    (False, 'abc', 'abc')
    """

    cleansed_word1 = ""
    cleansed_word2 = ""  

    for letter in word1.lower():
        if letter in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
            cleansed_word1 = cleansed_word1 + letter
    for letter in word2.lower():
        if letter in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
            cleansed_word2 = cleansed_word2 + letter

    if len(cleansed_word1) == len(cleansed_word2) and len(cleansed_word1) >= 3 and len(cleansed_word2) >=3 and cleansed_word1 != cleansed_word2:
        return((True, cleansed_word1, cleansed_word2))
    
    else:
        return((False, cleansed_word1, cleansed_word2))


def is_anagram_exhaustive(word1: str, word2: str) -> bool:
    """
    Determines whether two words are anagrams by generating all permutations of the first word.
    itertools.permutations is used to generate all possible arrangements of the characters in word1.
    
    Args:
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        bool: True if the words are anagrams, False otherwise.

    Examples:
    >>> is_anagram_exhaustive("listen", "silent")
    True
    >>> is_anagram_exhaustive("apple", "pale")
    False
    >>> is_anagram_exhaustive("actors", "costar")
    True
    """ 

    pass_quick_checks, cleansed_word1, cleansed_word2 = basic_checks(word1, word2)

    if not pass_quick_checks:
        return False

    if tuple(cleansed_word1) in set(permutations(cleansed_word2)):
        return True
    
    else: 
        return False


def is_anagram_checkoff(word1: str, word2: str) -> bool:
    """
    Determines whether two words are anagrams by checking off characters.
    Since strings are immutable, a parallel list-based version of one word is created.
    Letters in the list are set to None as they are found in the other word.

    Args:
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        bool: True if the words are anagrams, False otherwise.

    Examples:
    >>> is_anagram_checkoff("listen", "silent")
    True
    >>> is_anagram_checkoff("apple", "pale")
    False
    >>> is_anagram_checkoff("actors", "costar")
    True
    """

    pass_quick_checks, cleansed_word1, cleansed_word2 = basic_checks(word1, word2)

    if not pass_quick_checks:
        return False


    word2_list = []
    
    for letter in cleansed_word2:
        word2_list.append(letter)

    for letter in cleansed_word1:
        if letter in word2_list:
            word2_list.remove(letter)
        else:
            return False
    
    if len(word2_list) == 0:
        return True

    return False 


def is_anagram_lettercount(word1: str, word2: str) -> bool:
    """
    Determines whether two words are anagrams by counting the occurrences of each letter.

    Args:
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        bool: True if the words are anagrams, False otherwise.

    Examples:
    >>> is_anagram_lettercount("listen", "silent")
    True
    >>> is_anagram_lettercount("apple", "pale")
    False
    >>> is_anagram_lettercount("actors", "costar")
    True
    """

    pass_quick_checks, cleansed_word1, cleansed_word2 = basic_checks(word1, word2)

    if not pass_quick_checks:
        return False

    word1_letter_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0,
    'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0,
    'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0,
    'w': 0, 'x': 0, 'y': 0, 'z': 0 }

    word2_letter_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0,
    'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0,
    'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0,
    'w': 0, 'x': 0, 'y': 0, 'z': 0 }

    for letter in cleansed_word1:
        word1_letter_count[letter] += 1

    for letter in cleansed_word2:
        word2_letter_count[letter] += 1
    
    if word1_letter_count == word2_letter_count:
        return True
    
    return False

def is_anagram_sort(word1: str, word2: str) -> bool:
    """
    Determines whether two words are anagrams by sorting their characters.

    Args:
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        bool: True if the words are anagrams, False otherwise.

    Examples:
    >>> is_anagram_sort("listen", "silent")
    True
    >>> is_anagram_sort("apple", "pale")
    False
    >>> is_anagram_sort("actors", "costar")
    True
    """

    pass_quick_checks, cleansed_word1, cleansed_word2 = basic_checks(word1, word2)

    if not pass_quick_checks:
        return False

    return sorted([letter] for letter in cleansed_word1) == sorted([letter] for letter in cleansed_word2)  

ch_to_prime = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
    'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43,
    'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79,
    'w': 83, 'x': 89, 'y': 97, 'z': 101 }

def generate_hash(word: str) -> int:
    """
    Computes a hash value for a string using prime number multiplication.
    The ch_to_prime dictionary is provided to map each lowercase character to a unique prime number. 
    #print(chToprime['e']*chToprime['a']*chToprime['t']) -> 11*2*71 -> 1562
    
    Args:
        word (str): The input string.

    Returns:
        int: The computed hash value.

    Examples:
    >>> generate_hash("abc")
    30
    >>> generate_hash("cab")
    30
    >>> generate_hash("")
    1
    >>> generate_hash("eat")
    1562
    """

    hash = 1 

    for letter in word:
        hash = hash * ch_to_prime[letter]

    return hash

def is_anagram_prime_hash(word1: str, word2: str) -> bool:
    """
    Determines whether two words are anagrams using a prime number hash.

    Args:
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        bool: True if the words are anagrams, False otherwise.

    Examples:
    >>> is_anagram_prime_hash("listen", "silent")
    True
    >>> is_anagram_prime_hash("apple", "pale")
    False
    >>> is_anagram_prime_hash("actors", "costar")
    True
    """

    pass_quick_checks, cleansed_word1, cleansed_word2 = basic_checks(word1, word2)

    if not pass_quick_checks:
        return False
    
    return generate_hash(cleansed_word1) == generate_hash(cleansed_word2)

if __name__ == "__main__":
    #algorithms=[ is_anagram_exhaustive,is_anagram_checkoff, is_anagram_lettercount, is_anagram_prime_hash, is_anagram_sort ]
    algorithms=[is_anagram_checkoff, is_anagram_lettercount, is_anagram_sort, is_anagram_prime_hash]
    inputs=[("eat","ate"), ("tale", "late"), ("sneak", "snake"), ("actors", "costar"), ("allergy", "gallery"), ("calipers", "replicas"), ("cautioned", "education"), ("percussion", "supersonic"), ("calligraphy", "graphically"), ("SNOOZE ALARMS", "ALAS! NO MORE ZS :("), ("ASTRONOMERS", "No More Stars"), ("A DECIMAL POINT", "I'M A DOT IN PLACE"), ("conversationalists", "conservationalists"), ("hydroxydeoxycorticosterones", "hydroxydeoxycorticosteroids"), ("pseudopseudohypoparathyroidism", "pseudohypoparathyroidism"), ("THE UNITED STATES BUREAU OF FISHERIES", "I RAISE THE BASS TO FEED US IN THE FUTURE")]
    

    '''
    trials = 10
    experiment = TimingProfiler(algorithms, inputs, trials)
    experiment.run_experiments()
    print(experiment.results)
    experiment.graph(title="is_anagrams Timings", scale="linear")
    '''