"""
This module is the main executable of the Mars Orbiter game.

Author: Bryce Graffin
Date: 08 November 2025
"""
import os  # for updating where the window will be located if the user decides to exit fullscreen mode
import math  # for handling math calculations
import random  # for handling starting locations of the satellite sprite
import pygame as pg  # for running the game


def main():
    """
    Set up labels and instructions, create objects, & run the game loop.
    """
    pg.init()  # initializes pygame

    # set up the display
    os.environ['SDL_VIDEO_WINDOWS_POS'] = '700, 100'  # set origin of the game window
    screen = pg.display.set_mode((800, 645), pg.FULLSCREEN)  # set to full screen