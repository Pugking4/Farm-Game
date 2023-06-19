import arcade
from game import myGame

# Screen
SCALING = 2.0
SCREEN_WIDTH = int(1900/SCALING)
SCREEN_HEIGHT = int(1000/SCALING)
GUI_BUFFER = int(10/SCALING)
ICON_SIZE = int(120/SCALING)

# Map
TILE_SIZE = int(100/SCALING)
MAP_SIZE = (int(round(SCREEN_WIDTH/TILE_SIZE, 0)), int(round(SCREEN_HEIGHT/TILE_SIZE, 0)))
FARM_SIZE = (7, 5)
LEFT_MARGIN = int((SCREEN_WIDTH - (MAP_SIZE[0] * TILE_SIZE)) / 2)
BOTTOM_MARGIN = int((SCREEN_HEIGHT - (MAP_SIZE[1] * TILE_SIZE)) / 2)

GRASS_TEXTURES = [arcade.load_texture("assets\grasstileset\grass_064.png"), 
                  arcade.load_texture("assets\grasstileset\grass_065.png"), 
                  arcade.load_texture("assets\grasstileset\grass_079.png"), 
                  arcade.load_texture("assets\grasstileset\grass_080.png"), 
                  arcade.load_texture("assets\grasstileset\grass_049.png"), 
                  arcade.load_texture("assets\grasstileset\grass_050.png")]

# Sprite
SPRITE_SCALING = 1.5/SCALING
MOVEMENT_SPEED = 5

def main():
    game = myGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup(MAP_SIZE, LEFT_MARGIN, BOTTOM_MARGIN, TILE_SIZE, SPRITE_SCALING, MOVEMENT_SPEED, SCALING, GUI_BUFFER, ICON_SIZE, GRASS_TEXTURES)
    arcade.run()

if __name__ == "__main__":
    main()
