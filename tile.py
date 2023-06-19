class Tile:
    def __init__(self, type: int, tex) -> None:
        self.type = type
        self.bounds = ((0, 0), (0, 0))
        if self.type == 0:
            self.water_cap = 100
        self.water = 0
        self.growth = 0
        self.tex = tex
    
    def wheat(self):
        self.type = 20
        self.grow_cap = 10 #60
    
    def carrot(self):
        self.type = 21
        self.grow_cap = 15

