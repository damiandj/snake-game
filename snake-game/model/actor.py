import copy
from operator import add
from typing import List


class SnakeBody:
    def __init__(self, position: List[int]):
        self.position = position

        self.color = "aquamarine3"
        self.direction = [0, 1]  # right

    def __str__(self):
        return "B"

    @property
    def description(self):
        return f"(SnakePart: {self.position}, {self.direction})"


class SnakeHead(SnakeBody):
    def __init__(self, position: List[int]):
        super().__init__(position)
        self.color = "aquamarine4"

    def __str__(self):
        return "H"

    @property
    def description(self):
        return f"(SnakeHead: {self.position}, {self.direction})"


class Snake:
    def __init__(self, head: SnakeHead, arena_sizes: List[int]):
        self.head = head
        self.arena_sizes = arena_sizes
        self.body = [self.head]

    def add_part(self):
        prev_part = self.body[-1]
        new_part_position = list(
            map(add, prev_part.position, map(lambda x: -1 * x, prev_part.direction))
        )
        if new_part_position[0] == self.arena_sizes[0]:
            new_part_position[0] = 0
        if new_part_position[0] == -1:
            new_part_position[0] = self.arena_sizes[0] - 1
        if new_part_position[1] == self.arena_sizes[1]:
            new_part_position[1] = 0
        if new_part_position[1] == -1:
            new_part_position[1] = self.arena_sizes[1] - 1
        new_part = SnakeBody(new_part_position)

        new_part.direction = prev_part.direction

        self.body.append(new_part)

    def step(self):
        old_snake = copy.deepcopy(self.body)
        self.head.position = list(
            map(
                add, old_snake[0].position, map(lambda x: 1 * x, old_snake[0].direction)
            )
        )
        if self.head.position[0] == self.arena_sizes[0]:
            self.head.position[0] = 0
        if self.head.position[0] == -1:
            self.head.position[0] = self.arena_sizes[0] - 1
        if self.head.position[1] == self.arena_sizes[1]:
            self.head.position[1] = 0
        if self.head.position[1] == -1:
            self.head.position[1] = self.arena_sizes[1] - 1

        for item, part in enumerate(self.body[1:]):
            part.position = old_snake[item].position
            part.direction = old_snake[item].direction

        del old_snake

    def turn_up(self):
        if self.head.direction[1] != 0:
            return
        self.head.direction = [0, -1]

    def turn_bottom(self):
        if self.head.direction[1] != 0:
            return
        self.head.direction = [0, 1]

    def turn_left(self):
        if self.head.direction[0] != 0:
            return
        self.head.direction = [-1, 0]

    def turn_right(self):
        if self.head.direction[0] != 0:
            return
        self.head.direction = [1, 0]

    @property
    def description(self):
        return "+".join([item.description for item in self.body])


class Mouse:
    def __init__(self, position: List[int]):
        self.position = position

        self.color = "darkgray"


# head = SnakeHead([5, 5])
# snake = Snake(head=head)
# snake.add_part()
# snake.add_part()
# print(snake.description)
# snake.step()
# print(snake.description)
# snake.turn_up()
# snake.step()
# print(snake.description)
# snake.add_part()
# snake.step()
# print(snake.description)
