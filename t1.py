"""
Based on arcade.examples.sprite_move_angle
"""

import math
from random import random, randint, choice
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Zoomers and Spinners"

MOVEMENT_SPEED = 5
ANGLE_SPEED = 5

timer = 0
TIMER_SIZE = 10


class Zoomer(arcade.Sprite):
    """ Zooms across the screen """

    def __init__(self, image, scale, x, y, speed=0, angle=0, change_angle=0):

        # Call the parent init
        super().__init__(image, scale)

        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.angle = angle
        self.change_angle = change_angle

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        if self.right < 0 or self.left > SCREEN_WIDTH:
            self.kill()
        elif self.top < 0 or self.bottom > SCREEN_HEIGHT:
            self.kill()


class Spinner(arcade.Sprite):
    """ A growy/shrinky spinny thing """

    image_list = [
        ":resources:images/alien/alienBlue_front.png",
        ":resources:/images/enemies/bee.png",
        ":resources:/images/enemies/saw.png",
        ":resources:/images/enemies/slimeBlock.png",
        ":resources:/images/enemies/wormPink.png",
    ]

    def __init__(self, x, y, scale_delta=0.1, max_scale=1, change_angle=0):

        # Call the parent init (and pick a random image from the list)
        super().__init__(choice(self.image_list), 0.1)

        self.center_x = x
        self.center_y = y
        self.angle = randint(0, 359)
        self.scale_delta = scale_delta
        self.max_scale = max_scale
        self.change_angle = change_angle

    def update(self):
        # Rotate the ship
        self.angle += self.change_angle
        self.scale += self.scale_delta

        # Grow then shrink
        if self.scale > self.max_scale:
            self.scale_delta *= -1
        elif self.scale <= 0:
            self.kill()


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.sprite_list = None
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.sprite_list = arcade.SpriteList()

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()

    def on_update(self, delta_time):
        global timer
        self.sprite_list.update()

        timer += 1
        if timer >= TIMER_SIZE:
            # Create some new things
            timer = 0
            self.sprite_list.append(Zoomer(
                ":resources:images/space_shooter/playerShip1_orange.png",
                random()+0.2,
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                random()*4+1, randint(0, 359), random()-0.5))

            self.sprite_list.append(Spinner(
                randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT),
                random()/8+0.01,
                random()*2+0.5,
                randint(1, 10)
            ))

            # For debugging, keep an eye on how many objects we're creating.
            print(len(self.sprite_list))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # Quit
            arcade.exit()


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
