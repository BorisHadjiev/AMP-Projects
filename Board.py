import random
from colorama import Fore, Back, Style, init
from copy import deepcopy

try:
    from Pyramid import Pyramid
except ModuleNotFoundError:
    print("Pyramid.py is not found.")
    pass

class Board:
    def __init__(self, STYLES: dict[str, str] ):
        self.TRACK_LENGTH = 16
        self.STYLES = STYLES
        self.track = [[] for i in range(self.TRACK_LENGTH)]
        self.pyramid = Pyramid(self.STYLES)
        self.ticket_tents = {
                            "r": [5, 3, 2, 2],
                            "g": [5, 3, 2, 2], 
                            "b": [5, 3, 2, 2], 
                            "y": [5, 3, 2, 2], 
                            "p": [5, 3, 2, 2]
                             }
        self.dice_tents = []
        self.place_camels()
        
    def place_camels(self):
        '''Places stacked camels in a random order on the first position of the track.
        '''

        camels = ["r", "g", "b", "y", "p"]
        random.shuffle(camels)
        self.track[0] = camels

    def move_camel(self, die: tuple[str, int]):
        '''Moves the camel of the given color forward by the given number of spaces.
            If the camel is on a tile with other camels, it moves with all camels
            on top of it. 
            
            If the camel reaches the end of the track, it ... TODO

            Args:
                die (tuple[str, int]): A tuple containing the color and value of the die.
                    The color is a string representing the camel's color.
                    The value is an integer representing the number of spaces to move.
        '''

        moving_camel_color, move_distance = die

        starting_position = None

        camel_height = None

        moving_camels = None

        if moving_camel_color == "" or move_distance == 0:
            return

        for camel_location, camels in enumerate(self.track):
            if moving_camel_color in camels:
                starting_position = camel_location 
                camel_height = camels.index(moving_camel_color)
                moving_camels = camels[camel_height:]
                break

        
        finishing_position = starting_position + move_distance
        
        if finishing_position >= 15:
            finishing_position = 15

        del self.track[starting_position][camel_height:]

        self.track[finishing_position].extend(moving_camels)

    def roll_die(self):
        '''Shakes the pyramid and places the rolled die on the next dice tent
            If the pyramid is empty, returns a die with color "" and value 0.

            Returns:
                tuple[str, int] - A tuple representation of the rolled die
        '''

        
        die = self.pyramid.shake()
        if die[0] != "":
            self.dice_tents.append(die)
        return die


    
    def take_ticket(self, color:str):
        '''Removes the top ticket available from the ticket tent of the given color.
           Tickets are removed from the tent in the order of their values, with the highest value ticket being removed first.

            If no tickets are available, returns a ticket with value of 0.
            
            Returns:
                tuple[str, int] - A tuple representation of the ticket
        '''

        if len(self.ticket_tents[color]) > 0 :
            ticket_value = self.ticket_tents[color].pop(0)
        else: 
            ticket_value = 0

        return (color, ticket_value)

    
    def is_leg_finished(self):
        ''' A leg is finished when all dice have been rolled. This is determined by checking dice tents
            as playing with crazy camels involves more than five dice.

            Returns:
                bool - True if all dice have been rolled, False otherwise   
        '''

        if len(self.pyramid.remaining_dice) == 0:
            return True
        else: 
            return False

    
    def get_rankings(self):
        '''Returns the first and second place camels as a tuple of strings.
       
            Return
                tuple[str, str] - A tuple containing the first and second place camels
        '''

        ranking = []
        for position in range(len(self.track), 0, -1):
            for camel in reversed(self.track[position - 1]):
                ranking.append(camel)
            if len(ranking) >= 2:
                break

        if len(ranking) < 2:
            return ("", "")

        return (ranking[0], ranking[1])

        
    def reset_leg(self):
        '''Resets the board for a new leg of the game.
            - Resets the pyramid
            - Resets the ticket tents
            - Empties the dice tents
            - Does not move camels
        '''
        ## YOUR CODE GOES HERE

        self.pyramid.reset_leg()

        self.ticket_tents = {"r": [5, 3, 2, 2], 
                             "g": [5, 3, 2, 2], 
                             "b": [5, 3, 2, 2], 
                             "y": [5, 3, 2, 2], 
                             "p": [5, 3, 2, 2]
                             }
        
        self.dice_tents = []
    
    def __str__(self):
        board_string = ""
         #Ticket Tents
        ticket_string = "Ticket Tents: "
        for ticket_color in self.ticket_tents:
            if len(self.ticket_tents[ticket_color]) > 0:
                next_ticket_value = str(self.ticket_tents[ticket_color][0])
            else:
                next_ticket_value = 'X'
            ticket_string+=self.STYLES[ticket_color]+next_ticket_value+Style.RESET_ALL+" "
        board_string += ticket_string +"\t\t"

        #Dice Tents
        dice_string = "Dice Tents: "
        for die in self.dice_tents:
            dice_string+=self.STYLES[die[0]]+str(die[1])+Style.RESET_ALL+" "
        for i in range (5-len(self.dice_tents)):
            dice_string+=Back.WHITE+" "+Style.RESET_ALL+" "
        
        #Camels and Race Track
        board_string += dice_string +"\n"
        for row in range(4, -1, -1):
            row_str = [" "]*16
            for i in range(len(self.track)):
                for camel_place, camel in enumerate(self.track[i]):
                    if camel_place == row:
                        row_str[i]=self.STYLES[camel]+ camel +  Style.RESET_ALL 
            board_string += "🌴 "+str("   ".join(row_str))+" |🏁\n"
        board_string += "   "+"".join([str(i)+"   " for i in range(1, 10)])
        board_string += "".join([str(i)+"  " for i in range(10, 17)])

        return board_string
        


if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    board = Board(STYLES)
    print(str(board)+"\n")

    num_rolls=2
    
    for _ in range(num_rolls):
        rolled_die=board.roll_die()
        board.move_camel(rolled_die)
        print(f"{rolled_die} was shaken from the pyramid")
    print(board.pyramid)
    ticket = board.take_ticket(rolled_die[0])
    print(f"Player took a {rolled_die[0]} ticket: {ticket}")
    print(board)
    
    first, second = board.get_rankings()    
    print(f"First place: {first}, Second place: {second}")
    print("\nResetting leg...")
    board.reset_leg()
    print(board)      