"""
Sprite2 Meteor Performance:
    A sprite stress testing experiment.
    Based on Sprite2 - But modified to look at performance.
Usage:
    Left mouse button - Click on ship to eject the pilot.
    Space - Eject a random pilot.
    Backspace - Eject all the pilots.
    P - Display/hide performance metrics.
    F1 - Debug info. Show how many sprites are active.
    F2 - Switch between meteor types.

    ESC - Quit

TLDR: Rotating thousands of sprites every frame is computationally expensive!
      Circle Sprites or Sprites based on images doesn't make much difference.

Bonus: Trippy mode looks pretty cool with thousands of meteors :)

TODO:
    - Put Pilots and Ships back in one list?
"""

from time import time
from random import uniform, randint, choice
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite2: Meteor Performance"
VSYNC = False
TRIPPY_MODE = False
SHIP_FREQUENCY_SECONDS = 0.15
METEOR_FREQUENCY_SECONDS = 0.3
MAX_METEORS = 2000
METEORS_TO_ADD = 300

# Size of performance graphs and distance between them
PERFORMANCE_METRICS = True
GRAPH_WIDTH = int(SCREEN_WIDTH/2)
GRAPH_HEIGHT = 200


###############################################################################
class CircleMeteor(arcade.SpriteCircle):
    """ Move a meteor across screen right to left.
        Larger ones are faster, to give a sense of depth. """

    def __init__(self):
        # Call the parent init (and pick a random image from the list)
        super().__init__(radius=randint(1, 8),
                         color=(155, 155, 155))

        self.left = SCREEN_WIDTH  # just off right edge of screen
        self.center_y = randint(0, SCREEN_HEIGHT)

        self.delta_x = -self.width  # nearer/bigger = faster

    def update(self):
        # Update position.
        self.center_x += self.delta_x

        # Kill if off screen.
        if self.right < 0:
            self.kill()


###############################################################################
class NoRotationMeteor(arcade.Sprite):
    """ Move a meteor across screen right to left.
        Larger ones are faster, to give a sense of depth. """

    image_list = [
        ":resources:/images/space_shooter/meteorGrey_med1.png",
        ":resources:/images/space_shooter/meteorGrey_med2.png",
        ":resources:/images/space_shooter/meteorGrey_small1.png",
        ":resources:/images/space_shooter/meteorGrey_small2.png",
    ]

    def __init__(self):
        # Call the parent init (and pick a random image from the list)
        super().__init__(filename=choice(self.image_list),
                         scale=uniform(0.1, 0.5))

        self.left = SCREEN_WIDTH  # just off right edge of screen
        self.center_y = randint(0, SCREEN_HEIGHT)
        self.delta_x = -self.scale*20  # nearer/bigger = faster

    def update(self):
        # Update position. Apply any rotation.
        self.center_x += self.delta_x

        # Kill if off screen.
        if self.right < 0:
            self.kill()


###############################################################################
class RotatingMeteor(arcade.Sprite):
    """ Move a meteor across screen right to left.
        Larger ones are faster, to give a sense of depth. """

    image_list = [
        ":resources:/images/space_shooter/meteorGrey_med1.png",
        ":resources:/images/space_shooter/meteorGrey_med2.png",
        ":resources:/images/space_shooter/meteorGrey_small1.png",
        ":resources:/images/space_shooter/meteorGrey_small2.png",
    ]

    def __init__(self):
        # Call the parent init (and pick a random image from the list)
        super().__init__(filename=choice(self.image_list),
                         scale=uniform(0.1, 0.5))

        self.left = SCREEN_WIDTH  # just off right edge of screen
        self.center_y = randint(0, SCREEN_HEIGHT)
        self.angle = 0
        self.delta_angle = randint(-5, 5)
        self.delta_x = -self.scale*20  # nearer/bigger = faster

    def update(self):
        # Update position. Apply any rotation.
        self.center_x += self.delta_x
        self.angle += self.delta_angle

        # Kill if off screen.
        if self.right < 0:
            self.kill()


###############################################################################
class Ship(arcade.Sprite):
    """ Move a random ship across the screen left to right.
        Larger ones are faster, to give a sense of depth. """

    image_list = [
        ":resources:/images/space_shooter/playerShip1_blue.png",
        ":resources:/images/space_shooter/playerShip1_green.png",
        ":resources:/images/space_shooter/playerShip1_orange.png",
        ":resources:/images/space_shooter/playerShip2_orange.png",
        ":resources:/images/space_shooter/playerShip3_orange.png",
    ]

    def __init__(self):
        # Call the parent init (and pick a random image from the list)
        super().__init__(filename=choice(self.image_list),
                         scale=uniform(0.1, 1.0))

        self.right = -1  # just off left edge of screen
        self.center_y = randint(0, SCREEN_HEIGHT)
        self.angle = -90  # facing right
        self.delta_angle = 0
        self.delta_scale = 0
        self.delta_x = self.scale*7  # Bigger/nearer the ship, faster it goes
        self.tumbling = False

    def update(self):
        # Update position. Apply any rotation/scaling.
        self.center_x += self.delta_x
        self.angle += self.delta_angle
        self.scale += self.delta_scale

        # Kill if off screen or too small to see.
        if self.left > SCREEN_WIDTH or self.scale <= 0:
            self.kill()

    def tumble(self):
        """ Set the ship to tumble and 'fall' """
        self.delta_angle = randint(-5, +5)
        self.delta_scale = -0.01
        self.tumbling = True


