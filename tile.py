class Tile:
    def __init__(self, type: int) -> None:
        self.type = type
        self.bounds = ((0, 0), (0, 0))
    
    
    def wheat(self):
        self.type = 20
        self.grow_cap = 10 #60
        self.growth = 0
