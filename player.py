from typing import Optional
import arcade
from arcade import Texture

class Player(arcade.Sprite):
    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > 1920/2 - 1:
            self.right = 1920/2 - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > 1080/2 - 1:
            self.top = 1080/2 - 1