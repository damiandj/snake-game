import copy
from operator import add
from typing import List

from config import snake_body_color, snake_head_color, mouse_color, devil_color


class Actor:
    def __init__(self, position: List[int], color: str = "black"):
        self.position = position
        self.color = color

        self.speed = 1
        self.step_to_move = 11 - self.speed
        self.direction = [0, 0]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, val):
        self._direction = val

    def _reset_steps_to_move(self):
        self.step_to_move = 11 - self.speed

    def step(self):
        self.step_to_move -= 1
        if not self.step_to_move:
            self._reset_steps_to_move()
            self.make_step()

    def turn_up(self):
        if self.direction[1] != 0:
            return
        self.direction = [0, -1]

    def turn_bottom(self):
        if self.direction[1] != 0:
            return
        self.direction = [0, 1]

    def turn_left(self):
        if self.direction[0] != 0:
            return
        self.direction = [-1, 0]

    def turn_right(self):
        if self.direction[0] != 0:
            return
        self.direction = [1, 0]

    def turn_back(self):
        self.direction = list(map(lambda x: -1 * x, self.direction))

    def make_step(self): ...


class SnakeBody(Actor):
    def __init__(self, position: List[int]):
        super().__init__(position, snake_body_color)


class SnakeHead(Actor):
    def __init__(self, position: List[int]):
        super().__init__(position, snake_head_color)


class Snake(Actor):
    def __init__(self, position: List[int], arena_sizes: List[int]):
        self.body = [SnakeHead(position)]
        super().__init__(position)
        self.arena_sizes = arena_sizes

    @property
    def direction(self):
        return self.head.direction

    @direction.setter
    def direction(self, val):
        self.head.direction = val

    @property
    def head(self):
        return self.body[0]

    @property
    def tail(self):
        return self.body[1:]

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
            map(add, old_snake[0].position, map(lambda x: 1 * x, self.direction))
        )
        if self.head.position[0] == self.arena_sizes[0]:
            self.head.position[0] = 0
        if self.head.position[0] == -1:
            self.head.position[0] = self.arena_sizes[0] - 1
        if self.head.position[1] == self.arena_sizes[1]:
            self.head.position[1] = 0
        if self.head.position[1] == -1:
            self.head.position[1] = self.arena_sizes[1] - 1

        for item, part in enumerate(self.tail):
            part.position = old_snake[item].position
            part.direction = old_snake[item].direction

        del old_snake


class Mouse(Actor):
    def __init__(self, position: List[int]):
        super().__init__(position, color=mouse_color)


class Devil(Actor):
    def __init__(self, position: List[int]):
        super().__init__(position, color=devil_color)
