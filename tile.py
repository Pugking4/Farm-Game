class Tile:
    def __init__(self, type: int) -> None:
        self.type = type
        self.bounds = ((0, 0), (0, 0))