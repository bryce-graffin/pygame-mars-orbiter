"""
This module contains the `Satellite` class and methods.

Author: Bryce Graffin
Date: 08 November 2025
"""
# region === IMPORTS ===
# generic imports
import random  # for handling starting locations of the satellite sprite
import math  # for calculating distance and heading
import pygame as pg  # for running the game

# module imports
from src.utils.color_table import colors
from src.planet import Planet

# endregion

class Satellite(pg.sprite.Sprite):
    """
    Satellite object that orbits the planet(s) and is controller by the player.
    """

    def __init__(self, background):
        super().__init__()

        self.background = background  # this is passed in and will be used to draw the satellite's path

        # load and convert both satellite state images (alive/crashed) and convert them to usable format upon init
        self.image_sat = pg.image.load(r"src\assets\sprites\satellite.png").convert()
        self.image_crash = pg.image.load(r"src\assets\sprites\satellite_crashed.png").convert()
        self.image = self.image_sat  # create ref
        self.image.set_colorkey(colors['BLACK'])

        # region === SETTING INITIAL POSITION, SPEED, FUEL, & SOUND ATTRIBUTES ===

        # set starting coords using random ranges
        self.x = random.randrange(315, 425)
        self.y = random.randrange(70, 180)

        # create the rectangle attribute of the Satellite sprite, use the black parts to remove the background
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)  # sets the starting position of the sprite

        # set starting velocity
        self.dx = random.choice([-3, 3])  # negative values result in counterclockwise orbit
        self.dy = 0  # this is handled by gravity

        # set heading (dish orientation), fuel, mass, and distance to the planet
        self.heading = 0
        self.fuel = 100
        self.fuel_adjustment_factor = 2  # how much fuel is consumed per thruster firing, great for varying difficulty
        self.mass = 1
        self.distance = 0

        # set starting sound attributes
        self.thrust = pg.mixer.Sound(r'src\assets\sounds\thrust_audio.ogg')
        self.thrust.set_volume(0.07)  # valid values are 0-1

        # endregion

    # region === MOVEMENT HANDLING METHODS ===

    def check_keys(self):
        """
        Listens for user to input key presses and calls the `thruster()` method.
        """
        keys = pg.key.get_pressed()  # get the current state of all keyboard buttons

        if keys[pg.K_LEFT]:  # decrease Dx
            self.thruster('LEFT')
        if keys[pg.K_RIGHT]:  # increase Dx
            self.thruster('RIGHT')
        if keys[pg.K_UP]:  # decrease Dy
            self.thruster('UP')
        if keys[pg.K_DOWN]:  # increase Dy
            self.thruster('DOWN')

    def thruster(self, direction: str):
        """
        Updates the satellites velocity components. Receives the user input and adds/subtracts from dx, dy, and fuel
        accordingly.

        :param direction: A string representing which thruster direction was fired by the user.
        :type direction: str
        """
        if self.fuel > 0:  # only allow thruster firing if there is fuel
            # x-coordinate system is standard, so increasing x moves right on the screen
            if direction == 'LEFT':
                self.dx -= 0.05
            elif direction == 'RIGHT':
                self.dx += 0.05
            # y-coordinate system is inverted in pygame, so decreasing y moves up the screen
            elif direction == 'UP':
                self.dy -= 0.05
            elif direction == 'DOWN':
                self.dy += 0.05

            self.fuel -= self.fuel_adjustment_factor  # decrease fuel by 1 unit per thruster firing
            self.thrust.play()  # play the thruster sound effect

    def locate(self, planet: Planet):
        """
        Calculates the distance of the `Satellite` object from the `Planet` object and determines heading for pointing
        the radar dish towards the planet at all times.

        :param planet: Planet object that the satellite is orbiting.
        :type planet: Planet
        """
        px, py = planet.rect.center  # get the center coords of the planet
        dist_x = self.x - px  # horizontal distance from planet center
        dist_y = self.y - py  # vertical distance from planet center

        # get direction to planet to find heading and distance
        direction_to_planet_radians = math.atan2(dist_x, dist_y)  # convert to radians because pygame uses degrees
        self.heading = direction_to_planet_radians * (180 / math.pi)  # convert to degrees for heading
        self.heading -= 90  # adjust because the sprite is flipped (flying tail-first)
        self.distance = math.hypot(dist_x, dist_y)  # calculate Euclidian, straight-line distance to planet center
       
    def rotate(self):
        """
        Rotates `Satellite` (using degrees for `pygame`) so the radar dish faces the planet's center.

        Note: similar to `Planet.rotate()`

        ### Potential Future Improvement:
        - Consider factoring in a system (in harder game-modes) where the player needs to purchase real-world elements
        like a flywheel or reaction wheels to automatically orient the dish towards the planet - otherwise the satellite
        will face in the same direction and the player will need to manually rotate it or wait for the planet to rotate
        as it orbits, decreasing time and therefore score.
        """
        self.image = pg.transform.rotate(self.image_sat, self.heading)  # rotate the satellite image
        self.rect = self.image.get_rect()

    def path(self):
        """
        Draws the path of the `Satellite` as it orbits and updates after receiving input that updates it's position and
        movement.
        """
        # update position and draw line to trace the satellite's orbital path
        last_center = (self.x, self.y)  # store last-known position before updating
        self.x += self.dx  # update x coord
        self.y += self.dy  # update y coord
        pg.draw.line(
            surface=self.background,
            color=colors['WHITE'],
            start_pos=last_center,
            end_pos=(self.x, self.y),
            width=2  # TODO: update this after testing for different line thicknesses
        )

    # endregion

    def update(self):
        """
        Updates the `Satellite` object in the game loop.
        """
        self.check_keys()  # check for user input
        self.rotate()  # rotate the satellite to face the planet
        self.path()  # draw path
        self.rect.center = (self.x, self.y)  # update the rectangle position

        # change image to crashed (red) if entering the Planet's atmoshphere
        if self.dx == 0 and self.dy == 0:
            self.image = self.image_crash
            self.image.set_colorkey(colors['BLACK'])
