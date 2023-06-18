import arcade
from game import myGame

# Screen
SCALING = 2.0
SCREEN_WIDTH = int(1920/SCALING)
SCREEN_HEIGHT = int(1080/SCALING)

# Map
MAP_SIZE = (7, 5)
TILE_SIZE = int(150/SCALING)
LEFT_MARGIN = int((SCREEN_WIDTH - (MAP_SIZE[0] * TILE_SIZE)) / 2)
BOTTOM_MARGIN = int((SCREEN_HEIGHT - (MAP_SIZE[1] * TILE_SIZE)) / 2)

# Sprite
SPRITE_SCALING = 0.75
MOVEMENT_SPEED = 5

def main():
    game = myGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup(MAP_SIZE, LEFT_MARGIN, BOTTOM_MARGIN, TILE_SIZE, SPRITE_SCALING, MOVEMENT_SPEED)
    arcade.run()

if __name__ == "__main__":
    main()