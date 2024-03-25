from collections import deque
from typing import TYPE_CHECKING

from snake_ai.constants import Direction
from snake_ai.rewards import calc_distance

if TYPE_CHECKING:
    from snake_ai.game import SnakeGameAI


def calc_normal_reward(snake: 'SnakeGameAI'):
    reward = 0

    not_dead_reward = calc_not_dead_reward(snake)
    reward += not_dead_reward

    d_distance_reward, d_distance = calc_d_distance_reward(snake)
    reward += d_distance_reward

    distance_reward = calc_distance_reward(snake, d_distance)
    reward += distance_reward

    cost_for_circle_action = calc_cost_for_circle_action(snake)
    reward -= cost_for_circle_action

    direction_change_cost = calc_direction_change_cost(snake)
    reward -= direction_change_cost

    movement_cost = calc_movement_cost(snake)
    reward -= movement_cost

    reenter_field_cost = calc_reenter_field_cost(snake)
    reward -= reenter_field_cost

    return reward


def calc_d_distance_reward(snake: 'SnakeGameAI'):
    snake_len = len(snake.snake)

    current_distance, lastDist = calc_distance(snake)
    d_distance = lastDist - current_distance

    if d_distance <= 0:
        d_distance_reward = -0.8 - (snake.moves_since_last_food / (snake_len * 10))
        snake.goodMove = 0
    else:
        d_distance_reward = 2.2 - (snake.moves_since_last_food / (snake_len * 20))
        snake.goodMove = 1
        if d_distance_reward < 0.2:
            d_distance_reward = 0.2

    return d_distance_reward, d_distance


def calc_distance_reward(snake: 'SnakeGameAI', d_distance: float):
    distance_reward = 0

    if len(snake.snake) > 7:
        return distance_reward

    current_distance = calc_distance(snake)[0]

    if d_distance < 0:
        if current_distance > 12:
            distance_reward = -5 / 18 * current_distance + 5 / 3

    elif d_distance > 0:
        if current_distance <= 6.0:
            distance_reward = (5 / 36) * current_distance ** 2 - (5 / 3) * current_distance + 5

    return distance_reward


def all_same_elements(memory_queue: deque):
    # If the deque is empty, return False
    if not memory_queue:
        return False

    # Get the first element
    first_element = memory_queue[0]

    # Check if all elements are the same as the first element
    for element in memory_queue:
        if element != first_element:
            return False, first_element

    return True, first_element


def calc_cost_for_circle_action(snake: 'SnakeGameAI'):
    same_actions, direction = all_same_elements(snake.memory_queue)

    if all_same_elements(snake.memory_queue) and direction != Direction.DOWN or direction != Direction.UP:
        return 2.0

    return 0


def calc_direction_change_cost(snake: 'SnakeGameAI'):
    move_cost = 0.1

    if not snake.memory_queue or len(snake.memory_queue) < 2:
        return 0

    if snake.memory_queue[0] != snake.memory_queue[1]:
        return move_cost

    return 0


def calc_movement_cost(snake: 'SnakeGameAI'):
    move_cost = 0.1 + (snake.moves_since_last_food / (len(snake.snake) * 40))

    return move_cost


def calc_not_dead_reward(snake: 'SnakeGameAI'):
    not_dead_reward = 0.8

    current_not_dead_reward = not_dead_reward - (snake.moves_since_last_food / 200 * len(snake.snake))
    if current_not_dead_reward < 0:
        current_not_dead_reward = 0

    return current_not_dead_reward


def calc_reenter_field_cost(snake: 'SnakeGameAI'):
    if snake.movement_field_repetition:
        return 0.5
    return 0