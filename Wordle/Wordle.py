import random
from colorama import Fore, Back, Style, init
init(autoreset=True) #Ends color formatting after each print statement
import sys
import os
import string

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

try:
    from WordleAI import WordleAI as WordleAI
except ModuleNotFoundError:
    print("WordleAI.py is not found.")
    
from wordle_secret_words import get_secret_words
from valid_wordle_guesses import get_valid_wordle_guesses

class Wordle:
    

    def __init__(self, WordleAI):

        self.valid_word_list = [w.lower() for w in get_valid_wordle_guesses()]
        self.valid_secret_word = [w.lower() for w in get_secret_words()]

        
        self.guesses = []
        self.feedback_history = []
        self.feedback_string = ""
        self.wordleai = WordleAI(self.valid_word_list, self.valid_secret_word)

        self.secret_word = random.choice(self.valid_secret_word)
        self.max_guesses = 6

    def print_feedback(self):

        newest_word_feedback = self.feedback_history[-1]

        self.feedback_string += "\n"

        for index, letter in enumerate(newest_word_feedback):
            if letter == "-":
                self.feedback_string += Style.BRIGHT + Back.WHITE +  f"{self.guesses[-1][index].upper()}"
            if letter in list(string.ascii_lowercase):
                self.feedback_string += Style.BRIGHT + Back.LIGHTYELLOW_EX + f"{self.guesses[-1][index].upper()}"
            if letter in list(string.ascii_uppercase):
                self.feedback_string += Style.BRIGHT + Back.LIGHTGREEN_EX + f"{self.guesses[-1][index].upper()}"

            self.feedback_string += Style.RESET_ALL

        print(self.feedback_string)

    def play_game(self):
        print("Welcome to " + Style.BRIGHT + Back.GREEN + "Wo" + Style.BRIGHT + Back.YELLOW + "r" + Style.BRIGHT + Back.GREEN + "d" + Back.WHITE +"l" + Back.YELLOW + "e!")

        for turn in range(self.max_guesses + 1):
            guess = input(f"").lower()

            feedback = self.wordleai.get_feedback(guess, self.secret_word)

            self.guesses.append(guess)
            self.feedback_history.append(feedback)

            self.print_feedback()

            if guess == self.secret_word:
                break

        print(f"The word was {self.secret_word}")
        
if __name__ == "__main__":

    game = Wordle(WordleAI)
    game.play_game()
    
    


    