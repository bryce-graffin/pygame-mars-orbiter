"""
This module contains the `Planet` class and methods.

Author: Bryce Graffin
Date: 09 November 2025
"""
# region === IMPORTS ===
# generic imports
import math
import typing
import pygame as pg

# module imports
from src.utils.color_table import colors

if typing.TYPE_CHECKING:  # to avoid circular import issues
    from src.satellite import Satellite
# endregion

class Planet(pg.sprite.Sprite):
    """
    Planet object that the satellite orbits around.
    """

    def __init__(self):
        super().__init__()

        # load and convert the planet image and convert it to usable format upon init
        self.image_mars_pixel = pg.image.load(r'src\assets\sprites\mars_north_pole_3d_pixelated.png').convert()
        self.image_mars_real = pg.image.load(r'src\assets\sprites\mars_north_pole_3d_realistic.png').convert()
        self.image_copy = pg.transform.scale(self.image_mars_pixel, (100, 100))  # scale down for game window
        self.image_copy.set_colorkey(colors['BLACK'])
        self.rect = self.image_copy.get_rect()
        self.image = self.image_copy  # set the default image to pixelated version

        # set the initial attributes of the planet
        self.mass = 2000  # arbitrary mass value for gravity calcs relative to the small satellite mass

        # this x and y positions will center relative to the game window (windowed)
        # Potential Future Improvement: make this dynamic based on the screen size (windowed or fullscreen, adj by user)
        self.x = 400
        self.y = 320
        self.rect.center = (self.x, self.y)  # center the planet in the game window
        self.angle = math.degrees(0)  # initial angle for rotation animation
        self.rotate_by = math.degrees(0.01)  # essentially the rotation speed of the planet, not too high to avoid pops

    # region === MOVEMENT HANDLING METHODS ===

    def rotate(self):
        """
        Rotate the planet image with each game loop iteration.

        Note: similar to `Satellite.rotate()`
        """
        last_center = self.rect.center  # store the last center position
        self.image = pg.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = last_center  # reset to last center position
        self.angle += self.rotate_by

    # endregion

    # region === PHYSICS HANDLING METHODS ===

    def gravity(self, satellite: 'Satellite'):
        """
        Calculates the impact of gravity from `Planet` onto `Satellite`.
        """
        G = 1.0  # graviational constant, arbitrary value for game balance, consider real value in future versions
        dist_x = self.x - satellite.x
        dist_y = self.y - satellite.y
        distance = math.hypot(dist_x, dist_y)

        # normalize x and y coords to a unit vector 
        dist_x /= distance
        dist_y /= distance

        # apply gravity (dx & dy represent pixels/frame, so this is a simplification of real physics)
        force = (satellite.mass * self.mass) / (math.pow(distance, 2)) * G  # Newton's gravitational force formula

        # calculate acceleration changes in each step by multiplying force by the normalized distances
        satellite.dx += force * dist_x
        satellite.dy += force * dist_y

    # endregion

    def update(self):
        """
        Updates the `Planet` object in the game loop (i.e. rotate it).
        """
        self.rotate()  # rotate the planet each frame
