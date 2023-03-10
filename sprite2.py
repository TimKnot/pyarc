"""
Sprite2: An experiment with sprite scaling, sorting and mouse actions.
Usage:
    Left mouse button - Click on ship to eject the pilots.
    Space - Eject from a random ship.
    Backspace - Eject all the pilots.
    P - Performance Metrics toggle.
    F1 - Debug info. Show how many sprites are active and FPS.
    ESC - Quit
"""

from time import time
from random import uniform, randint, choice
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite2: Scaling and sorting"

VSYNC = False
TRIPPY_MODE = False

METEOR_FREQUENCY_SECONDS = 0.1
MAX_METEORS = 1000
METEORS_TO_ADD = 30

SHIP_FREQUENCY_SECONDS = 0.3
SHIPS_TO_ADD = 3
MAX_SHIPS = 100

EJECTED_PILOTS_TO_ADD = 4
MAX_EJECTED_PILOTS = 1000

PERFORMANCE_METRICS = False
GRAPH_WIDTH = int(SCREEN_WIDTH/2)
GRAPH_HEIGHT = 200


###############################################################################
class Meteor(arcade.SpriteCircle):
    """ Move a meteor across screen right to left.
        Larger ones are faster, to give a sense of depth. """

    def __init__(self):
        # Call the parent init (and pick a random image from the list)
        super().__init__(radius=randint(1, 6),
                         color=(100, 100, 100))

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
class Ship(arcade.Sprite):
    """ Move a random ship across the screen left to right.
        Larger ones are faster, to give a sense of depth. """

    count = 0  # Keep track of the number of ships in action.
    image_list = [
        "space_shooter/playerShip1_blue.png",
        "space_shooter/playerShip1_green.png",
        "space_shooter/playerShip1_orange.png",
        "space_shooter/playerShip2_orange.png",
        "space_shooter/playerShip3_orange.png",
    ]

    def __init__(self):
        # Call the parent init (and pick a random image from the list)
        file = f":resources:/images/{choice(self.image_list)}"
        super().__init__(filename=file,
                         scale=uniform(0.1, 1.0))

        Ship.count += 1
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
            Ship.count -= 1
            self.kill()

    def tumble(self):
        """ Set the ship to tumble and 'fall' """
        self.delta_angle = randint(-5, +5)
        self.delta_scale = -0.005
        self.tumbling = True


###############################################################################
class EjectedPilot(arcade.Sprite):
    """ A spinning creature that grows then shrinks. """

    count = 0  # Keep track of the number of pilots in flight.
    image_list = [
        "enemies/slimeBlock.png",
        "enemies/wormPink.png",
        "animated_characters/female_adventurer/femaleAdventurer_jump.png",
        "animated_characters/male_adventurer/maleAdventurer_fall.png",
        "animated_characters/robot/robot_fall.png",
        "animated_characters/zombie/zombie_idle.png",
    ]

    def __init__(self, x, y, scale, delta_x=0, delta_y=0):
        file = f":resources:/images/{choice(EjectedPilot.image_list)}"
        super().__init__(filename=file, scale=scale)
        EjectedPilot.count += 1
        self.center_x = x
        self.center_y = y
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.angle = randint(0, 359)
        self.max_scale = self.scale*2
        self.delta_scale = (self.max_scale - self.scale) / 50
        self.delta_angle = randint(-5, 5)

    def update(self):
        # Rotate the ship
        self.angle += self.delta_angle
        self.scale += self.delta_scale
        self.center_x += self.delta_x
        self.center_y += self.delta_y

        # Grow then shrink
        if self.scale > self.max_scale:
            self.delta_scale *= -1
        elif self.scale <= 0:
            EjectedPilot.count -= 1
            self.kill()


