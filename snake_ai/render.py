from typing import TYPE_CHECKING

import pygame

from snake_ai.constants import WHITE, MAP_SIZE_Y, MAP_SIZE_X, TileNames, BLACK, BLOCK_SIZE, BLUE1, BLUE2, RED, font, \
    WIDTH, HEIGHT
from . import config

if TYPE_CHECKING:
    from snake_ai.game import SnakeGameAI


class Render:
    def __init__(self):
        self.w = WIDTH
        self.h = HEIGHT

        self.display = pygame.display.set_mode((self.w, self.h))

        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

    def update_ui(self, snake: 'SnakeGameAI'):
        if config['render_ui']:
            self.display.fill(WHITE)

            for y in range(MAP_SIZE_Y):
                for x in range(MAP_SIZE_X):
                    if snake.map_array[y * MAP_SIZE_X + x] == TileNames.Border:
                        pygame.draw.rect(self.display, BLACK,
                                         pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    elif snake.map_array[y * MAP_SIZE_X + x] == TileNames.Floor:
                        pygame.draw.rect(self.display, WHITE,
                                         pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            for pt in snake.snake[1:]:
                pygame.draw.rect(self.display, BLUE1,
                                 pygame.Rect(pt.x * BLOCK_SIZE, pt.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2,
                             pygame.Rect(snake.snake[0].x * BLOCK_SIZE, snake.snake[0].y * BLOCK_SIZE, BLOCK_SIZE,
                                         BLOCK_SIZE))

            pygame.draw.rect(self.display, RED,
                             pygame.Rect(snake.food.x * BLOCK_SIZE, snake.food.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            text = font.render("Score: " + str(snake.score), True, BLACK)
            self.display.blit(text, [0, 300])

        pygame.display.flip()
