import math
import queue
import random
from collections import deque

import numpy as np
import pygame
from numpy import sqrt

from snake_ai.constants import TileNames, BLOCK_SIZE, Direction, Point, RED, WHITE, font, BLUE1, BLACK, SPEED, \
    WIDTH, HEIGHT, MAPSIZEX, MAPSIZEY


def calc_direction_change_cost(move_cost):
    if not deque:
        return 0

    if deque[0] != deque[1]:
        return move_cost

    return 0


class SnakeGameAI:
    def __init__(self):  # dimensions
        self.map_array = [TileNames.Floor] * (MAPSIZEX * MAPSIZEY)
        for y in range(MAPSIZEY):
            for x in range(MAPSIZEX):
                if x == 0 or y == 0 or y == MAPSIZEY - 1 or x == MAPSIZEX - 1:
                    self.map_array[y * MAPSIZEX + x] = TileNames.Border

        self.w = WIDTH
        self.h = HEIGHT
        self.display = pygame.display.set_mode((self.w, self.h))

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
            if 1 <= pt.x < MAPSIZEX - 1 and 1 <= pt.y < MAPSIZEY - 1:
                map_array[int((1 + pt.y) * MAPSIZEX + (1 + pt.x))] = TileNames.Snake

        if 1 <= self.snake[0].x < MAPSIZEX - 1 and 1 <= self.snake[0].y < MAPSIZEY - 1:
            map_array[int((1 + self.snake[0].y) * MAPSIZEX + (1 + self.snake[0].x))] = TileNames.Head

        if 1 <= self.food.x < MAPSIZEX - 1 and 1 <= self.food.y < MAPSIZEY - 1:
            map_array[int((1 + self.food.y) * MAPSIZEX + (1 + self.food.x))] = TileNames.Food

        return map_array

    def reset(self):  # game state
        self.direction = Direction.RIGHT
        self.head = Point(MAPSIZEX / 2, MAPSIZEY / 2)
        self.snake = [self.head,
                      Point(self.head.x - 1, self.head.y),
                      Point(self.head.x - 2, self.head.y)]
        self.score = 0
        self.lastDist = 0.0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.moves_since_last_food = 0

    def _place_food(self):
        x = random.randint(1, MAPSIZEX - 2)
        y = random.randint(1, MAPSIZEY - 2)
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
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = self.calc_distance_to_food_after_death_reward()
            return reward, game_over, self.score
        if self.head == self.food:
            self.score += 1
            reward = 40 + 5 * self.score
            self._place_food()
            self.moves_since_last_food = 0
        else:
            self.moves_since_last_food += 1
            reward = self.calc_reward()
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    def calc_reward(self):
        move_cost = 0.1
        not_dead_reward = 0.5
        current_not_dead_reward = not_dead_reward - (self.moves_since_last_food / 20 * len(self.snake))
        if current_not_dead_reward < 0:
            current_not_dead_reward = 0

        d_distance_reward = self.calc_d_distance_reward() * 10
        same_action_reward = self.calc_reward_for_same_action()

        reward = d_distance_reward
        reward += current_not_dead_reward
        reward += same_action_reward
        reward -= calc_direction_change_cost(move_cost)

        #print(reward)

        return reward ** 2

    def calc_distance_to_food_after_death_reward(self):
        max_distance = 23

        head = self.head
        food = self.food

        current_distance = sqrt((food.x - head.x) ** 2 + (food.y - head.y) ** 2)
        current_distance = float(abs(current_distance))

        if current_distance > 18.0:
            return -10
        elif 12.0 < current_distance <= 18.0:
            return -5
        elif 6.0 < current_distance <= 12.0:
            return 0
        elif 6.0 < current_distance <= 2.5:
            return 1
        elif 2.5 < current_distance <= 1.5:
            return 10
        else:
            return 20

    def calc_d_distance_reward(self):
        max_distance = 23
        reward_per_distance = 0.1
        head = self.head
        food = self.food
        snake_len = len(self.snake)

        current_distance = abs(sqrt((food.x - head.x) ** 2 + (food.y - head.y) ** 2))
        d_distance = current_distance - self.lastDist

        d_distance_reward_per_unit = 1

        # if snake_len > 5:
        #     d_distance_reward_per_unit = reward_per_distance / (snake_len - 5)
        # else:
        #     d_distance_reward_per_unit = reward_per_distance

        if d_distance <= 0:
            d_distance_reward = -1
        else:
            d_distance_reward = 1

        # d_distance_reward = d_distance * d_distance_reward_per_unit
        #
        # if d_distance_reward < 0:
        #     d_distance_reward = 0

        self.lastDist = current_distance

        return d_distance_reward

    def all_same_elements(self, deque):
        # If the deque is empty, return False
        if not deque:
            return False

        # Get the first element
        first_element = deque[0]

        # Check if all elements are the same as the first element
        for element in deque:
            if element != first_element:
                return False

        return True

    def calc_reward_for_same_action(self):
        if self.all_same_elements(self.memory_queue):
            return -2.0

        return 0

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x == 0 or pt.x == MAPSIZEX - 1 or pt.y == MAPSIZEY - 1 or pt.y == 0:
            return True
        if pt in self.snake[1:-1]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(WHITE)

        for y in range(MAPSIZEY):
            for x in range(MAPSIZEX):
                if self.map_array[y * MAPSIZEX + x] == TileNames.Border:
                    pygame.draw.rect(self.display, BLACK,
                                     pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                elif self.map_array[y * MAPSIZEX + x] == TileNames.Floor:
                    pygame.draw.rect(self.display, WHITE,
                                     pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1,
                             pygame.Rect(pt.x * BLOCK_SIZE, pt.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED,
                         pygame.Rect(self.food.x * BLOCK_SIZE, self.food.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, BLACK)
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
            x += 1
        elif self.direction == Direction.LEFT:
            x -= 1
        elif self.direction == Direction.DOWN:
            y += 1
        elif self.direction == Direction.UP:
            y -= 1

        self.head = Point(x, y)

        self.memory_queue.append(self.direction)
