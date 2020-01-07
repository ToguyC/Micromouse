class Cell():
    """
    Représentation d'une cellule
    """

    def __init__(self, x: int, y: int, exitCount: int, direction: int):
        """
        Constructeur
        """
        self.__coord = [x, y]
        self.__exits = exitCount
        self.__direction = direction

    #region Getter / Setter
    @property
    def Coord(self):
        return self.__coord

    @Coord.setter
    def Coord(self, value):
        self.__coord = value
    
    @property
    def Exits(self):
        return self.__exits

    @Exits.setter
    def Exits(self, value):
        self.__exits = value

    @property
    def Direction(self):
        return self.__direction

    @Direction.setter
    def Direction(self, value):
        self.__direction = value
    
    #endregion Getter / Setter