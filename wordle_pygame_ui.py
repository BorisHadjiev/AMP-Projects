import sys, os, pygame

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from WordleAI import WordleAI
from Wordle import Wordle

SIZE, GAP, TOP = 60, 8, 80
COLORS = {"-": (58, 58, 60), "y": (181, 159, 59), "Y": (83, 141, 78)}
BG, BORDER, TEXT = (18, 18, 19), (90, 90, 90), (255, 255, 255)

game = Wordle(WordleAI)
guess, msg, over = "", "", False

pygame.init()
screen = pygame.display.set_mode((SIZE * 5 + GAP * 6, TOP + SIZE * 6 + GAP * 7))
font = pygame.font.SysFont("arial", 30, bold=True)
clock = pygame.time.Clock()

def color(ch):
    return COLORS["-"] if ch == "-" else COLORS["Y"] if ch.isupper() else COLORS["y"]

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.KEYDOWN and not over:
            if e.key == pygame.K_BACKSPACE:
                guess = guess[:-1]
            elif e.key == pygame.K_RETURN and len(guess) == 5:
                if guess.lower() not in game.valid_word_list and guess.lower() not in game.valid_secret_word:
                    msg = "Not in word list"
                else:
                    fb = game.wordleai.get_feedback(guess.lower(), game.secret_word)
                    game.guesses.append(guess.lower())
                    game.feedback_history.append(fb)
                    over = guess.lower() == game.secret_word.lower() or len(game.guesses) == 6
                    msg = f"Word was {game.secret_word.upper()}" if over else ""
                    guess = ""
            elif e.unicode.isalpha() and len(guess) < 5:
                guess += e.unicode

    screen.fill(BG)
    if msg:
        screen.blit(font.render(msg, True, TEXT), (20, 25))

    for row in range(6):
        word = game.guesses[row] if row < len(game.guesses) else guess if row == len(game.guesses) else ""
        fb = game.feedback_history[row] if row < len(game.feedback_history) else ""
        for col in range(5):
            rect = pygame.Rect(GAP + col * (SIZE + GAP), TOP + row * (SIZE + GAP), SIZE, SIZE)
            pygame.draw.rect(screen, color(fb[col]) if fb else BG, rect)
            pygame.draw.rect(screen, BORDER, rect, 2)
            if col < len(word):
                screen.blit(font.render(word[col].upper(), True, TEXT), rect.move(22, 15))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()