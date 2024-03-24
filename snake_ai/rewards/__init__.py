from numpy import sqrt


def calc_distance(snake: 'SnakeGameAI'):
    head = snake.head
    food = snake.food

    current_distance = abs(sqrt((food.x - head.x) ** 2 + (food.y - head.y) ** 2))

    lastDist = snake.lastDist
    snake.lastDist = current_distance

    return current_distance, lastDist