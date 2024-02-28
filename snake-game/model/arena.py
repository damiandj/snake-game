from typing import Union

from model.actor import SnakePart, SnakeHead, Mouse


class Arena:
    def __init__(self, size: int):
        self.size = size
        self.arena = [["-" for _ in range(self.size)] for _ in range(self.size)]

    def add_snake_part(self, snake_part: Union[SnakePart, SnakeHead]):
        self.arena[snake_part.position[0]][snake_part.position[1]] = snake_part

    def add_mouse(self, mouse: Mouse):
        self.arena[mouse.position[0]][mouse.position[1]] = mouse

    @property
    def description(self):
        out = ""
        for l in self.arena:
            for i in l:
                out += f" {i}"
            out += "\n"
        return out