###############################################################################
class MyGame(arcade.Window):
    def __init__(self, width, height, title, vsync=False):
        super().__init__(width, height, title, vsync)
        arcade.set_background_color(arcade.color.BLACK)
        arcade.enable_timings()  # required for performance metrics.

        self.meteor_list = None
        self.ship_list = None  # Can also contain EjectedPilots
        self.perf_graph_list = None

    def setup(self):
        self.meteor_list = arcade.SpriteList()
        self.ship_list = arcade.SpriteList()
        self.previous_meteor_time = time()
        self.previous_ship_time = time()

        # Create a sprite list and put the FPS performance graph into it
        self.perf_graph_list = arcade.SpriteList()
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS")
        graph.center_x = SCREEN_WIDTH / 2
        graph.top = SCREEN_HEIGHT - 10
        self.perf_graph_list.append(graph)

    def on_draw(self):
        """ Draw all sprites and performance metrics.
            Sort ships (and pilots) list into scale order to give
            impression of depth. """

        if not TRIPPY_MODE:
            self.clear()

        self.meteor_list.draw()
        self.ship_list.sort(key=lambda s: s.scale)
        self.ship_list.draw()

        if PERFORMANCE_METRICS:
            self.perf_graph_list.draw()

    def on_update(self, delta_time):
        """ Update sprite positions.
            Create new meteors and ships at regular intervals.
            Check for keyboard and mouse input. """

        self.meteor_list.update()
        self.ship_list.update()

        t = time()
        # Produce METEORS_TO_ADD new meteor every METEOR_FREQUENCY_SECONDS
        # but only if existing number of meteors is within MAX_METEORS.
        if t > self.previous_meteor_time + METEOR_FREQUENCY_SECONDS:
            self.previous_meteor_time = t
            if len(self.meteor_list) < MAX_METEORS:
                for _ in range(METEORS_TO_ADD):
                    self.meteor_list.append(Meteor())

        # Produce SHIPS_TO_ADD new ship every SHIP_FREQUENCY_SECONDS
        # but only if existing number of ships is within MAX_SHIPS.
        if t > self.previous_ship_time + SHIP_FREQUENCY_SECONDS:
            self.previous_ship_time = t
            if Ship.count < MAX_SHIPS:
                for _ in range(SHIPS_TO_ADD):
                    self.ship_list.append(Ship())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # Quit.
            arcade.exit()

        elif key == arcade.key.F1:
            # Show number of active sprites.
            print(f"Meteors {len(self.meteor_list):4} "
                  f" | Ships {Ship.count:4} "
                  f" | Pilots {EjectedPilot.count:4} "
                  f" | FPS {arcade.get_fps(60):3.1f}")

        elif key == arcade.key.SPACE:
            # Eject a pilot from a random ship.
            ship = choice(self.ship_list)
            self.eject_pilot_from_ship(ship)

        elif key == arcade.key.BACKSPACE:
            # Eject all the pilots!
            for ship in self.ship_list:
                self.eject_pilot_from_ship(ship)

        elif key == arcade.key.P:
            # Toggle Performance Metrics
            global PERFORMANCE_METRICS
            PERFORMANCE_METRICS = not PERFORMANCE_METRICS

        elif key == arcade.key.T:
            # Toggle Trippy Mode
            global TRIPPY_MODE
            TRIPPY_MODE = not TRIPPY_MODE

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Eject the pilot from the ships being clicked on. """
        ships = arcade.get_sprites_at_point((x, y), self.ship_list)
        for ship in ships:
            self.eject_pilot_from_ship(ship)

    def eject_pilot_from_ship(self, ship: Ship):
        """ Create a pilot at the ships location, and set ship tumbling.
            Ignore ships that are already tumbling. """

        # Is this object actually a ship (and not a pilot)?
        if type(ship) == Ship and not ship.tumbling:
            ship.tumble()
            if EjectedPilot.count < MAX_EJECTED_PILOTS:
                for _ in range(EJECTED_PILOTS_TO_ADD):
                    self.ship_list.append(
                        EjectedPilot(ship.center_x, ship.center_y,
                                     ship.scale,
                                     ship.delta_x/2, randint(-5, 5)))


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, VSYNC)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
