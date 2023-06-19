import arcade
from PIL import ImageFont
from tile import Tile
from player import Player
from message import Message
from seeds import *
from produce import *
from functions import *
from shop import Shop
from money import Money

class myGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.WHITE)

        # Screen
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

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
        self.evaporation_rate = 1/60/10
        

    def setup(self, MAP_SIZE, LEFT_MARGIN, BOTTOM_MARGIN, TILE_SIZE, SPRITE_SCALING, MOVEMENT_SPEED, SCALING, GUI_BUFFER, ICON_SIZE):
        # Set up your game here
        #Constants

        self.LEFT_MARGIN = LEFT_MARGIN
        self.BOTTOM_MARGIN = BOTTOM_MARGIN
        self.MAP_SIZE = MAP_SIZE
        self.TILE_SIZE = TILE_SIZE
        self.SPRITE_SCALING = SPRITE_SCALING
        self.MOVEMENT_SPEED = MOVEMENT_SPEED
        self.SCALING = SCALING
        self.GUI_BUFFER = GUI_BUFFER
        self.ICON_SIZE = ICON_SIZE

        # Sprite setup
        self.player_list = arcade.SpriteList()

        #Misc
        self.shop = Shop((GUI_BUFFER, ICON_SIZE + GUI_BUFFER, self.SCREEN_HEIGHT - ICON_SIZE - GUI_BUFFER, self.SCREEN_HEIGHT - GUI_BUFFER),
                        (self.SCREEN_WIDTH - (ICON_SIZE + GUI_BUFFER)*2, self.SCREEN_WIDTH - GUI_BUFFER, self.SCREEN_HEIGHT - ICON_SIZE - GUI_BUFFER, self.SCREEN_HEIGHT - GUI_BUFFER),
                        (self.SCREEN_WIDTH - (ICON_SIZE + GUI_BUFFER), self.SCREEN_WIDTH - GUI_BUFFER, self.SCREEN_HEIGHT - ICON_SIZE - GUI_BUFFER, self.SCREEN_HEIGHT - GUI_BUFFER))

        # Generate map
        self.map = []
        for i in range(self.MAP_SIZE[1]):
            row = []
            for j in range(self.MAP_SIZE[0]):
                row.append(Tile(0))
            self.map.append(row)
        self.map[0][0].type = 10
        self.map[4][6].type = 10

        self.current_tile = self.map[0][0]
        self.SEED_TYPE_DICT = {
            0: ("Wheat", self.current_tile.wheat),
            1: ("Carrot", self.current_tile.carrot)
        }

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", self.SPRITE_SCALING, 50, 50, self.SCALING, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
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
                elif self.map[i][j].type == 21:
                    arcade.draw_rectangle_filled(x, y, self.TILE_SIZE, self.TILE_SIZE, arcade.color.CARROT_ORANGE)
                elif self.map[i][j].type == 31:
                    arcade.draw_rectangle_filled(x, y, self.TILE_SIZE, self.TILE_SIZE, arcade.color.DEEP_CARROT_ORANGE)
                else:
                    arcade.draw_rectangle_filled(x, y, self.TILE_SIZE, self.TILE_SIZE, arcade.color.SAP_GREEN)
        
        arcade.draw_rectangle_outline(self.current_tile.bounds[0][0] + self.TILE_SIZE/2, self.current_tile.bounds[1][0] + self.TILE_SIZE/2, self.TILE_SIZE, self.TILE_SIZE, arcade.color.BLUE, 5)
        
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

            arcade.Text(self.message.text, self.player_sprite.center_x, self.player_sprite.center_y + 50, (0, 0, 0, int(self.message.alpha)), 40/self.SCALING, anchor_x="center").draw()
            self.message.frames -= 1
            if self.message.frames < 0:
                self.message = None

        # Draw all the sprites.
        self.player_list.draw()
            
        list_x = []
        total_y = 0
        _text = []
        #arcade.draw_rectangle_outline(self.SCREEN_WIDTH - (150 + self.GUI_BUFFER)/self.SCALING, self.SCREEN_HEIGHT - (50 + self.GUI_BUFFER)/self.SCALING, 300/self.SCALING, 100/self.SCALING, arcade.color.DARK_GRAY, 1)
        for count, i in enumerate(self.player_sprite.inventory):
 
            font = ImageFont.truetype('calibri.ttf', int(20/self.SCALING*2))
            size = font.getsize(f"{i.name}: {i.amount}")

            list_x.append(size[0])
            total_y += size[1]
            #print(list_x)

            _text.append(arcade.Text(f"{i.name}: {i.amount}", self.SCREEN_WIDTH - self.GUI_BUFFER*2, self.SCREEN_HEIGHT - self.GUI_BUFFER - self.GUI_BUFFER*3 - size[1] * count, arcade.color.BLACK, 20/self.SCALING, anchor_x="right"))
        #print(size)
        #print(self.SCREEN_WIDTH - (max(list_x) + self.GUI_BUFFER*3), self.SCREEN_HEIGHT - self.GUI_BUFFER*3, max(list_x) + self.GUI_BUFFER*2, total_y + self.GUI_BUFFER*2)
        #print(max(list_x))
        #arcade.draw_line(self.SCREEN_WIDTH - self.GUI_BUFFER, self.SCREEN_HEIGHT - self.GUI_BUFFER, self.SCREEN_WIDTH - self.GUI_BUFFER, 0, arcade.color.RED, 1)
        #arcade.draw_line(self.GUI_BUFFER, self.SCREEN_HEIGHT - self.GUI_BUFFER, self.GUI_BUFFER, 0, arcade.color.RED, 1)
        #arcade.draw_line(self.SCREEN_WIDTH - self.GUI_BUFFER, self.SCREEN_HEIGHT - self.GUI_BUFFER, 0, self.SCREEN_HEIGHT - self.GUI_BUFFER, arcade.color.RED, 1)

        arcade.draw_rectangle_filled(self.SCREEN_WIDTH - (max(list_x) - self.GUI_BUFFER)/2, self.SCREEN_HEIGHT - ((self.GUI_BUFFER*3 + total_y)/2), (max(list_x) - self.GUI_BUFFER*3), -(total_y + self.GUI_BUFFER), arcade.color.WHITE_SMOKE)
        arcade.draw_rectangle_outline(self.SCREEN_WIDTH - (max(list_x) - self.GUI_BUFFER)/2, self.SCREEN_HEIGHT - ((self.GUI_BUFFER*3 + total_y)/2), (max(list_x) - self.GUI_BUFFER*3), -(total_y + self.GUI_BUFFER), arcade.color.DARK_GRAY, 1)

        for i in _text:
            i.draw()
        
        arcade.draw_rectangle_filled((self.ICON_SIZE/2) + self.GUI_BUFFER, self.SCREEN_HEIGHT - ((self.ICON_SIZE/2) + self.GUI_BUFFER), (self.ICON_SIZE), (self.ICON_SIZE), arcade.color.OLD_GOLD)

        if self.shop.open:
            arcade.draw_rectangle_filled(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, (185, 163, 126))
            
            arcade.draw_rectangle_filled(self.SCREEN_WIDTH/2, (self.SCREEN_HEIGHT-(self.ICON_SIZE + self.GUI_BUFFER*2))-(200/self.SCALING), self.SCREEN_WIDTH - self.GUI_BUFFER*2, (400/self.SCALING), (209, 190, 157))
            arcade.draw_rectangle_outline(self.SCREEN_WIDTH/2, (self.SCREEN_HEIGHT-(self.ICON_SIZE + self.GUI_BUFFER*2))-(200/self.SCALING), self.SCREEN_WIDTH - self.GUI_BUFFER*2, (400/self.SCALING), (100, 81, 59), 1)

            arcade.draw_rectangle_filled(self.SCREEN_WIDTH/2, 200/self.SCALING + self.GUI_BUFFER, self.SCREEN_WIDTH - self.GUI_BUFFER*2, (400/self.SCALING), (209, 190, 157))
            arcade.draw_rectangle_outline(self.SCREEN_WIDTH/2, 200/self.SCALING + self.GUI_BUFFER, self.SCREEN_WIDTH - self.GUI_BUFFER*2, (400/self.SCALING), (100, 81, 59), 1)
            
            arcade.draw_rectangle_filled((self.ICON_SIZE/2) + self.GUI_BUFFER, self.SCREEN_HEIGHT - ((self.ICON_SIZE/2) + self.GUI_BUFFER), (self.ICON_SIZE), (self.ICON_SIZE), arcade.color.RED_DEVIL)
            arcade.draw_rectangle_filled(self.SCREEN_WIDTH - ((self.ICON_SIZE/2) + self.GUI_BUFFER), self.SCREEN_HEIGHT - ((self.ICON_SIZE/2) + self.GUI_BUFFER), (self.ICON_SIZE), (self.ICON_SIZE), arcade.color.DUTCH_WHITE)
            arcade.draw_rectangle_filled(self.SCREEN_WIDTH - ((self.ICON_SIZE*1.5) + self.GUI_BUFFER*2), self.SCREEN_HEIGHT - ((self.ICON_SIZE/2) + self.GUI_BUFFER), (self.ICON_SIZE), (self.ICON_SIZE), arcade.color.DUTCH_WHITE)
        
        

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
                    print(f"Player is on tile type {j.type:02d}", f"({count_x}, {count_y})")
                    self.current_tile = self.map[count_y][count_x]
                if int(f"{j.type:02d}"[0]) == 2:
                    if j.growth >= j.grow_cap:
                        j.type += 10
                        j.growth = int(j.growth)
                    else:
                        j.growth += self.growth_rate * (j.water / j.water_cap)
                
                if j.water > self.evaporation_rate:
                    j.water -= self.evaporation_rate
                elif j.water == self.evaporation_rate:
                    j.water = 0
                
        # 0x Base Block
        # 1x Plowed Block
        # 2x Crop Block
        # 3x Grown Crop Block

        # x0 Dirt Type

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
            if type_convert(self.current_tile.type, 0) == 0:
                self.current_tile.type += 10
                print("Tile changed to type 1")
                self.message = Message("Sowed the soil", 150, True)
            elif type_convert(self.current_tile.type, 0) == 3:
                if type_convert(self.current_tile.type, 1) == 0:
                    index = next((i for i, obj in enumerate(self.player_sprite.inventory) if isinstance(obj, Wheat)), None)
                    if index is not None:
                        self.player_sprite.inventory[index].amount += 1
                    else:
                        self.player_sprite.inventory.append(Wheat(1))
                elif type_convert(self.current_tile.type, 1) == 1:
                    index = next((i for i, obj in enumerate(self.player_sprite.inventory) if isinstance(obj, Carrot)), None)
                    if index is not None:
                        self.player_sprite.inventory[index].amount += 1
                    else:
                            self.player_sprite.inventory.append(Carrot(1))
                self.current_tile.type -= 10
                self.current_tile.growth = 0

                print(f"Tile changed to type {self.current_tile.type}")
                self.message = Message(f"Harvested {self.SEED_TYPE_DICT[type_convert(self.current_tile.type, 1)][0]}", 150, True)

        elif key == arcade.key.F:
            if self.current_tile.type == 10:
                if int(str(f"{self.player_sprite.hand.type:02d}")[1]) == 0 and self.player_sprite.hand.amount > 0:
                    self.current_tile.wheat()
                elif int(str(f"{self.player_sprite.hand.type:02d}")[1]) == 1 and self.player_sprite.hand.amount > 0:
                    self.current_tile.carrot()
                self.player_sprite.hand.amount -= 1
                self.message = Message(f"Planted {self.player_sprite.hand.name}", 150, True)
            else:
                self.message = Message("No soil to plant in", 75, True)

        elif key == arcade.key.R:
            if type_convert(self.current_tile.type, 0) in [2, 3]:
                self.message = Message(f"{round(self.current_tile.growth, 1)}/{self.current_tile.grow_cap} {round(self.current_tile.water, 2)}/{self.current_tile.water_cap}", 150, True)

        elif key == arcade.key.E:
            if self.current_tile.water + 20 <= self.current_tile.water_cap:
                self.current_tile.water += 20
            else:
                self.current_tile.water = self.current_tile.water_cap
        elif key == arcade.key.Q:
            self.player_sprite.hand_num += 1
            if self.player_sprite.hand_num >= len(self.player_sprite.inventory):
                self.player_sprite.hand_num = 0
            if self.player_sprite.hand == Money:
                self.player_sprite.hand_num += 1
            self.player_sprite.hand = self.player_sprite.inventory[self.player_sprite.hand_num]
            self.message = Message(f"Selected {self.player_sprite.hand.name}", 50, True)
            

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
                    print(f"Clicked on tile type {j.type:02d}")
        
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.shop.bounds[0][0] <= x <= self.shop.bounds[0][1] and self.shop.bounds[1][0] <= y <= self.shop.bounds[1][1]:
                if self.shop.open:
                    self.shop.open = False
                else:
                    self.shop.open = True
            elif self.shop.open and self.shop.forward_bounds[0][0] <= x <= self.shop.forward_bounds[0][1] and self.shop.forward_bounds[1][0] <= y <= self.shop.forward_bounds[1][1]:
                print("Forward")
            elif self.shop.open and self.shop.back_bounds[0][0] <= x <= self.shop.back_bounds[0][1] and self.shop.back_bounds[1][0] <= y <= self.shop.back_bounds[1][1]:
                print("Back")
            else:
                print(self.shop.forward_bounds)
                print(self.shop.back_bounds)