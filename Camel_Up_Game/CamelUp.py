from colorama import Fore, Back, Style, init
import copy
import random

try:
    from Board import Board
except ModuleNotFoundError:
    print("Board.py is not found.")
    pass
try:
    from Player import Player
except ModuleNotFoundError:
    print("Player.py is not found.")
    pass
try:
    from AI import AI
except ModuleNotFoundError:
    print("AI.py is not found.")
    pass

class CamelUp:
    def __init__(self, camel_styles:dict[str, str], player_list:list[Player]):
        self.STYLES = camel_styles
        self.board = Board(self.STYLES)
        self.ai = AI(self.board)
        self.players = player_list
        self.camels = ["r", "g", "b", "y", "p"]

    def get_player_move(self, player:Player):
        print(f"{player.name}-", end =" ")     
        choice = "not_an_option"
        while choice.lower() not in ["b", "r", "a"]:
            choice = input("(B)et or (R)oll or (A)dvice? ").lower()
        return choice
    
    def get_player_bet(self):
        available_tickets="Available bets: "
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value=tickets_left[0]
                available_tickets += f"({color})"+self.STYLES[color]+str(top_ticket_value)+Style.RESET_ALL+" "
            else:
                available_tickets += f"({color})"+self.STYLES[color]+"X"+Style.RESET_ALL+" "
        print(available_tickets)
        
        ticket_color = "not_an_option"
        while ticket_color.lower() not in self.STYLES.keys() or len(self.board.ticket_tents[ticket_color])<=0:
            ticket_color = input("Which betting ticket would you like to take?\n").lower()

        return (self.board.take_ticket(ticket_color))
    
    def play_leg(self):
        curr_player = 0
        ai_player = None
        ai_player_list = []
        while ai_player not in ["y", "n"]:
            ai_player = input("Would you like to play against an AI player? (y/n) ").lower()

        for i in range(len(self.players)):
            ai_player_list.append(False)

        if ai_player == "y":
            ai_player_list[random.randint(0,1)] = True
        #randomly sets the AI player to go first or second
        
        while not self.board.is_leg_finished():
            player = self.players[curr_player]
                
            if ai_player_list[curr_player]:
                print("AI ponders... ")
                move, best_camel = self.ai_move()
                match move:
                    case "r":
                        self.board.move_camel(self.board.roll_die())
                        player.update_money(1)
                    case "b":
                        ticket = self.board.take_ticket(best_camel)
                        player.add_bet(ticket)
            else:
                move = 'x'
                while move not in ['r', 'b']:
                    move = self.get_player_move(player)
                    match move:
                        case "r":
                            self.board.move_camel(self.board.roll_die())
                            player.update_money(1)
                        case "b":
                            player.add_bet(self.get_player_bet())
                        case "a":
                            print(self.ai)

            print(self)
            curr_player = (curr_player + 1) % 2

    def ai_move(self):
        # I took a lot of prewritten code from the AI file

        enum, placeholder = self.ai.run_analysis(1)
        # only one trial since I am only taking the data from the enumerative analysis

        best_ev = -10
        best_camel = None
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value = tickets_left[0]
                ev = self.ai.get_ticket_EV(top_ticket_value, enum[color][0], enum[color][1])
                if ev > best_ev:
                    best_ev = ev
                    best_camel = color

        if best_ev > 1.1 and best_camel is not None:
            return ("b", best_camel)
        else:
            return ("r", None)


    def process_leg_payouts(self):
        """Process the payouts for the end of a leg, which includes determing first and second place camels
        and updating player money based on their bets. First place gets the value of their ticket, second place
        gets $1, and all other bets lose $1.

        Returns:
            tuple: a tuple of the form (first:str, second:str) 
            where first is the color (letter) of the winning camel and second is the color (letter) of the second place camel
            ex. ("b","y")
        """

        first_place, second_place = self.board.get_rankings()

        for player in self.players:
            for bet_color, ticket_value in player.bets:
                if bet_color == first_place:
                    player.update_money(ticket_value)
                    continue
                if bet_color == second_place:
                    player.update_money(1)
                    continue
                else:
                    player.update_money(-1)
        return first_place, second_place


    def __str__(self):
        game_str = str(self.board)
        for player in self.players:
            game_str += "\n" + str(player)
        return game_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    player1 = Player("Dave", STYLES)
    player2 = Player("Sasha", STYLES)
    game = CamelUp(STYLES, [player1, player2])
    print(game)
    game.play_leg()
    first, second = game.process_leg_payouts()

    print(f"{game.STYLES[first]}{first}{Style.RESET_ALL} comes in 1st🥇🥇🥇!")
    print(f"{game.STYLES[second]}{second}{Style.RESET_ALL} comes in 2nd🥈🥈🥈!")

    for player in game.players:
        print(f"{player.name} ended the leg with {player.money} coins.")

    if player1.money == player2.money:
        print("The first leg is a tie!")
    else:
        winner = player1 if player1.money > player2.money else player2
        print(f"{winner.name} wins the first leg!")