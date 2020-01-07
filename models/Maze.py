import math
import random as rd

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from .Constants import *
from .Robot import Robot


class Maze():
    """Représentation d'un labyrinthe
    """
    def __init__(self, showSolution: bool):
        self.mazeSize = []
        self.maze = [] # 2D array
        self.__showSolution = showSolution
        self.InitializeMazeFromC()
        self.__img = Image.new('RGB', (BITMAP_WIDTH, BITMAP_HEIGHT), "white") # Create a default white image
        self.__robot = Robot(self.GetStartCell())
        self.Robot.Path = np.zeros((self.maze.shape[0], self.maze.shape[1]), dtype=int)
        self.startPos = self.GetCurrentRobotCell()
        self.Robot.Path[self.startPos[1], self.startPos[0]] = self.Robot.CurrentStep

        self.x = 0
        self.y = 0
        
    #region Getter / Setter
    @property
    def Img(self):
        return self.__img

    @Img.setter
    def Img(self, value):
        self.__img = value

    @property
    def Robot(self):
        return self.__robot

    @Robot.setter
    def Robot(self, value):
        self.__robot = value

    @property
    def ShowSolution(self):
        return self.__showSolution

    @ShowSolution.setter
    def ShowSolution(self, value: bool):
        self.__showSolution = value

    #endregion Getter / Setter

    def GetImage(self):
        """Récupère l'image du labyrinthe
        """
        self.__img = Image.new('RGB', (BITMAP_WIDTH, BITMAP_HEIGHT), "white") # Create a default white image
        self.CreateGrid(self.maze.shape[0], self.maze.shape[1])
        self.GenerateMaze(self.maze)

        return self.__img

    def GetStartCell(self) -> int:
        """Récupère la valeur de la cellule de départ du robot

        Returns:
            La valeur de la cellule si succes, sinon 0x000

        """
        for row in range(0, self.maze.shape[1]):
            for col in range(0, self.maze.shape[0]):
                if 0 < (self.maze[row, col] & C_START):
                    return self.maze[row, col]
        return 0x0000

    def InitializeMazeFromC(self):
        """Intilialise le labyrinthe depuis un tableau de chiffres héxadécimaux

        See:
            https://github.com/micromouseonline/micromouse_maze_tool/tree/master/mazefiles/cfiles
        """
        """
        world_maz = np.array([
            0x0E, 0x0A, 0x08, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x09,
            0x0C, 0x0A, 0x02, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x09, 0x05,
            0x05, 0x0C, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x08, 0x0A, 0x09, 0x05, 0x05,
            0x05, 0x05, 0x0D, 0x0C, 0x0A, 0x09, 0x0E, 0x09, 0x0C, 0x0A, 0x09, 0x05, 0x0C, 0x01, 0x05, 0x05,
            0x05, 0x05, 0x04, 0x01, 0x0E, 0x02, 0x09, 0x04, 0x03, 0x0E, 0x00, 0x01, 0x05, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x05, 0x06, 0x0B, 0x0E, 0x02, 0x02, 0x0A, 0x0B, 0x07, 0x06, 0x03, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x05, 0x0C, 0x08, 0x0B, 0x0C, 0x08, 0x0A, 0x09, 0x0C, 0x09, 0x0C, 0x01, 0x05, 0x05,
            0x05, 0x05, 0x05, 0x05, 0x06, 0x09, 0x05, 0x04, 0x09, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x05, 0x04, 0x09, 0x06, 0x01, 0x06, 0x03, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x05, 0x07, 0x06, 0x09, 0x06, 0x0A, 0x0A, 0x03, 0x05, 0x06, 0x03, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x04, 0x0A, 0x0A, 0x03, 0x0E, 0x08, 0x0A, 0x0A, 0x02, 0x0A, 0x0B, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x06, 0x09, 0x0D, 0x0E, 0x08, 0x02, 0x0A, 0x0A, 0x0A, 0x0A, 0x09, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x0C, 0x03, 0x05, 0x0C, 0x03, 0x0C, 0x0A, 0x0A, 0x0A, 0x0A, 0x03, 0x05, 0x05, 0x05,
            0x05, 0x05, 0x06, 0x09, 0x04, 0x03, 0x0C, 0x03, 0x0C, 0x09, 0x0C, 0x0A, 0x09, 0x05, 0x05, 0x05,
            0x05, 0x06, 0x0A, 0x02, 0x03, 0x0E, 0x02, 0x0A, 0x03, 0x06, 0x03, 0x0E, 0x01, 0x05, 0x05, 0x05,
            0x06, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x02, 0x02, 0x02, 0x03,
        ])
        """
        world_maz = np.array([
            0x0E, 0x0A, 0x0A, 0x0A, 0x08, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x08, 0x0A, 0x0A, 0x0B,
            0x0E, 0x08, 0x08, 0x0A, 0x02, 0x0A, 0x0A, 0x08, 0x08, 0x0A, 0x0A, 0x0A, 0x02, 0x08, 0x08, 0x0B,
            0x0C, 0x03, 0x06, 0x0A, 0x0B, 0x0C, 0x0A, 0x01, 0x04, 0x0A, 0x09, 0x0E, 0x0A, 0x03, 0x06, 0x09,
            0x06, 0x09, 0x0C, 0x08, 0x08, 0x00, 0x0A, 0x00, 0x00, 0x0A, 0x00, 0x08, 0x08, 0x09, 0x0C, 0x03,
            0x0C, 0x03, 0x05, 0x05, 0x05, 0x06, 0x0A, 0x01, 0x04, 0x0A, 0x03, 0x05, 0x05, 0x05, 0x06, 0x09,
            0x06, 0x09, 0x05, 0x05, 0x06, 0x0A, 0x0B, 0x06, 0x03, 0x0E, 0x0A, 0x03, 0x05, 0x05, 0x0C, 0x03,
            0x0C, 0x02, 0x02, 0x02, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x02, 0x02, 0x02, 0x09,
            0x04, 0x0A, 0x0A, 0x08, 0x0A, 0x0A, 0x0B, 0x0C, 0x09, 0x0D, 0x0D, 0x0D, 0x0D, 0x0D, 0x0D, 0x05,
            0x05, 0x0D, 0x0D, 0x04, 0x0A, 0x0A, 0x0B, 0x04, 0x03, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
            0x04, 0x00, 0x00, 0x00, 0x0A, 0x0A, 0x0B, 0x05, 0x0D, 0x05, 0x07, 0x07, 0x07, 0x07, 0x07, 0x05,
            0x05, 0x05, 0x05, 0x04, 0x0A, 0x0A, 0x0B, 0x05, 0x05, 0x06, 0x0A, 0x0A, 0x0A, 0x08, 0x0B, 0x05,
            0x05, 0x06, 0x00, 0x03, 0x0C, 0x0A, 0x0A, 0x02, 0x01, 0x0E, 0x0A, 0x09, 0x0E, 0x00, 0x0B, 0x05,
            0x05, 0x0E, 0x00, 0x0B, 0x06, 0x0A, 0x0A, 0x09, 0x06, 0x09, 0x0E, 0x01, 0x0E, 0x00, 0x0B, 0x05,
            0x05, 0x0E, 0x00, 0x0B, 0x0C, 0x0A, 0x0A, 0x03, 0x0D, 0x06, 0x09, 0x05, 0x0E, 0x00, 0x0B, 0x05,
            0x05, 0x0E, 0x00, 0x0B, 0x06, 0x0A, 0x0A, 0x09, 0x05, 0x0D, 0x06, 0x01, 0x0E, 0x00, 0x0B, 0x05,
            0x07, 0x0E, 0x02, 0x0A, 0x0A, 0x0A, 0x0A, 0x02, 0x02, 0x02, 0x0A, 0x02, 0x0A, 0x02, 0x0B, 0x07,
        ])

        world_maz[0] |= (C_START | C_ROBOT_N | C_PATH)
        world_maz[119] |= C_GOAL
        world_maz[120] |= C_GOAL
        world_maz[135] |= C_GOAL
        world_maz[136] |= C_GOAL

        if (self.ShowSolution):
            world_maz[0] &= (~(C_ROBOT_N | C_PATH))
        
        self.mazeSize = [(int)(math.sqrt(world_maz.__len__())), (int)(math.sqrt(world_maz.__len__()))]
        self.maze = self.ToArray2D(world_maz, self.mazeSize)

    def ToArray2D(self, anArray: [], newArraySize: []):
        """Transforme un tableau à 1 dimension en 2 dimension
        """
        clone = np.arange(anArray.__len__()).reshape(-1, newArraySize[0])
        
        for i in range(0, anArray.__len__()):
            clone[newArraySize[1] - (i % newArraySize[1]) - 1, int(i / newArraySize[0])] = int(anArray[i])

        return clone

    def GetCurrentRobotCell(self) -> []:
        """Récupère les coordonées de la cellule où le robot se trouve

        Returns:
            Les coordonées de la cellules si succes, sinon [-1, -1]

        """
        for row in range(0, self.maze.shape[1]):
            for col in range(0, self.maze.shape[0]):
                if self.maze[row, col] == self.Robot.CurrentCell:
                    return np.array([col, row])
        return np.array([-1, -1])

    def CreateGrid(self, cols: int = DEFAULT_MAZE_WIDTH, rows: int = DEFAULT_MAZE_HEIGHT):
        """Créer la grille de départ
        """
        size = [int((self.Img.width - 40) / cols), int((self.Img.height - 40) / rows)]
        pos = []
        font = ImageFont.truetype("arial", 10)
        bitmap = ImageDraw.Draw(self.Img) # Direct modification on self.Img

        for row in range(0, rows):
            bitmap.text((2, int(row * size[1] + 35)), str(row), (0, 0, 0), font=font)
            for col in range(0, cols):
                if row == 0: # Draw only 1 time
                    bitmap.text((int(col * size[0] + 35), 2), str(col), (0, 0, 0), font=font)
                pos = [int(col * size[0] + 20), int(row * size[1] + 20)]
                bitmap.rectangle(((pos[0], pos[1]), (pos[0] + size[0], pos[1] + size[1])), outline="black")

    def GenerateMaze(self, maze):
        """Génère le labyrinthe en fonction des valeures du tableau à 2 dimensions donné
        """
        size = [int((self.Img.width - 40) / maze.shape[0]), int((self.Img.height - 40) / maze.shape[1])]
        bitmap = ImageDraw.Draw(self.Img) # Direct modification on self.Img
        font = ImageFont.truetype("arial", 12)

        robot_up = Image.open("./img/up.png").resize((tuple)(size))
        robot_right = Image.open("./img/right.png").resize((tuple)(size))
        robot_down = Image.open("./img/down.png").resize((tuple)(size))
        robot_left = Image.open("./img/left.png").resize((tuple)(size))
        rock = Image.open("./img/rock.png").resize((tuple)(size))
        walked_grass = Image.open("./img/walked_grass.png").resize((tuple)(size))

        for row in range(0, maze.shape[1]):
            for col in range(0, maze.shape[0]):
                posX = int(col * size[0] + 20)
                posY = int(row * size[1] + 20)

                if (self.ShowSolution or self.Robot.Path[row, col] > 0):
                    # Le dernier argument est la couleur sous forme de tuples (r, g, b [, a])
                    # START - GOAL - VISITED - DONE
                    if ((maze[row, col] & C_START) > 0):
                        bitmap.rectangle(((posX, posY), (posX + size[0], posY + size[1])), GREEN)

                    if ((maze[row, col] & C_GOAL) > 0):
                        bitmap.rectangle(((posX, posY), (posX + size[0], posY + size[1])), ORANGE)

                    if ((maze[row, col] & C_PATH) > 0):
                        self.Img.paste(walked_grass, (posX, posY), walked_grass) # bitmap.rectangle(((posX, posY), (posX + size[0], posY + size[1])), YELLOW)

                    if ((maze[row, col] & C_VISITED) > 0):
                        self.Img.paste(rock, (posX, posY), rock) # bitmap.rectangle(((posX, posY), (posX + size[0], posY + size[1])), BLUE)

                    # *******************

                    # ROBOT FACES
                    if ((maze[row, col] & C_ROBOT_N) > 0):
                        self.Img.paste(robot_up, (posX, posY), robot_up) # Syntaxe pour pouvoir coller une image avec fond transparent

                    if ((maze[row, col] & C_ROBOT_E) > 0):
                        self.Img.paste(robot_right, (posX, posY), robot_right)

                    if ((maze[row, col] & C_ROBOT_S) > 0):
                        self.Img.paste(robot_down, (posX, posY), robot_down)

                    if ((maze[row, col] & C_ROBOT_W) > 0):
                        self.Img.paste(robot_left, (posX, posY), robot_left)

                    # *******************

                    # WALLS
                    if ((maze[row, col] & C_N) > 0):
                        bitmap.rectangle(((posX, posY), (posX + size[0], posY + 2)), BLACK)

                    if ((maze[row, col] & C_E) > 0):
                        bitmap.rectangle(((posX + size[0], posY), (posX + size[0] + 2, posY + size[1])), BLACK)

                    if ((maze[row, col] & C_S) > 0):
                        bitmap.rectangle(((posX, posY + size[1]), (posX + size[0], posY + size[1] + 2)), BLACK)
                    
                    if ((maze[row, col] & C_W) > 0):
                        bitmap.rectangle(((posX, posY), (posX + 2, posY + size[1])), BLACK)

                # Affichage du numéro de pas pour chaque case
                if (not self.ShowSolution):
                    if ((maze[row, col] & C_VISITED) == 0):
                        x = int(posX + size[0] / 4 - (str(self.Robot.CurrentStep).__len__() - 1) * 3)
                        y = int(posY + (size[1] / 2) - 10)
                        
                        color = BLACK if self.Robot.Path[row, col] == 0 else WHITE

                        if (maze[row, col] == self.Robot.CurrentCell):
                            bitmap.text((x, y), str(self.Robot.CurrentStep), font=font, fill=color)
                        else:
                            bitmap.text((x, y), str(self.Robot.Path[row, col]), font=font, fill=color)

    def MoveRobotNorth(self):
        """Fait bouger le robot au Nord
        """
        self.maze[self.y, self.x] &= (~(C_ROBOT_N | C_ROBOT_E | C_ROBOT_S | C_ROBOT_W))
        self.maze[self.y - 1, self.x] |= C_ROBOT_N

        if ((self.maze[self.y - 1, self.x]) & C_PATH) == 0 and (self.maze[self.y - 1, self.x] & C_VISITED) == 0:
            self.maze[self.y -1, self.x] |= C_PATH
        
        self.Robot.CurrentCell = self.maze[self.y - 1, self.x]

    def MoveRobotEast(self):
        """Fait bouger le robot à l'Est
        """
        self.maze[self.y, self.x] &= (~(C_ROBOT_N | C_ROBOT_E | C_ROBOT_S | C_ROBOT_W))
        self.maze[self.y, self.x + 1] |= C_ROBOT_E

        if ((self.maze[self.y, self.x + 1]) & C_PATH) == 0 and (self.maze[self.y, self.x + 1] & C_VISITED) == 0:
            self.maze[self.y, self.x + 1] |= C_PATH
        
        self.Robot.CurrentCell = self.maze[self.y, self.x + 1]

    def MoveRobotSouth(self):
        """Fait bouger le robot au Sud
        """
        self.maze[self.y, self.x] &= (~(C_ROBOT_N | C_ROBOT_E | C_ROBOT_S | C_ROBOT_W))
        self.maze[self.y + 1, self.x] |= C_ROBOT_S

        if ((self.maze[self.y + 1, self.x]) & C_PATH) == 0 and (self.maze[self.y + 1, self.x] & C_VISITED) == 0:
            self.maze[self.y + 1, self.x] |= C_PATH
        
        self.Robot.CurrentCell = self.maze[self.y + 1, self.x]
        
    def MoveRobotWest(self):
        """Fait bouger le robot à l'Ouest
        """
        self.maze[self.y, self.x] &= (~(C_ROBOT_N | C_ROBOT_E | C_ROBOT_S | C_ROBOT_W))
        self.maze[self.y, self.x - 1] |= C_ROBOT_W

        if ((self.maze[self.y, self.x - 1]) & C_PATH) == 0 and (self.maze[self.y, self.x - 1] & C_VISITED) == 0:
            self.maze[self.y, self.x - 1] |= C_PATH
        
        self.Robot.CurrentCell = self.maze[self.y, self.x - 1]    

    def TurnRight(self):
        """Fait tourner le robot à gauche
        """
        facingDirection = self.Robot.GetFacingDirection()

        self.maze[self.y, self.x] &= (~(C_ROBOT_N | C_ROBOT_E | C_ROBOT_S | C_ROBOT_W))

        if (facingDirection == C_ROBOT_N):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_E
        if (facingDirection == C_ROBOT_E):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_S
        if (facingDirection == C_ROBOT_S):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_W
        if (facingDirection == C_ROBOT_W):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_N

        self.Robot.CurrentCell = self.maze[self.y, self.x]

    def TurnLeft(self):
        """Fait tourner le robot à droite
        """
        facingDirection = self.Robot.GetFacingDirection()

        self.maze[self.y, self.x] &= (~(C_ROBOT_N | C_ROBOT_E | C_ROBOT_S | C_ROBOT_W))

        if (facingDirection == C_ROBOT_N):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_W
        if (facingDirection == C_ROBOT_E):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_N
        if (facingDirection == C_ROBOT_S):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_E
        if (facingDirection == C_ROBOT_W):
            self.maze[self.y, self.x] = self.maze[self.y, self.x] | C_ROBOT_S

        self.Robot.CurrentCell = self.maze[self.y, self.x]

    def GoForward(self):
        """Fait avancé le robot devant lui
        """
        self.Robot.CurrentStep += 1

        facingDirection = self.Robot.GetFacingDirection()

        if (facingDirection == C_ROBOT_N):
            self.MoveRobotNorth()
        if (facingDirection == C_ROBOT_E):
            self.MoveRobotEast()
        if (facingDirection == C_ROBOT_S):
            self.MoveRobotSouth()
        if (facingDirection == C_ROBOT_W):
            self.MoveRobotWest()

        self.x = self.GetCurrentRobotCell()[0]
        self.y = self.GetCurrentRobotCell()[1]

        self.Robot.Path[self.y, self.x] = self.Robot.CurrentStep

    def GoBack(self):
        """Fait revenir le robot sur ses pas
        """
        self.maze[self.y, self.x] &= (~(C_ROBOT_N | C_ROBOT_E | C_ROBOT_S | C_ROBOT_W))

        self.Robot.RemoveLastPos()

        newX = self.Robot.CurrentPath[-1].Coord[0]
        newY = self.Robot.CurrentPath[-1].Coord[1]
        self.maze[self.y, self.x] |= C_VISITED
        self.maze[newY, newX] |= self.Robot.CurrentPath[-1].Direction
        self.Robot.CurrentCell = self.maze[newY, newX]

        self.x = newX
        self.y = newY
        self.Robot.CurrentStep -= 1

    def IsThereAPossibleExit(self) -> bool:
        """Y a-t-il une sortie possible sur la cellule où le robot se trouve

        Returns:
            True si succes, sinon False

        """
        self.x = self.GetCurrentRobotCell()[0];
        self.y = self.GetCurrentRobotCell()[1];

        if ((self.Robot.CanGoNorth() and self.y - 1 >= 0 and (self.maze[self.y - 1, self.x] & C_PATH) == 0) or
            (self.Robot.CanGoEast() and self.x + 1 <= 15 and (self.maze[self.y, self.x + 1] & C_PATH) == 0) or
            (self.Robot.CanGoSouth() and self.y + 1 <= 15 and (self.maze[self.y + 1, self.x] & C_PATH) == 0) or
            (self.Robot.CanGoWest() and self.x - 1 >= 0 and (self.maze[self.y, self.x - 1] & C_PATH) == 0)):
            return True;

        return False;

    def NewGuess(self):
        """Fait un nouvel essaie
        """
        if (not self.Robot.IsOnGoal()):
            exitCount = 0

            self.x = self.GetCurrentRobotCell()[0]
            self.y = self.GetCurrentRobotCell()[1]

            if (self.Robot.CanGoNorth()):
                exitCount += 1
            if (self.Robot.CanGoEast()):
                exitCount += 1
            if (self.Robot.CanGoSouth()):
                exitCount += 1
            if (self.Robot.CanGoWest()):
                exitCount += 1

            if (self.Robot.CanGoLeft() and self.Robot.GetLeftPathCell(self.x, self.y) == 0):
                self.TurnLeft()
            if (self.Robot.CanGoRight() and self.Robot.GetRightPathCell(self.x, self.y) == 0):
                self.TurnRight()

            if (self.Robot.CanGoForward()):
                if (self.Robot.GetFacingPathCell(self.x, self.y) == 0):
                    self.GoForward()
                    self.Robot.AddCellToCurrentPath(self.x, self.y, exitCount, self.Robot.GetFacingDirection())
                else:
                    if (self.Robot.CanGoLeft() and self.Robot.GetLeftPathCell(self.x, self.y) == 0):
                        self.TurnLeft()
                    elif (self.Robot.CanGoRight() and self.Robot.GetRightPathCell(self.x, self.y) == 0):
                        self.TurnRight()
                    else:
                        self.Robot.NeedToFindAnExit = True
            else:
                self.Robot.NeedToFindAnExit = True

            if (self.Robot.NeedToFindAnExit):
                self.GoBack()

                # Si il y a une sortie possible sur la cellule où le robot se trouve
                if (self.IsThereAPossibleExit()):
                    self.Robot.NeedToFindAnExit = False
