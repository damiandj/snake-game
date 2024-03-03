from model.actor import Mouse, Snake, Devil
from model.actor.snake import SnakeHead, SnakePart


class Arena:
    def __init__(self, size: int):
        self.size = size
        self.arena = [["" for _ in range(self.size)] for _ in range(self.size)]

    def add_snake(self, snake: Snake):
        for part in snake.body:
            self.arena[part.position[0]][part.position[1]] = part

    def add_mouse(self, mouse: Mouse):
        self.arena[mouse.position[0]][mouse.position[1]] = mouse

    def add_devil(self, devil: Devil):
        self.arena[devil.position[0]][devil.position[1]] = devil

    @property
    def flat_arena(self):
        return [cell for row in self.arena for cell in row]

    def __str__(self):
        ret = ""
        for row in self.arena:
            ret += "|"
            for cell in row:
                if isinstance(cell, SnakeHead):
                    ret += "H|"
                elif isinstance(cell, SnakePart):
                    ret += "B|"
                elif isinstance(cell, Mouse):
                    ret += "M|"
                elif isinstance(cell, Devil):
                    ret += "D|"
                else:
                    ret += "-|"
            ret += "\n"

        return ret

    def __repr__(self):
        return self.__str__()
