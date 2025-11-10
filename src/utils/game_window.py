"""
Module containing utility functions for elements related to the game window seen by the player.
"""
# region === IMPORTS ===
# generic imports
import pygame as pg

# module imports
from src.utils.color_table import colors
from src.planet import Planet

# endregion

# region === LABEL FUNCTIONS ===

def instructions_label(screen: pg.Surface, text: list, color: tuple, x: int, y: int):
    """
    Render and display instruction labels on the game window.

    :param screen: The game window surface where the labels will be drawn.
    :type screen: pygame.Surface
    :param text: List of strings representing the lines of text to display.
    :type text: list
    :param color: Color of the text.
    :type color: tuple
    :param x: X-coordinate for the top-left corner of the text block.
    :type x: int
    :param y: Y-coordinate for the top-left corner of the text block.
    :type y: int
    """
    font = pg.font.SysFont(None, 25)  # default font, size 25 pt
    line_spacing = 22  # space between lines
    for index, line in enumerate(text):
        label = font.render(text=line, antialias=True, color=color, background=colors['BLACK'])
        screen.blit(label, (x, y + index * line_spacing))

def box_label(screen: pg.Surface, text: str, dimensions: tuple):
    """
    Make fixed-size label from screen, text and left, top, width, height.

    :param screen: The game window surface where the label will be drawn.
    :type screen: pg.Surface
    :param text: List of strings representing the lines of text to display.
    :type text: str
    :param dimensions: Left, top, width, height of the label
    :type dimensions: tuple
    """
    readout_font = pg.font.SysFont(None, 27) # default font, size 27 pt
    base = pg.Rect(dimensions)  # left, top, width, height
    pg.draw.rect(surface=screen, color=colors['WHITE'], rect=base, width=0)
    label = readout_font.render(text=text, antialias=True, color=colors['BLACK'])
    label_rect = label.get_rect(center=base.center)
    screen.blit(label, label_rect)

# endregion

# region === GAMEPLAY VISUALS FUNCTIONS ===

def satellite_mapping_on(planet: Planet):
    """
    Turn on the visuals for mapping the planet once win conditions have been met by the player and they press 'M'.

    Essentially, this changes the planet image to a more realistic version as if the planet has been scanned by
    the satellite.

    :param planet: Planet object.
    :type planet: Planet
    """
    last_center = planet.rect.center  # store last center position
    planet.image_copy = pg.transform.scale(planet.image_mars_real, (100, 100))
    planet.image_copy.set_colorkey(colors['BLACK'])
    planet.rect = planet.image_copy.get_rect()  # update rect for new image
    planet.rect.center = last_center  # reset to last center position

def satellite_mapping_off(planet: Planet):
    """
    Turn off the visuals for mapping the planet (i.e. restore original pixelated planet image.)

    :param planet: Planet object.
    :type planet: Planet
    """
    planet.image_copy = pg.transform.scale(planet.image_mars_pixel, (100, 100))  # scale down for game window
    planet.image_copy.set_colorkey(colors['BLACK'])

def cast_planet_shadow(screen: pg.Surface):
    """
    Add optional terminator & cast a shadow from 'behind' the planet to the edge of the screen.

    This simulates the idea that the Sun is shining onto the planet (and it is either the vernal/autumnal equinox.)

    :param screen: _description_
    :type screen: pg.Surface
    """
    shadow = pg.Surface((400, 100), flags=pg.SRCALPHA)  # tuple is width, height
    shadow.fill((0, 0, 0, 210))  # RGBA where A is alpha (opacity set to very dark, but not fully opaque)

    # potential future improvement: make shadow postion random for each new game instance to vary user experience
    screen.blit(shadow, (0, 270))  # position at top left coords

# endregion
