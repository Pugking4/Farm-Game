from seeds import *
from produce import *

class Shop:
    def __init__(self, bounds, back_bounds, forward_bounds):
        self.items = []
        self.bounds = ((bounds[0], bounds[1]), (bounds[2], bounds[3]))
        self.back_bounds = ((back_bounds[0], back_bounds[1]), (back_bounds[2], back_bounds[3]))
        self.forward_bounds = ((forward_bounds[0], forward_bounds[1]), (forward_bounds[2], forward_bounds[3]))
        self.open = False
        self.stock = {
            'Wheat Seed': [wheatSeed(amount=20), None],
            'Carrot Seed': [carrotSeed(amount=20), None]
        }
        self.sell = {
            'Wheat': [Wheat(amount=3), None],
            'Carrot': [Carrot(amount=2), None]
        }


    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items