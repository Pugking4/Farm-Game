from typing import Optional
import arcade
from arcade import Texture
from seeds import *
from money import Money

class Player(arcade.Sprite):
    def __init__(self, filename: str, scale: float, center_x: float, center_y: float, SCALING, SCREEN_WIDTH, SCREEN_HEIGHT) -> None:
        super().__init__(filename, scale)

        self.SPRITE_SCALING = scale
        self.SCALING = SCALING
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.inventory = [Money(amount=20), wheatSeed(amount=5), carrotSeed(amount=2)]
        self.hand_num = 1
        self.hand = self.inventory[self.hand_num]

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > self.SCREEN_WIDTH - 1:
            self.right = self.SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > self.SCREEN_HEIGHT - 1:
            self.top = self.SCREEN_HEIGHT - 1