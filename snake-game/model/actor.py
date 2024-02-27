import copy
from operator import add
from typing import List

from config import snake_body_color, snake_head_color


class Actor:
    def __init__(self, position: List[int], color: str = "black"):
        self.position = position
        self.color = color

        self.speed = 1
        self.step_to_move = 11 - self.speed
        self.direction = [0, 0]

    def _reset_steps_to_move(self):
        self.step_to_move = 11 - self.speed

    def step(self):
        self.step_to_move -= 1
        if not self.step_to_move:
            self._reset_steps_to_move()
            self.make_step()

    def make_step(self): ...


class SnakeBody(Actor):
    def __init__(self, position: List[int]):
        super().__init__(position, snake_body_color)


class SnakeHead(Actor):
    def __init__(self, position: List[int]):
        super().__init__(position, snake_head_color)


class Snake(Actor):
    def __init__(self, position: List[int], arena_sizes: List[int]):
        super().__init__(position)
        self.head = SnakeHead(position)
        self.arena_sizes = arena_sizes
        self.body = [self.head]

    def speed_up(self):
        if self.speed < 10:
            self.speed += 1
            self._reset_steps_to_move()

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

    def make_step(self):
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


class Mouse:
    def __init__(self, position: List[int]):
        self.position = position

        self.color = "darkgray"
