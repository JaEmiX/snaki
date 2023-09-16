# constants.py
from dataclasses import dataclass

import pygame
from enum import Enum
from collections import namedtuple

# Constants and enums here
pygame.init()
font = pygame.font.Font('arial.ttf', 25)

BLOCK_SIZE = 20

WIDTH, HEIGHT = 640, 480
MAPSIZEX = int(WIDTH / BLOCK_SIZE) + 2
MAPSIZEY = int(HEIGHT / BLOCK_SIZE) + 2

SPEED = 50

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

Direction = Enum('Direction', 'RIGHT LEFT UP DOWN')
Point = namedtuple('Point', 'x, y')


@dataclass(
    frozen=True
)
class TileNames:
    Floor = 2
    Border = 3
    Snake = 4
    Head = 5
    Food = 6