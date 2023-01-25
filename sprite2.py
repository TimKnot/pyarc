"""
Sprite2: An experiment with sprite scaling, sorting and mouse actions.
Usage:
    Left mouse button - Click on ship to eject the pilot.
    Space - Eject a random pilot.
    Backspace - Eject all the pilots.
    F1 - Debug info. Show how many sprites are active.
"""

from time import time
from random import random, randint, choice
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite2: Scaling and sorting"
SHIP_FREQUENCY_SECONDS = 0.15
VSYNC=False

class Ship(arcade.Sprite):
    """ Move a random ship across the screen left to right.
        Larger ones are faster, to give a sense of distance. """

    image_list = [
        ":resources:/images/space_shooter/playerShip1_blue.png",
        ":resources:/images/space_shooter/playerShip1_green.png",
        ":resources:/images/space_shooter/playerShip1_orange.png",
        ":resources:/images/space_shooter/playerShip2_orange.png",
        ":resources:/images/space_shooter/playerShip3_orange.png",
    ]

    def __init__(self):
        size_factor = random()+0.1  # Defines the scale and size of the ship

        # Call the parent init (and pick a random image from the list)
        super().__init__(filename=choice(self.image_list), scale=size_factor)

        self.right = -1  # just off left edge of screen
        self.center_y = randint(0, SCREEN_HEIGHT)
        self.angle = -90  # facing right
        self.angle_delta = 0
        self.scale_delta = 0
        self.x_delta = size_factor*7  # Bigger/nearer the ship, faster it goes

    def update(self):
        # Move right. Apply any rotation/scaling.
        self.center_x += self.x_delta
        self.angle += self.angle_delta
        self.scale += self.scale_delta

        # Kill if off screen or too small to see.
        if self.left > SCREEN_WIDTH or self.scale <= 0:
            self.kill()

    def tumble(self):
        """ Set the ship to tumble and 'fall' """
        self.angle_delta = randint(-5, +5)
        self.scale_delta = -0.01


class EjectedPilot(arcade.Sprite):
    """ A spinning creature that grows then shrinks. """

    image_list = [
        ":resources:images/alien/alienBlue_front.png",
        ":resources:/images/enemies/bee.png",
        ":resources:/images/enemies/saw.png",
        ":resources:/images/enemies/slimeBlock.png",
        ":resources:/images/enemies/wormPink.png",
    ]

    def __init__(self, x, y, scale):
        super().__init__(filename=choice(self.image_list), scale=0.1)
        self.center_x = x
        self.center_y = y
        self.scale = scale / 5
        self.angle = randint(0, 359)
        self.max_scale = self.scale*10
        self.scale_delta = (self.max_scale - self.scale) / 100
        self.angle_delta = randint(1, 10)

    def update(self):
        # Rotate the ship
        self.angle += self.angle_delta
        self.scale += self.scale_delta

        # Grow then shrink
        if self.scale > self.max_scale:
            self.scale_delta *= -1
        elif self.scale <= 0:
            self.kill()


class MyGame(arcade.Window):
    def __init__(self, width, height, title, vsync=False):
        super().__init__(width, height, title, vsync)
        arcade.set_background_color(arcade.color.BLACK)

        self.ship_list = None
        self.pilot_list = None
        self.previous_time = time()

    def setup(self):
        self.ship_list = arcade.SpriteList()
        self.pilot_list = arcade.SpriteList()

    def on_draw(self):
        """ Merge all the sprites into one list, then sort by scale.
            This forces bigger/nearer ones to be drawn over far away ones.
            There's probably a better way to do this! """
        self.clear()
        all_sprites = arcade.SpriteList()
        all_sprites.extend(self.ship_list)
        all_sprites.extend(self.pilot_list)
        all_sprites.sort(key=lambda s: s.scale)
        all_sprites.draw()

    def on_update(self, delta_time):
        global timer
        self.ship_list.update()
        self.pilot_list.update()

        # Produce a new ship every SHIP_FREQUENCY_SECONDS
        t = time()
        if t > self.previous_time + SHIP_FREQUENCY_SECONDS:
            self.previous_time = t
            self.ship_list.append(Ship())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # Quit
            arcade.exit()

        elif key == arcade.key.F1:
            # Show number of active sprites
            print(f"Ships: {len(self.ship_list)} "
                  f"Pilots: {len(self.pilot_list)}")

        elif key == arcade.key.SPACE:
            # Eject a pilot from a random ship and set the ship spinning
            ship = choice(self.ship_list)
            self.eject_pilot_from_ship(ship)

        elif key == arcade.key.BACKSPACE:
            # Eject all the pilots!
            for ship in self.ship_list:
                self.eject_pilot_from_ship(ship)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Eject the pilot from the ships being clicked on. """
        ships = arcade.get_sprites_at_point((x, y), self.ship_list)
        for ship in ships:
            self.eject_pilot_from_ship(ship)

    def eject_pilot_from_ship(self, ship):
        """ Create a pilot at the ships location, and set ship tumbling. """
        ship.tumble()
        new_pilot = EjectedPilot(ship.center_x, ship.center_y, ship.scale)
        self.pilot_list.append(new_pilot)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, VSYNC)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()