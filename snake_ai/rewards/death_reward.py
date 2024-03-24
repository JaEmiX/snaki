from typing import TYPE_CHECKING
from snake_ai.rewards import calc_distance

if TYPE_CHECKING:
    from snake_ai.game import SnakeGameAI


def calc_death_reward(snake: 'SnakeGameAI', suicide: bool):
    if suicide:
        return calc_suicide_reward(snake)
    else:
        return calc_distance_to_food_after_death_reward(snake)


def calc_distance_to_food_after_death_reward(snake: 'SnakeGameAI'):
    current_distance = calc_distance(snake)[0]

    if 18.0 < current_distance:
        return -20
    elif 12.0 < current_distance <= 18.0:
        return -8
    elif 6.0 < current_distance <= 12.0:
        return -2
    elif 6.0 < current_distance <= 2.5:
        return 1
    elif 2.5 < current_distance <= 1.5:
        return 2.5
    else:
        return 5


def calc_suicide_reward(snake: 'SnakeGameAI'):
    suicide_reward = -40 * len(snake.snake)

    return suicide_reward
