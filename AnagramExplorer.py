from itertools import combinations
from valid_anagame_words import get_valid_word_list

class AnagramExplorer:
    def __init__(self, valid_words: list[str]):
        """
        Initializes the AnagramExplorer with a list of valid words.

        Args:
            valid_words (list[str]): A list of valid words to use for anagram exploration.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones"])
        >>> explorer.corpus
        ['listen', 'silent', 'enlist', 'inlets', 'stone', 'tones']
        """
        self.__corpus = valid_words
        self.__lookup_dict = self.build_lookup_dict() #only calculated once, when the object is created

    @property
    def corpus(self):
        return self.__corpus

    @property
    def lookup_dict(self):
        return self.__lookup_dict
    
    def generate_hash(self, word: str) -> tuple[str]:
        """
        Generates a hash for the given word by sorting its letters and returning a tuple.

        Args:
            word (str): The word to generate a hash for.

        Returns:
            tuple[str]: A tuple representing the sorted letters of the word.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent"])
        >>> explorer.generate_hash("listen")
        ('e', 'i', 'l', 'n', 's', 't')
        """

        return tuple(sorted((letter for letter in word)))

    def build_lookup_dict(self) -> dict[str, set[str]]:
        """
        Builds a lookup dictionary where keys are sorted tuples of lowercase letters, 
        and values are sets of lowercase words from self.__corpus with the same letters.
        Facilitates quick retrieval of anagram families based on their sorted letter representation.

        Returns:
            dict: A dictionary mapping sorted letter tuples to sets of words.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "apple"])
        >>> lookup = explorer.build_lookup_dict()
        >>> lookup[('e', 'i', 'l', 'n', 's', 't')] ==  {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> ('s', 't', 'o', 'n', 'e') in lookup
        False
        >>> lookup[('a', 'e', 'l', 'p', 'p')] == {"apple"}
        True
        """

        lookup_dict = dict()

        for word in self.corpus:
            word_hash = self.generate_hash(word)
            if word_hash not in lookup_dict:
                lookup_dict[word_hash] = {word}
            else:
                lookup_dict[word_hash].add(word)
        
        return lookup_dict

    def is_valid_anagram_pair(self, pair: tuple[str, str], letters: list[str] = None) -> bool:
        """
        Valid anagram pairs must exist in the corpus. 
        If letters are provided, both words must match the letters in the list (without replacement).
        Words must be at least 3 characters long and not identical.

        Args:
            pair (tuple[str, str]): A tuple containing two words to check.
            letters (list[str]): A list of letters available for forming anagrams.

        Returns:
            bool: True if the pair forms a valid anagram, False otherwise.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "Ten", "net", "stent", "tents", "and"])
        >>> explorer.is_valid_anagram_pair(("listen", "silent"), ["l", "i", "s", "t", "e", "n"])
        True
        >>> explorer.is_valid_anagram_pair(("Ten", "net"), ["l", "i", "s", "t", "e", "n"])
        True
        >>> explorer.is_valid_anagram_pair(("stent", "tents"), ["l", "i", "s", "t", "e", "n"])
        False
        >>> explorer.is_valid_anagram_pair(("stent", "tents"))
        True
        >>> explorer.is_valid_anagram_pair(("stone", "tones"), ["s", "t", "o", "n", "e"])
        False
        >>> explorer.is_valid_anagram_pair(("apple", "pale"), ["a", "p", "p", "l", "e"])
        False
        """

        word1, word2 = pair

        cleaned_word1 = ""
        cleaned_word2 = ""  

        for letter in word1.lower():
            if letter in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
                cleaned_word1 = cleaned_word1 + letter
        for letter in word2.lower():
            if letter in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
                cleaned_word2 = cleaned_word2 + letter

        if len(cleaned_word1) != len(cleaned_word2) or len(cleaned_word1) < 3 or len(cleaned_word2) < 3 or (cleaned_word1 == cleaned_word2) or (cleaned_word1 not in [word.lower() for word in self.corpus]) or (cleaned_word2 not in [word.lower() for word in self.corpus]):
            return False

        if letters != None:
            for word in (cleaned_word1, cleaned_word2):
                remaining_letters = [letter for letter in letters]
                for letter in word:
                    if letter in remaining_letters:
                        remaining_letters.remove(letter)
                    else:
                        return False
            
        return sorted(cleaned_word1) == sorted(cleaned_word2)
           
    def get_all_anagrams(self, letters: list[str] = None) -> set[str]:
        """
        Finds all anagrams that can be formed using the given letters. If no letters are provided
        or if the letters list is empty, returns all words from the corpus that can form an anagram pair.

        Args:
            letters (list[str], optional): A list of letters to form anagrams. Defaults to None.

        Returns:
            set[str]: A set of all valid anagrams.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_all_anagrams(["l", "i", "s", "t", "e", "n"]) == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_all_anagrams() == {'listen', 'silent', 'enlist', 'inlets', 'stone', 'tones'}
        True
        >>> explorer.get_all_anagrams(["a", "p", "p", "l", "e"])
        set()
        """

        valid_anagrams = set()

        if not letters:
            for group in self.__lookup_dict.values():
                if len(group) >= 2:
                    valid_anagrams.update(group)

            return valid_anagrams
        

        for word_length in range(3, len(letters) + 1):
            for letter_combination in combinations(letters, word_length):
                sorted_letter_combination = tuple(sorted(letter_combination))
                if sorted_letter_combination in self.__lookup_dict:
                    potential_anagram = self.__lookup_dict[sorted_letter_combination] 
                    if len(potential_anagram) >= 2:
                        valid_anagrams.update(potential_anagram)
                
        return valid_anagrams

    def get_most_anagrams(self, letters: list[str] = None) -> set[str]:
        """
        Generates a set of words which form the largest number of anagram combinations within self.__corpus 
        The returned set contains all words for each anagram group that produces the maximum number of anagrams.
        If a list of letters is provided, the search is restricted to anagrams that can be formed from those letters.

        Args:
            letters (list[str], optional): A list of letters to form anagrams. Defaults to None.

        Returns:
            set[str]: A set of words that form the most anagrams.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_most_anagrams(["l", "i", "s", "t", "e", "n"]) == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_most_anagrams() == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_most_anagrams(["a", "p", "p", "l", "e"])
        set()
        """

        all_anagram_words = self.get_all_anagrams(letters)

        anagrams_groups = dict()

        for word in all_anagram_words:
            word_hash = self.generate_hash(word)
            if word_hash not in anagrams_groups:
                anagrams_groups[word_hash] = set()
            anagrams_groups[word_hash].add(word)                

        if anagrams_groups == dict():
            return set()
        
        biggest_anagram_group = - 10

        for word_group in anagrams_groups.values():
            if len(word_group) > biggest_anagram_group:
                biggest_anagram_group = len(word_group)

        most_anagrams = set()

        for word_group in anagrams_groups.values():
            if len(word_group) == biggest_anagram_group:
                most_anagrams.update(word_group)

        return most_anagrams


    def get_words_with_no_anagrams(self, letters: list[str] = None) -> set[str]:
        """
        Finds all words in the corpus that do not form any valid anagram pairs with any other word.
        If a list of letters is provided, words that cannot be constructed from those letters are not considered valid anagram pairs and are included in the returned set.

        Returns:
            set[str]: A set of words from the corpus that have no anagrams.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_words_with_no_anagrams() == {'unique'}
        True
        >>> explorer = AnagramExplorer(["rat", "tar", "art", "stop", "tops", "pots", "spot", "post"])
        >>> explorer.get_words_with_no_anagrams()
        set()
        >>> explorer = AnagramExplorer(["apple", "banana", "carrot"])
        >>> explorer.get_words_with_no_anagrams() == {'apple', 'banana', 'carrot'}
        True
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> letters = ["s", "i", "l", "e", "n", "t", "a"]
        >>> explorer.get_words_with_no_anagrams(letters) == {'stone', 'tones', 'unique'}
        True
        """

        return set(self.corpus) - self.get_all_anagrams(letters)

    

    def prime_hash(self, word: str) -> int:
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

            ch_to_prime = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
        'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43,
        'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79,
        'w': 83, 'x': 89, 'y': 97, 'z': 101 }

            hash = 1 

            for letter in word:
                hash = hash * ch_to_prime[letter]

            return hash



    


