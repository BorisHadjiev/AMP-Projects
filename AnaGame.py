import time
import random
import string
import math

from valid_anagame_words import get_valid_word_list


try:
    from AnagramExplorer import AnagramExplorer
except ModuleNotFoundError:
    print("AnagramExplorer.py is not found.")
    pass

class AnaGame:
    def __init__(self, fun_factor:int, time_limit: int, corpus:list[str]):
        self.corpus = corpus
        self.explorer = AnagramExplorer(corpus)
        self.time_limit= time_limit
        self.letters= self.generate_letters(fun_factor, "SCRABBLE") #"UNIFORM", "SCRABBLE", "FREQUENCY"
        self.all_guesses= []
        self.guess_timestamps = []
        self.stats= {}
    
    def generate_letters(self, fun_factor: int, distribution: str):
        '''Generates a list of 7 randomly-chosen lowercase letters which can form at least 
            fun_factor unique anagramable words

            Args:
                fun_factor (int): minimum number of unique anagram words offered by the chosen letters
                distribution (str): The type of distribution to use in order to choose letters
                        "UNIFORM" - chooses letters based on a uniform distribution, with replacement
                        "SCRABBLE" - chooses letters based on a scrabble distribution, without replacement

            Returns:
                list: A list of 7 lowercase letters
        '''

        anagram_words = -10

        while anagram_words < fun_factor:
            letters = []
            match distribution:
                case "UNIFORM":
                    for i in range(7):
                        letters.append(random.choice(string.ascii_lowercase))
                    
                case "SCRABBLE":
                    scrabble_letters = [                    
                                        ["a" for a in range(9)] +
                                        ["b" for b in range(2)] +
                                        ["c" for b in range(2)] +
                                        ["d" for b in range(4)] +
                                        ["e" for b in range(12)]+
                                        ["f" for b in range(2)] +
                                        ["g" for b in range(3)] +
                                        ["h" for b in range(2)] +
                                        ["i" for b in range(9)] +
                                        ["j" for b in range(1)] +
                                        ["k" for b in range(1)] +
                                        ["l" for b in range(4)] +
                                        ["m" for b in range(2)] +
                                        ["n" for b in range(6)] +
                                        ["o" for b in range(8)] + 
                                        ["p" for b in range(2)] +
                                        ["q" for b in range(1)] +
                                        ["r" for b in range(6)] +
                                        ["s" for b in range(4)] +
                                        ["t" for b in range(6)] +
                                        ["u" for b in range(4)] +
                                        ["v" for b in range(2)] +
                                        ["w" for b in range(2)] +
                                        ["x" for b in range(1)] +
                                        ["y" for b in range(2)] +
                                        ["z" for b in range(1)] ]
                    
                    for i in range(7):
                        letters.append(scrabble_letters[0].pop(scrabble_letters[0].index(random.choice(scrabble_letters[0]))))
                    
            anagram_words = len(self.explorer.get_all_anagrams(letters))

        return letters

    def parse_guess(self, guess: str):
        '''Splits an entered guess into a two word tuple with all white space removed.
        
            Args:
                guess (str): A single string reprsenting the player guess

            Returns:
                tuple: A tuple of two words. ("", "") in case of invalid input.

            Examples
            --------
            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat, tea") == ("eat", "tea")
            True

            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat , tea") == ("eat", "tea")
            True

            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat,tea") == ("eat", "tea")
            True

            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat tea") == ("", "")
            True
        '''

        if guess.count(",") != 1:
            return ("", "")

        first_value, second_value = guess.split(",")

        first_word = ""
        second_word = ""
        
        for char in first_value:
            if char != " ":
                first_word += char

        for char in second_value:
            if char != " ":
                second_word += char

        return (first_word, second_word)


    def play_game(self):
        '''Plays a single game of AnaGame'''

        print("\nWelcome to AnaGame!\n")
        print("Please enter your anagram guesses separated by a comma: eat,tea")
        print("Enter 'quit' to end the game early, or 'hint' to get a useful word\n")
        print(f"You have {self.time_limit} seconds to guess as many anagrams as possible!")
        print(f"{self.letters}")

        guesses = [] 
        quit = False
        streak_commentary = ["You're on Fire!", "Too Hot to Touch!", "B-B-B-Bazinga!", "JACKPOT", "Ding Ding Ding!", "Home Run!", "Someone Call the Cops!", "The Crowd Goes Wild!", "You are an ANAGAME MACHINE"]

        streak = 0
        last_guess_timestamp = None

        start = time.perf_counter() #start the stopwatch (sec)
        stop = start + self.time_limit

        while time.perf_counter() < stop and not quit:
            guess = input('')
            if guess.strip().lower() == "quit":
                quit = True
            elif guess.strip().lower() == "hint":
                print(f"Try working with: {list(self.explorer.get_most_anagrams(self.letters))[0]}")
            else:
                tuple_guess = self.parse_guess(guess)
                if len(tuple_guess[0]) > 1:
                    

                    if last_guess_timestamp != None and time.perf_counter() - last_guess_timestamp <= 5:
                        streak += 1
                    else:
                        streak = 0
                    
                    if streak >= 1:
                        print(random.choice(streak_commentary))

                    self.all_guesses.append(tuple_guess)
                    self.guess_timestamps.append(time.perf_counter())
                    last_guess_timestamp = time.perf_counter()
                    
                else:
                    print("Invalid input")

            print(f"{self.letters} {round(stop - time.perf_counter(), 2)} seconds left")

    def update_stats(self):
        '''Aggregates several statistics into a single dictionary with the following key-value pairs:
            "valid_guesses" - list of valid guesses
            "invalid_guesses" - list of invalid/duplicate guesses
            "unique_guessed" - set of unique words guessed from valid guesses
            "not_guessed" - list of unique words not guessed, sorted by anagrammability/alphabetically
            "score" - per the rules of the game
            "accuracy" -  truncated int percentage representing valid player guesses out of all player guesses
                    3 valid and 5 invalid guesses would result in an accuracy of 37 --> 3/8 = .375
            "skill" - truncated int percentage representing the total number of unique anagram words guessed out of all possible unique anagram words
                Guessing 66 out of 99 unique words would result in a skill of 66 --> 66/99 = .66666666
            Args:
            guesses (list): A list of tuples representing all word pairs guesses by the user
            letters (list): The list of valid letters from which user should create anagrams
            explorer (AnagramExplorer): helper object used to compute anagrams of letters.

            Returns:
            dict: Returns a dictionary with seven keys: "valid", "invalid", "score", "accuracy", "guessed", "not guessed", "skill"
            
            Example
            -------
            >>> letters = ["p", "t", "s", "a", "r"]
            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.letters = letters
            >>> game.all_guesses = [("star","tarts"),("far","rat"),("rat","art"),("rat","art"),("art","rat"),("pots","stop")]
            >>> game.update_stats()
            >>> game.stats["valid_guesses"] == [("rat", "art")]
            True
            >>> game.stats["invalid_guesses"] == [("star", "tarts"), ("far", "rat"), ("rat", "art"), ("art", "rat"),("pots","stop")]
            True
            >>> game.stats["score"]
            1
            >>> game.stats["accuracy"]
            16
            >>> game.stats["unique_guessed"] == {"rat", "art"}
            True
            >>> game.stats["not_guessed"] == ['par', 'rap', 'asp', 'sap', 'spa', 'apt', 'pat', 'tap', 'tar', 'raps', 'rasp', 'spar', 'part', 'prat', 'rapt', 'trap', 'past', 'pats', 'spat', 'taps', 'arts', 'rats', 'star', 'tars', 'parts', 'sprat', 'strap', 'traps']
            True
            >>> game.stats["skill"]
            6
            '''
        self.stats["valid_guesses"] = [] #[(rat, tar)]
        self.stats["invalid_guesses"] = [] #[(rat, tax)]
        self.stats["unique_guessed"] = set() #unique valid guessed words
        self.stats["not_guessed"] = [] #list... sorted by anagrammability
        self.stats["score"] = 0    #total score per the rules of the game
        self.stats["accuracy"] = 0 #int percentage- valid player guesses/all player guesses
        self.stats["skill"] = 0    #int percentage- unique guessed words/all possible unique anagram words
        
        consumed_pairs = set()
        streak = 0
        last_valid_guess_time = None

        for index, guess in enumerate(self.all_guesses):
            word1, word2 = guess
            pair_key = tuple(sorted((word1, word2)))  

            if self.explorer.is_valid_anagram_pair(guess, self.letters) and pair_key not in consumed_pairs:
                self.stats["valid_guesses"].append(guess)
                consumed_pairs.add(pair_key)

                base_points = len(word1) - 2
                bonus = 0

                if index < len(self.guess_timestamps):
                        current_time = self.guess_timestamps[index]
                        if last_valid_guess_time != None and (current_time - last_valid_guess_time) <= 5:
                            streak += 1
                            bonus += streak
                        else:
                            streak = 0
                        last_valid_guess_time = current_time 
                self.stats["score"] += base_points + bonus
            else:
                self.stats["invalid_guesses"].append(guess)

                

        all_valid_guesses = []
        for word_pair in self.stats["valid_guesses"]:
            all_valid_guesses.extend(word_pair)

        self.stats["unique_guessed"] = set(all_valid_guesses)

        all_anagrams = self.explorer.get_all_anagrams(self.letters)

        self.stats["not_guessed"] = sorted(
                all_anagrams - self.stats["unique_guessed"],
                key=lambda w: (self.explorer.prime_hash(w), w)
            )

                                     
        if self.all_guesses:
            self.stats["accuracy"] = math.floor((len(self.stats["valid_guesses"]) / len(self.all_guesses)) * 100)

        if all_anagrams:
            self.stats["skill"] = math.floor((len(self.stats["unique_guessed"]) / len(all_anagrams)) * 100)
 
    def __str__(self):
        '''Returns a string representation of the game'''
        output = "------------\n"
        output+= f"Total Guesses: {len(self.all_guesses)}\n"
        for guess in self.all_guesses:
            output+=f"  {guess[0]},{guess[1]}"

        output += "\n------------\n"
        output+=f"Valid Guesses: {len(self.stats['valid_guesses'])}/{len(self.all_guesses)}\n"
        for guess in self.stats['valid_guesses']:
            output+=f"  {guess[0]},{guess[1]}"
        output+=f"\n\nInvalid Guesses: {len(self.stats['invalid_guesses'])}/{len(self.all_guesses)}\n"
        for guess in self.stats['invalid_guesses']:
            output+=f"  {guess[0]},{guess[1]}"

        output+="\n------------\n"
        output+=f"Unique Words Guessed: {len(self.stats['unique_guessed'])}\n"
        for guess in sorted(self.stats['unique_guessed']):
            output+=f"  {guess}"
        output+=f"\n\nWords you could have guessed: {len(self.stats['not_guessed'])}\n"
        for guess in self.stats['not_guessed']:
            output+=f"  {guess}"

        output+=f"\n------------\n"
        output+=f"Accuracy: {round(self.stats['accuracy'], 2)}%\n"
        output+=f"\nSkill: {self.stats['skill']}%\n"
        output+=f"\nScore: {self.stats['score']}\n"
        output+=f"------------\n"

        return output


if __name__ == "__main__":
    time_limit = 60
    fun_factor = 100
    game = AnaGame(fun_factor, time_limit, get_valid_word_list())
    game.play_game()
    game.update_stats()

    print("\nThanks for playing AnaGame!\n")
    print(game)