###############################################################################
class EjectedPilot(arcade.Sprite):
    """ A spinning creature that grows then shrinks. """

    image_list = [
        "enemies/slimeBlock.png",
        "enemies/wormPink.png",
        "animated_characters/female_adventurer/femaleAdventurer_jump.png",
        "animated_characters/male_adventurer/maleAdventurer_fall.png",
        "animated_characters/robot/robot_fall.png",
        "animated_characters/zombie/zombie_idle.png",
    ]

    def __init__(self, x, y, scale, delta_x=0):
        file = f":resources:/images/{choice(EjectedPilot.image_list)}"
        super().__init__(filename=file, scale=scale)
        self.center_x = x
        self.center_y = y
        self.delta_x = delta_x
        self.angle = randint(0, 359)
        self.max_scale = self.scale*2
        self.delta_scale = (self.max_scale - self.scale) / 50
        self.delta_angle = randint(-5, 5)

    def update(self):
        # Rotate the ship
        self.angle += self.delta_angle
        self.scale += self.delta_scale
        self.center_x += self.delta_x

        # Grow then shrink
        if self.scale > self.max_scale:
            self.delta_scale *= -1
        elif self.scale <= 0:
            self.kill()


###############################################################################
class MyGame(arcade.Window):
    def __init__(self, width, height, title, vsync=False):
        super().__init__(width, height, title, vsync)
        arcade.set_background_color(arcade.color.BLACK)

        self.meteor_list = None
        self.ship_list = None
        self.pilot_list = None
        self.perf_graph_list = None
        self.meteor_types = [RotatingMeteor, NoRotationMeteor, CircleMeteor]
        self.meteor_type = 0
        print(self.meteor_types[self.meteor_type])

    def setup(self):
        self.meteor_list = arcade.SpriteList()
        self.ship_list = arcade.SpriteList()
        self.pilot_list = arcade.SpriteList()
        self.previous_meteor_time = time()
        self.previous_ship_time = time()

        # Create a sprite list and put the FPS performance graph into it
        self.perf_graph_list = arcade.SpriteList()
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS")
        graph.center_x = SCREEN_WIDTH / 2
        graph.top = SCREEN_HEIGHT - 10
        self.perf_graph_list.append(graph)

    def on_draw(self):
        """ Draw meteor field first.
            Then merge ships and pilots into one list, then sort by scale.
            This forces bigger/nearer ones to be drawn over far away ones.
            There's probably a better way to do this! """

        if not TRIPPY_MODE:
            self.clear()
        self.meteor_list.draw()

        all_sprites = arcade.SpriteList()
        all_sprites.extend(self.ship_list)
        all_sprites.extend(self.pilot_list)
        all_sprites.sort(key=lambda s: s.scale)
        all_sprites.draw()

        # Draw the performance graph(s)
        if PERFORMANCE_METRICS:
            self.perf_graph_list.draw()

    def on_update(self, delta_time):
        """ Update sprite positions.
            Create new meteors and ships at regular intervals.
            Check for keyboard and mouse input. """

        self.meteor_list.update()
        self.ship_list.update()
        self.pilot_list.update()

        t = time()
        # Produce METEORS_TO_ADD new meteor every METEOR_FREQUENCY_SECONDS
        # if existing number of meteors is within MAX_METEORS.
        # The type of meteor added is based on the current meteor_type.
        if t > self.previous_meteor_time + METEOR_FREQUENCY_SECONDS:
            self.previous_meteor_time = t
            if len(self.meteor_list) < MAX_METEORS:
                for _ in range(METEORS_TO_ADD):
                    meteor_class = self.meteor_types[self.meteor_type]
                    self.meteor_list.append(meteor_class())

        # Produce a new ship every SHIP_FREQUENCY_SECONDS
        if t > self.previous_ship_time + SHIP_FREQUENCY_SECONDS:
            self.previous_ship_time = t
            self.ship_list.append(Ship())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # Quit.
            arcade.exit()

        elif key == arcade.key.F1:
            # Show number of active sprites.
            arcade.print_timings()
            print(f"Meteors: {len(self.meteor_list)} "
                  f"Ships: {len(self.ship_list)} "
                  f"Pilots: {len(self.pilot_list)}")

        elif key == arcade.key.SPACE:
            # Eject a pilot from a random ship.
            ship = choice(self.ship_list)
            self.eject_pilot_from_ship(ship)

        elif key == arcade.key.BACKSPACE:
            # Eject all the pilots!
            for ship in self.ship_list:
                self.eject_pilot_from_ship(ship)

        elif key == arcade.key.T:
            # Toggle Trippy Mode
            global TRIPPY_MODE
            TRIPPY_MODE = not TRIPPY_MODE

        elif key == arcade.key.P:
            # Toggle Performance Metrics
            global PERFORMANCE_METRICS
            PERFORMANCE_METRICS = not PERFORMANCE_METRICS

        elif key == arcade.key.F2:
            # Toggle Meteor type
            self.meteor_type += 1
            if self.meteor_type >= len(self.meteor_types):
                self.meteor_type = 0
            print(self.meteor_types[self.meteor_type])

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Eject the pilot from the ships being clicked on. """
        ships = arcade.get_sprites_at_point((x, y), self.ship_list)
        for ship in ships:
            self.eject_pilot_from_ship(ship)

    def eject_pilot_from_ship(self, ship: Ship):
        """ Create a pilot at the ships location, and set ship tumbling.
            (Ignore ships that are already tumbling) """
        if not ship.tumbling:
            ship.tumble()
            new_pilot = EjectedPilot(ship.center_x, ship.center_y,
                                     ship.scale, ship.delta_x/2)
            self.pilot_list.append(new_pilot)


def main():
    arcade.enable_timings()  # required for performance metrics.
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, VSYNC)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
