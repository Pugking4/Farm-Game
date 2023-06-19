class Produce:
    def __init__(self, _type, price, image, name, amount=1):
        self.type = _type
        self.price = price
        self.image = image
        self.name = name
        self.amount = amount

class Wheat(Produce):
    def __init__(self, amount=1):
        super().__init__(0, 2, "", 'Wheat', amount)

class Carrot(Produce):
    def __init__(self, amount=1):
        super().__init__(1, 4, "", 'Carrot', amount)
