"""
Based on arcade.examples.sprite_move_angle
"""

import math
from random import random, randint
import arcade

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite by Angle Example"

MOVEMENT_SPEED = 5
ANGLE_SPEED = 5

timer = 0
TIMER_SIZE = 5


class Player(arcade.Sprite):
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


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.player_list = None
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.player_list = arcade.SpriteList()

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        global timer
        self.player_list.update()

        timer += 1
        if timer >= TIMER_SIZE:
            timer = 0
            self.player_list.append(Player(
                ":resources:images/space_shooter/playerShip1_orange.png",
                random()+0.2,
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                random()*4+1, randint(0, 359), random()-0.5))
            print(len(self.player_list))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            print(len(self.player_list))

    def on_key_release(self, key, modifiers):
        pass


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
