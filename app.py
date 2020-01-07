import sys
import time

import pygame
from PIL import ImageQt

from models.Maze import Maze
from models.Constants import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK

# Création de la fenêtre
pygame.init()
pygame.display.set_caption("Micromouse Maze")
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.fill(WHITE)

# Création des deux instances de labyrinthe
maze     = Maze(False)
solution = Maze(True)

# Variables
clock                  = pygame.time.Clock()
counter         : int  = 0
solve           : bool = False
done            : bool = False
solutionDrawDone: bool = False
robotFoundGoal  : bool = False
FRAME_RATE      : int  = 16
UPDATE_FREQUENCY: int  = 10

def text_objects(text: str, font: object):
    """Créer les objects textuels nécessaire à l'affichage du text
    """
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def message_display(text: str):
    """Écrit un message à l'écran
    """
    largeText = pygame.font.Font(pygame.font.match_font("arial"), 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    display.blit(TextSurf, TextRect)

# Boucle principale
while not done:
    # Prise en charges des évèmenents
    for event in pygame.event.get():
        # Croix pour quitter
        if event.type == pygame.QUIT:
            done = True

        # Évènements claviers
        if event.type == pygame.KEYDOWN:
            if pygame.K_SPACE:
                solve = not solve

    if (solve and counter % UPDATE_FREQUENCY):
        maze.NewGuess()

    # Robot
    if (not robotFoundGoal):
        image = maze.GetImage()
        source = image.tobytes()
        display.blit(pygame.image.fromstring(source, (image.width, image.height), "RGB"), (10, 10))

    # Solution
    if (not solutionDrawDone):
        image = solution.GetImage()
        source = image.tobytes()
        display.blit(pygame.image.fromstring(source, (image.width, image.height), "RGB"), (880, 10))

    pygame.display.update()

    if (maze.Robot.IsOnGoal()):
        robotFoundGoal = True
        message_display(str(maze.Robot.CurrentStep))

    # Mise à jour directement pour ne pas redessiner la solution
    solutionDrawDone = True

    counter += 1
    clock.tick(FRAME_RATE)
