import random
from colorama import Fore, Back, Style, init
from copy import deepcopy

class Pyramid:
    def __init__(self, camel_styles:dict[str, str]):
        '''Creates a pyramid of dice for the game Camel Up.'''
        self.STYLES = camel_styles
        self.DIE_VALUES = [1, 2, 3] #TODO
        self.DIE_COLORS = ["r", "b", "g", "y", "p"] #TODO
        self.remaining_dice = []

        self.reset_leg()

        ## YOUR CODE GOES HERE
        pass
    
    def shake(self): 
        '''Shakes the pyramid to remove a random color from the remaining dice.

            Return
                tuple[str, int] - A tuple representation of the rolled die
                                  If there are no dice remaining, return ("", 0)
        '''
        ## YOUR CODE GOES HERE

        if self.remaining_dice == []:
            return("", 0)

        chosen_random_die_color = random.choice(self.remaining_dice)

        self.remaining_dice.remove(chosen_random_die_color)

        chosen_random_die_value = random.randint(1,3)

        roll_result = (chosen_random_die_color, chosen_random_die_value)

        return(roll_result)
    
    def reset_leg(self):
        '''Ensures that all dice colors are returned to the pyramid
        '''
        
        self.remaining_dice = deepcopy(self.DIE_COLORS)

        pass

    def __str__(self):
        dice_str="Remaining dice: "
        for die in self.remaining_dice:
            dice_str+=self.STYLES[die[0]]+die[0]+Style.RESET_ALL+" "
        return dice_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    pyramid = Pyramid(STYLES)
    print(pyramid)
    num_rolls=3
    for _ in range(num_rolls):
        rolled_die = pyramid.shake()
        print(f"{rolled_die} was shaken from the pyramid")
    print(pyramid)
    