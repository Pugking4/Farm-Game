import arcade
from tile import Tile
from player import Player
from message import Message

class myGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.WHITE)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Msic
        self.message = None
        self.growth_rate = 1/60

    def setup(self, MAP_SIZE, LEFT_MARGIN, BOTTOM_MARGIN, TILE_SIZE, SPRITE_SCALING, MOVEMENT_SPEED):
        # Set up your game here
        #Constants

        self.LEFT_MARGIN = LEFT_MARGIN
        self.BOTTOM_MARGIN = BOTTOM_MARGIN
        self.MAP_SIZE = MAP_SIZE
        self.TILE_SIZE = TILE_SIZE
        self.SPRITE_SCALING = SPRITE_SCALING
        self.MOVEMENT_SPEED = MOVEMENT_SPEED

        # Sprite setup
        self.player_list = arcade.SpriteList()
        self.current_tile = None

        # Generate map
        self.map = []
        for i in range(self.MAP_SIZE[1]):
            row = []
            for j in range(self.MAP_SIZE[0]):
                row.append(Tile(0))
            self.map.append(row)
        self.map[0][0].type = 10
        self.map[4][6].type = 10

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", self.SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = self.MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = self.MOVEMENT_SPEED * -1
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = self.MOVEMENT_SPEED * -1
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.MOVEMENT_SPEED * 1

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Loop for each row
        for i in range(len(self.map)):
            # Loop for each column
            for j in range(len(self.map[i])):
                # Calculate our location
                x = j * self.TILE_SIZE + self.LEFT_MARGIN
                y = i * self.TILE_SIZE + self.BOTTOM_MARGIN

                self.map[i][j].bounds = ((x-self.TILE_SIZE/2, x+self.TILE_SIZE/2), (y-self.TILE_SIZE/2, y+self.TILE_SIZE/2))

                # Draw the item
                if self.map[i][j].type == 10:
                    arcade.draw_rectangle_filled(x, y, self.TILE_SIZE, self.TILE_SIZE, arcade.color.DARK_BROWN)
                elif self.map[i][j].type == 20:
                    arcade.draw_rectangle_filled(x, y, self.TILE_SIZE, self.TILE_SIZE, arcade.color.YELLOW_GREEN)
                elif self.map[i][j].type == 30:
                    arcade.draw_rectangle_filled(x, y, self.TILE_SIZE, self.TILE_SIZE, arcade.color.PASTEL_YELLOW)
                else:
                    arcade.draw_rectangle_filled(x, y, self.TILE_SIZE, self.TILE_SIZE, arcade.color.SAP_GREEN)
        
        if self.message:
            if self.message.fade_in[1]+1 < self.message.frames <= self.message.fade_in[0]:
                self.message.alpha += 255 / self.message.fade
                #print(self.message.alpha)
            elif self.message.fade_out[1] <= self.message.frames < self.message.fade_out[0]:
                self.message.alpha -= 255 / self.message.fade
                #print(self.message.alpha)
            else:
                self.message.alpha = 255
                #print("reset")

            arcade.Text(self.message.text, self.player_sprite.center_x, self.player_sprite.center_y + 50, (0, 0, 0, int(self.message.alpha)), 20, anchor_x="center").draw()
            self.message.frames -= 1
            if self.message.frames < 0:
                self.message = None


        # Draw all the sprites.
        self.player_list.draw()


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update()

        for count_y, i in enumerate(self.map):
            for count_x, j in enumerate(i):
                if j.bounds[0][0] <= self.player_sprite.center_x <= j.bounds[0][1] and j.bounds[1][0] <= self.player_sprite.center_y <= j.bounds[1][1] and j != self.current_tile:
                    # Player is within the bounds of the tile
                    print(f"Player is on tile type {j.type}", f"({count_x}, {count_y})")
                    self.current_tile = self.map[count_y][count_x]
                
                if j.type == 20:
                    if j.growth >= j.grow_cap:
                        j.type = 30
                    else:
                        j.growth += self.growth_rate
        

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()
        elif key == arcade.key.C:
            if self.current_tile.type == 0:
                self.current_tile.type = 10
                print("Tile changed to type 1")
                self.message = Message("Sowed the soil", 150, True)
            elif self.current_tile.type == 30:
                self.current_tile.wheat()
                print("Tile changed to type 20")
                self.message = Message("Harvested wheat", 150, True)
        elif key == arcade.key.F:
            if self.current_tile.type == 10:
                self.current_tile.wheat()
                self.message = Message("Planted wheat", 150, True)
            else:
                self.message = Message("No soil to plant in", 75, True)
        elif key == arcade.key.R:
            if self.current_tile.type == 20 or self.current_tile.type == 30:
                self.message = Message(f"{self.current_tile.growth}/{self.current_tile.grow_cap}", 150, True)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        
        print(f"Click at ({x}, {y})")
        for i in self.map:
            for j in i:
                if j.bounds[0][0] <= x <= j.bounds[0][1] and j.bounds[1][0] <= y <= j.bounds[1][1]:
                    #j.type = 1
                    print(f"Clicked on tile type {j.type}")
