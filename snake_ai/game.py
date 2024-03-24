import random
from collections import deque

import numpy as np
import pygame

from snake_ai.constants import TileNames, BLOCK_SIZE, Direction, Point, RED, WHITE, font, BLUE1, BLACK, GAME_SPEED, \
    WIDTH, HEIGHT, MAP_SIZE_X, MAP_SIZE_Y, BLUE2, MAP_SIZE, RENDER_UI
from snake_ai.rewards.death_reward import calc_death_reward
from snake_ai.rewards.food_reward import calc_food_reward
from snake_ai.rewards.normal_reward import calc_normal_reward


class SnakeGameAI:
    def __init__(self):  # dimensions
        self.map_array = [TileNames.Floor] * MAP_SIZE
        for y in range(MAP_SIZE_Y):
            for x in range(MAP_SIZE_X):
                if x == 0 or y == 0 or y == MAP_SIZE_Y - 1 or x == MAP_SIZE_X - 1:
                    self.map_array[y * MAP_SIZE_X + x] = TileNames.Border

        self.w = WIDTH
        self.h = HEIGHT
        self.display = pygame.display.set_mode((self.w, self.h))
        self.goodMove = 0

        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.lastDist = 0.0
        self.moves_since_last_food = 0

        self.memory_queue = deque(maxlen=3)

        self.reset()

    @property
    def map(self):
        map_array = self.map_array.copy()

        for pt in self.snake:
            if 1 <= pt.x < MAP_SIZE_X - 1 and 1 <= pt.y < MAP_SIZE_Y - 1:
                map_array[int((1 + pt.y) * MAP_SIZE_X + (1 + pt.x))] = TileNames.Snake

        if 1 <= self.snake[0].x < MAP_SIZE_X - 1 and 1 <= self.snake[0].y < MAP_SIZE_Y - 1:
            map_array[int((1 + self.snake[0].y) * MAP_SIZE_X + (1 + self.snake[0].x))] = TileNames.Head

        if 1 <= self.food.x < MAP_SIZE_X - 1 and 1 <= self.food.y < MAP_SIZE_Y - 1:
            map_array[int((1 + self.food.y) * MAP_SIZE_X + (1 + self.food.x))] = TileNames.Food

        return map_array

    def reset(self):  # game state
        self.direction = Direction.RIGHT
        self.head = Point(MAP_SIZE_X / 2, MAP_SIZE_Y / 2)
        self.snake = [self.head,
                      Point(self.head.x - 1, self.head.y),
                      Point(self.head.x - 2, self.head.y)]
        self.score = 0
        self.lastDist = 0.0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.moves_since_last_food = 0
        self.goodMove = 0

    def _place_food(self):
        x = random.randint(1, MAP_SIZE_X - 2)
        y = random.randint(1, MAP_SIZE_Y - 2)
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

        game_over = False

        if self.is_collision():
            game_over = True
            reward = calc_death_reward(self, False)
            return reward, game_over, self.score
        if self.is_suicide():
            game_over = True
            reward = calc_death_reward(self, True)
            return reward, game_over, self.score
        if self.frame_iteration > 100 * len(self.snake):
            dead_look_reward = -500
            game_over = True
            reward = dead_look_reward
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = calc_food_reward(self)
            self._place_food()
            self.moves_since_last_food = 0

        else:
            self.moves_since_last_food += 1
            reward = calc_normal_reward(self)
            self.snake.pop()

        self._update_ui()
        self.clock.tick(GAME_SPEED)
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x == 0 or pt.x == MAP_SIZE_X - 1 or pt.y == MAP_SIZE_Y - 1 or pt.y == 0:
            return True

        return False

    def is_suicide(self, pt=None):
        if pt is None:
            pt = self.head
        if pt in self.snake[1:-1]:
            return True

        return False

    def _update_ui(self):
        if RENDER_UI:
            self.display.fill(WHITE)

            for y in range(MAP_SIZE_Y):
                for x in range(MAP_SIZE_X):
                    if self.map_array[y * MAP_SIZE_X + x] == TileNames.Border:
                        pygame.draw.rect(self.display, BLACK,
                                         pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    elif self.map_array[y * MAP_SIZE_X + x] == TileNames.Floor:
                        pygame.draw.rect(self.display, WHITE,
                                         pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            for pt in self.snake[1:]:
                pygame.draw.rect(self.display, BLUE1,
                                 pygame.Rect(pt.x * BLOCK_SIZE, pt.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2,
                             pygame.Rect(self.snake[0].x * BLOCK_SIZE, self.snake[0].y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            pygame.draw.rect(self.display, RED,
                             pygame.Rect(self.food.x * BLOCK_SIZE, self.food.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            text = font.render("Score: " + str(self.score), True, BLACK)
            self.display.blit(text, [0, 300])

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
            x += 1
        elif self.direction == Direction.LEFT:
            x -= 1
        elif self.direction == Direction.DOWN:
            y += 1
        elif self.direction == Direction.UP:
            y -= 1

        self.head = Point(x, y)

        self.memory_queue.append(self.direction)
