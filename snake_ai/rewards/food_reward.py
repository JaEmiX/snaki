from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from snake_ai.game import SnakeGameAI


def calc_food_reward(snake: 'SnakeGameAI'):
    food_reward = 40 + 5 * snake.score
    return food_reward

