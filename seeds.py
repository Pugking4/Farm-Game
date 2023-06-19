class Seed:
    def __init__(self, _type, price, image, name, amount=1):
        self.type = _type
        self.price = price
        self.image = image
        self.name = name
        self.amount = amount

class wheatSeed(Seed):
    def __init__(self, amount=1):
        super().__init__(0, 1, "", 'Wheat Seed', amount)

class carrotSeed(Seed):
    def __init__(self, amount=1):
        super().__init__(1, 2, "", 'Carrot Seed', amount)