if __name__ == "__main__":
    print("Demonstrating AnagramExplorer functionality")

    simple_corpus = [
        "listen", "silent", "enlist", "inlets", "stone", "tones", "note", "tone", "rat", "tar", "art", 
        "stop", "pots", "tops", "opt", "spot", "post", "unique", "apple", "banana", "carrot"
    ]

    explorer = AnagramExplorer(simple_corpus)
    letters = ["l", "i", "s", "t", "e", "n"]

    print("\nGet all anagrams for a particular collection of letters:", letters)
    print("Anagrams:", explorer.get_all_anagrams(letters))

    print("\nGet all words from the corpus that can form an anagram pair:")
    print("Anagrams:", explorer.get_all_anagrams())

    print("\nFind the words that form the most anagrams for a particular collection of letters::", letters)
    print("Most anagrams:", explorer.get_most_anagrams(letters))

    print("\nFind the words that form the most anagrams in the entire corpus:")
    print("Most anagrams:", explorer.get_most_anagrams())

    word_pair = ("listen", "silent")
    print("\nCheck if two words form a valid anagram pair:", word_pair)
    print("Is valid anagram pair:", explorer.is_valid_anagram_pair(word_pair, letters))

    letters = ["p", "i", "s", "t", "e", "n"]
    print("\nWords with no anagrams in the corpus for a particular collection of letters:", letters)
    print(explorer.get_words_with_no_anagrams(letters))

    print("\nWords with no anagrams in the corpus:")
    print(explorer.get_words_with_no_anagrams())
