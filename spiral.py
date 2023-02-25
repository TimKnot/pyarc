"""
Spiral: Maths stuff
Usage:
    ESC - Quit
"""


# from random import choice
from math import sin, cos, pi
from random import randint
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Spirtal"


###############################################################################
class Arc:
    def __init__(self, x, y, width=10, angle=0):
        self.x = x
        self.y = y
        self.width = width
        self.previous_width = 0
        self.start_angle = angle
        self.end_angle = angle + 90

    def update(self):
        self.move(self.end_angle+90, self.previous_width)
        new_width = self.width + self.previous_width
        self.previous_width = self.width
        self.width = new_width

    def move(self, angle, distance):
        self.x += round(distance * cos(angle*pi/180))
        self.y += round(distance * sin(angle*pi/180))

    def draw(self, colour):
        # arcade.draw_arc_filled(self.x, self.y, self.width*2, self.width*2,
        #                        colour, self.start_angle, self.end_angle)
        arcade.draw_arc_outline(self.x, self.y, self.width*2, self.width*2,
                                colour, self.start_angle, self.end_angle, 5)
        self.start_angle += 90
        self.end_angle += 90


class Spiral:
    def __init__(self, x, y, width=2, angle=0, steps=10):
        self.arc = Arc(x, y, width, angle)
        r = randint(100, 255)
        g = randint(100, 255)
        b = randint(100, 255)
        self.colour = (r, g, b)
        self.steps = steps

    def draw(self):
        for _ in range(self.steps):
            self.arc.draw(self.colour)
            self.arc.update()


###############################################################################
class MainWindow(arcade.Window):
    def __init__(self, width, height, title, vsync=False):
        super().__init__(width, height, title, vsync)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.start_angle = 359

    def on_draw(self):
        self.clear()
        a = Arc(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 2, self.start_angle)
        x = Arc(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2, 2, self.start_angle)
        r = randint(100, 255)
        g = randint(100, 255)
        b = randint(100, 255)

        z = Spiral(SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2, 2, self.start_angle, 14)
        z.draw()

        for _ in range(14):
            a.draw((r, g, b))
            a.update()
            x.draw((r, g, b))
            x.update()

    def on_update(self, delta_time):
        self.start_angle -= 5
        if self.start_angle < 0:
            self.start_angle = 359

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()


if __name__ == "__main__":
    window = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
