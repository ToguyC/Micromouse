from typing import List  # Automaticaly installed with python 3.8 at least

from .Cell import Cell
from .Constants import *


class Robot():
    """Représentation d'un robot
    """

    def __init__(self, startCell: int):
        """Constructeur
        """
        self.__currentCell = startCell
        self.__needToFindAnExit = False
        self.__path = [] # 2D array
        self.__currentStep = 1
        self.__currenPath = []

    #region Getter / Setter
    @property
    def CurrentCell(self):
        return self.__currentCell

    @CurrentCell.setter
    def CurrentCell(self, value):
        self.__currentCell = value

    @property
    def NeedToFindAnExit(self):
        return self.__needToFindAnExit

    @NeedToFindAnExit.setter
    def NeedToFindAnExit(self, value):
        self.__needToFindAnExit = value

    @property
    def Path(self):
        return self.__path

    @Path.setter
    def Path(self, value):
        self.__path = value

    @property
    def CurrentStep(self):
        return self.__currentStep

    @CurrentStep.setter
    def CurrentStep(self, value):
        self.__currentStep = value

    @property
    def CurrentPath(self):
        return self.__currenPath

    @CurrentPath.setter
    def CurrentPath(self, value):
        self.__currenPath = value
        
    #endregion Getter / Setter

    # Functions
    def AddCellToCurrentPath(self, x: int, y: int, exitCount: int, direction: int):
        """Ajout une cellule dans le chemin actuel
        """
        self.CurrentPath.append(Cell(x, y, exitCount, direction))

    def RemoveLastPos(self):
        """Supprime la dernière position
        """
        self.CurrentPath.pop()

    def GetFacingDirection(self) -> int:
        """Récupère la direction du robot
        """
        facing:int = 0x000

        if ((self.CurrentCell & C_ROBOT_N) > 0):
            facing = self.CurrentCell & C_ROBOT_N

        if ((self.CurrentCell & C_ROBOT_E) > 0):
            facing = self.CurrentCell & C_ROBOT_E

        if ((self.CurrentCell & C_ROBOT_S) > 0):
            facing = self.CurrentCell & C_ROBOT_S

        if ((self.CurrentCell & C_ROBOT_W) > 0):
            facing = self.CurrentCell & C_ROBOT_W

        return facing

    def GetFacingPathCell(self, x: int, y: int) -> int:
        """Récupère la cellule devant le robot

        Args:
            x: X position x de la cellule devant le robot
            y: Y position y de la cellule devant le robot

        Returns:
            La valeur de la cellule devant le robot si succes, sinon -1

        """
        facingDirection: int = self.GetFacingDirection()

        if (facingDirection == C_ROBOT_N):
            return self.Path[y - 1, x]
        if (facingDirection == C_ROBOT_E):
            return self.Path[y, x + 1]
        if (facingDirection == C_ROBOT_S):
            return self.Path[y + 1, x]
        if (facingDirection == C_ROBOT_W):
            return self.Path[y, x - 1]

        return -1

    def GetRightPathCell(self, x: int, y: int) -> int:
        """Récupère la cellule à droite du robot

        Args:
            x: X position x de la cellule à droite du robot
            y: Y position y de la cellule à droite du robot

        Returns:
            La valeur de la cellule à droite robot si succes, sinon -1

        """
        facingDirection: int = self.GetFacingDirection()

        if (facingDirection == C_ROBOT_N and x + 1 <= 15):
            return self.Path[y, x + 1]
        if (facingDirection == C_ROBOT_E and y + 1 <= 15):
            return self.Path[y + 1, x]
        if (facingDirection == C_ROBOT_S and x - 1 >= 0):
            return self.Path[y, x - 1]
        if (facingDirection == C_ROBOT_W and y - 1 >= 0):
            return self.Path[y - 1, x]

        return -1

    def GetLeftPathCell(self, x: int, y: int) -> int:
        """Récupère la cellule à gauche du robot

        Args:
            x: X position x de la cellule à gauche du robot
            y: Y position y de la cellule à gauche du robot

        Returns:
            La valeur de la cellule à gauche du robot si succes, sinon -1

        """
        facingDirection: int = self.GetFacingDirection()

        if (facingDirection == C_ROBOT_N and x - 1 >= 0):
            return self.Path[y, x - 1]
        if (facingDirection == C_ROBOT_E and y - 1 >= 0):
            return self.Path[y - 1, x]
        if (facingDirection == C_ROBOT_S and x + 1 <= 15):
            return self.Path[y, x + 1]
        if (facingDirection == C_ROBOT_W and y + 1 <= 15):
            return self.Path[y + 1, x]

        return -1

    def CanGoNorth(self) -> bool:
        """Test si le robot peut aller au Nord
        """
        return ((self.CurrentCell & C_N) == 0) 

    def CanGoEast(self) -> bool:
        """Test si le robot peut aller à l'Est
        """
        return ((self.CurrentCell & C_E) == 0) 

    def CanGoSouth(self) -> bool:
        """Test si le robot peut aller au Sud
        """
        return ((self.CurrentCell & C_S) == 0) 

    def CanGoWest(self) -> bool:
        """Test si le robot peut aller à l'Ouest
        """
        return ((self.CurrentCell & C_W) == 0) 

    def CanGoForward(self) -> bool:
        """Test si le robot peut aller devant
        """
        if (self.GetFacingDirection() == C_ROBOT_N):
            return self.CanGoNorth()
        if (self.GetFacingDirection() == C_ROBOT_E):
            return self.CanGoEast()
        if (self.GetFacingDirection() == C_ROBOT_S):
            return self.CanGoSouth()
        if (self.GetFacingDirection() == C_ROBOT_W):
            return self.CanGoWest()

        return False

    def CanGoLeft(self) -> bool:
        """Test si le robot peut aller à gauche
        """
        if (self.GetFacingDirection() == C_ROBOT_N):
            return self.CanGoWest()
        if (self.GetFacingDirection() == C_ROBOT_E):
            return self.CanGoNorth()
        if (self.GetFacingDirection() == C_ROBOT_S):
            return self.CanGoEast()
        if (self.GetFacingDirection() == C_ROBOT_W):
            return self.CanGoSouth()

        return False

    def CanGoRight(self) -> bool:
        """Test si le robot peut aller à droite
        """
        if (self.GetFacingDirection() == C_ROBOT_N):
            return self.CanGoEast()
        if (self.GetFacingDirection() == C_ROBOT_E):
            return self.CanGoSouth()
        if (self.GetFacingDirection() == C_ROBOT_S):
            return self.CanGoWest()
        if (self.GetFacingDirection() == C_ROBOT_W):
            return self.CanGoNorth()

        return False

    def IsOnGoal(self) -> bool:
        """Test si le robot est arrivé à la sortie
        """
        return ((self.CurrentCell & C_GOAL) > 0)
