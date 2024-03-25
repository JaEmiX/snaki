from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from snake_ai.game import SnakeGameAI


def calc_food_reward(snake: 'SnakeGameAI'):
    food_reward = 60 + 8 * snake.score - snake.moves_since_last_food * 0.1
    return food_reward

