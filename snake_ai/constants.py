# constants.py
from dataclasses import dataclass

import pygame
from enum import Enum
from collections import namedtuple

# Constants and enums here
pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# AI
HIDDEN_LAYER = 6_000
MAX_MEMORY = 200_000
BATCH_SIZE = 18
LR = 0.04  # learning rate
GAMMA = 0.015  # discount rate

# GAME
GAME_CLOCK_HITS = 2000
Direction = Enum('Direction', 'RIGHT LEFT UP DOWN')
Point = namedtuple('Point', 'x, y')

# MAP
BLOCK_SIZE = 20

WIDTH, HEIGHT = 640, 480
MAP_SIZE_X = int(20)
MAP_SIZE_Y = int(12)
MAP_SIZE = MAP_SIZE_X * MAP_SIZE_Y

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 150, 255)
BLACK = (0, 0, 0)


@dataclass(
    frozen=True
)
class TileNames:
    Floor = 0
    Border = 1
    Snake = 2
    Head = 3
    Food = 4
