"""Emil is blöd"""
import random
import numpy as np
import pygame

from snake_ai.constants import TileNames, BLOCK_SIZE, Direction, Point, BLUE2, RED, WHITE, font, BLUE1, BLACK, SPEED, \
    WIDTH, HEIGHT, MAPSIZEX, MAPSIZEY


class SnakeGameAI:

    def __init__(self):  # dimensions
        self.map_array = [TileNames.Floor] * (MAPSIZEX * MAPSIZEY)
        self.direction = None
        self.head = None
        self.snake = None
        self.food = None
        self.score = None
        self.frame_iteration = None
        self.w = WIDTH
        self.h = HEIGHT
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    @property
    def map(self):
        map_array = [TileNames.Floor] * (MAPSIZEX * MAPSIZEY)

        for y in range(MAPSIZEY):
            for x in range(MAPSIZEX):
                if y == 0 or y == MAPSIZEY - 1 or x == 0 or x == MAPSIZEX - 1:
                    map_array[y * MAPSIZEX + x] = TileNames.Border

        # for i in range(len(self.snake)):
        #     y = int(self.snake[i].y / BLOCK_SIZE)
        #     x = int(self.snake[i].x / BLOCK_SIZE)  # Removed the +1 for now as it seemed an error in the previous code
        #     map_array[y * MAPSIZEX + x] = TileNames.Snake
        #
        # y = int(self.head.y / BLOCK_SIZE)
        # x = int(self.head.x / BLOCK_SIZE)  # Removed the +1 for now as it seemed an error in the previous code
        # map_array[y * MAPSIZEX + x] = TileNames.Head
        #
        # y = int(self.food.y / BLOCK_SIZE) + 1
        # x = int(self.food.x / BLOCK_SIZE) + 1  # Removed the +1 for now as it seemed an error in the previous code
        # map_array[y * MAPSIZEX + x] = TileNames.Food

        # for row in range(MAPSIZEY):
        #     for column in range(MAPSIZEX):
        #         print(map_array[row * MAPSIZEX + column], end=' ')  # Print the element with a space separator
        #
        # y = int(self.head.y / BLOCK_SIZE) + 1
        # x = int(self.head.x / BLOCK_SIZE) + 1 # Removed the +1 for now as it seemed an error in the previous code

        return map_array

    def reset(self):  # game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self._move(action)
        self.snake.insert(0, self.head)
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        if self.head == self.food:
            self.score += 1
            reward = 100
            self._place_food()
        else:
            self.snake.pop()
        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):  # straight
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):  # right turn
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:  # [0,0,1] aka left turn
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
