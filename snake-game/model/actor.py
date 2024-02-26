from __future__ import annotations

from operator import add
from typing import List


class Actor:
    def __init__(self, center: List[float], size: List[float], arena_size: List[float]):
        self.center = center
        self.size = size
        self.arena_size = arena_size

        self.speed = 0
        self.direction = [1, 0]  # right
        self.color = "white"

    @property
    def left(self):
        return self.center[0] - self.size[0] / 2

    @property
    def right(self):
        return self.center[0] + self.size[0] / 2

    @property
    def top(self):
        return self.center[1] + self.size[1] / 2

    @property
    def bottom(self):
        return self.center[1] - self.size[1] / 2

    def step(self):
        self.center = list(
            map(add, self.center, map(lambda x: x * self.speed, self.direction))
        )
        if self.center[0] < 0:
            self.center[0] = self.arena_size[0]

        if self.center[0] > self.arena_size[0]:
            self.center[0] = 0

        if self.center[1] < 0:
            self.center[1] = self.arena_size[1]

        if self.center[1] > self.arena_size[1]:
            self.center[1] = 0

    def speed_up(self):
        self.speed += 1

    def slow_down(self):
        if self.speed > 1:
            self.speed -= 1

    def __str__(self):
        return f"{self.center}, {self.size}"

    def intersect(self, other: Actor, epsilon: float = 1) -> bool:
        return (
            abs(self.center[0] - other.center[0])
            < (self.size[0] / 2 + other.size[0] / 2) * epsilon
        ) and (
            abs(self.center[1] - other.center[1])
            < (self.size[1] / 2 + other.size[1] / 2) * epsilon
        )


class SnakePiece(Actor):
    def __init__(
        self, position: List[float], size: List[float], arena_size: List[float]
    ):
        super().__init__(position, size, arena_size)
        self.color = "green"


class SnakeHead(SnakePiece):
    def __init__(
        self, position: List[float], size: List[float], arena_size: List[float]
    ):
        super().__init__(position, size, arena_size)
        self.color = "darkgreen"


class SnakeBody:
    def __init__(self, head: SnakeHead):
        self.head = head
        self.tail = []

    def speed_up(self):
        self.head.speed_up()
        for item in self.tail:
            item.speed = self.head.speed

    def add_piece(self):
        last_piece = self.tail[-1] if self.tail else self.head
        if last_piece.direction == [1, 0]:
            new_piece_center = [
                last_piece.center[0] - last_piece.size[0],
                last_piece.center[1],
            ]
        elif last_piece.direction == [-1, 0]:
            new_piece_center = [
                last_piece.center[0] + last_piece.size[0],
                last_piece.center[1],
            ]
        elif last_piece.direction == [0, 1]:
            new_piece_center = [
                last_piece.center[0],
                last_piece.center[1] - last_piece.size[1],
            ]
        else:
            new_piece_center = [
                last_piece.center[0],
                last_piece.center[1] + last_piece.size[1],
            ]
        new_piece = SnakePiece(
            position=new_piece_center,
            size=last_piece.size,
            arena_size=last_piece.arena_size,
        )
        new_piece.direction = last_piece.direction
        new_piece.speed = last_piece.speed
        self.tail.append(new_piece)


class Mouse(Actor):
    def __init__(self, position: List[int], size: List[float], arena_size: List[int]):
        super().__init__(position, size, arena_size)
        self.color = "darkgray"


class DirectionChangePoint(Actor):
    def __init__(self, center: List[float], size: List[float], arena_size: List[float]):
        super().__init__(center, size, arena_size)
