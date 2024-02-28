import copy
from typing import List

from config import snake_body_color, snake_head_color, mouse_color, devil_color


class Actor:
    """
    Base class for game actors.

    Attributes:
        position (List[int]): The initial position of the actor [x, y].
        color (str): The color of the actor.
        speed (int): The speed of the actor.
        step_to_move (int): Steps needed for the actor to move.
        direction (List[int]): The direction of the actor.
    """

    def __init__(self, position: List[int], color: str = "black"):
        """
        Initialize an Actor object.

        Args:
            position (List[int]): The initial position of the actor.
            color (str, optional): The color of the actor. Defaults to "black".
        """
        self.position = position
        self.color = color

        self.speed = 1
        self.step_to_move = 11 - self.speed
        self.direction = [0, 0]

    @property
    def direction(self) -> List[int]:
        """Get the direction of the actor."""
        return self._direction

    @direction.setter
    def direction(self, val: List[int]):
        """Set the direction of the actor."""
        self._direction = val

    def step(self):
        """Advance the actor by one step."""
        self.step_to_move -= 1
        if not self.step_to_move:
            self._reset_steps_to_move()
            self.make_step()

    def _reset_steps_to_move(self):
        """Reset the steps needed for the actor to move."""
        self.step_to_move = 11 - self.speed

    def turn_north(self):
        """Turn the actor to the north."""
        if self.direction[1] != 0:
            return
        self.direction = [0, -1]

    def turn_south(self):
        """Turn the actor to the south."""
        if self.direction[1] != 0:
            return
        self.direction = [0, 1]

    def turn_west(self):
        """Turn the actor to the west."""
        if self.direction[0] != 0:
            return
        self.direction = [-1, 0]

    def turn_east(self):
        """Turn the actor to the east."""
        if self.direction[0] != 0:
            return
        self.direction = [1, 0]

    def turn_back(self):
        self.direction = list(map(lambda x: -1 * x, self.direction))

    def make_step(self):
        """Make a step in the game."""
        pass


class SnakePart(Actor):
    """
    Represents a part of the snake body.

    Attributes:
        Inherits attributes from Actor.
    """

    def __init__(self, position: List[int]):
        """
        Initialize a SnakePart object.

        Args:
            position (List[int]): The initial position of the snake part.
        """
        super().__init__(position, snake_body_color)


class SnakeHead(Actor):
    """
    Represents a snake head.

    Attributes:
        Inherits attributes from Actor.
    """

    def __init__(self, position: List[int]):
        """
        Initialize a SnakeHead object.

        Args:
            position (List[int]): The initial position of the snake head.
        """
        super().__init__(position, snake_head_color)


class Snake(Actor):
    """
    Represents the snake in the game.

    Attributes:
        body (List[SnakePart]): The parts of the snake's body.
        arena_sizes (List[int]): The size of the game arena [width, height].
    """

    def __init__(self, position: List[int], arena_sizes: List[int]):
        """
        Initialize a Snake object.

        Args:
            position (List[int]): The initial position of the snake head [x, y].
            arena_sizes (List[int]): The size of the game arena [width, height].
        """
        self.body = [SnakeHead(position)]
        super().__init__(position)
        self.arena_sizes = arena_sizes

    @property
    def direction(self):
        """Get the direction of the snake."""
        return self.head.direction

    @direction.setter
    def direction(self, val):
        """Set the direction of the snake."""
        self.head.direction = val

    @property
    def head(self):
        """Get the head of the snake."""
        return self.body[0]

    @property
    def tail(self):
        """Get the tail of the snake."""
        return self.body[1:]

    def speed_up(self):
        """Increase the speed of the snake."""
        if self.speed < 10:
            self.speed += 1
            self._reset_steps_to_move()

    def add_part(self):
        """Add a part to the snake's body."""
        prev_part = self.body[-1]
        new_part_position = [
            (prev_part.position[0] - prev_part.direction[0]) % self.arena_sizes[0],
            (prev_part.position[1] - prev_part.direction[1]) % self.arena_sizes[1],
        ]
        new_part = SnakePart(new_part_position)
        new_part.direction = prev_part.direction
        self.body.append(new_part)

    def make_step(self):
        """Move the snake by one step."""
        old_snake = copy.deepcopy(self.body)
        new_head_position = [
            (old_snake[0].position[0] + self.direction[0]) % self.arena_sizes[0],
            (old_snake[0].position[1] + self.direction[1]) % self.arena_sizes[1],
        ]
        self.head.position = new_head_position

        for item, part in enumerate(self.tail):
            part.position = old_snake[item].position
            part.direction = old_snake[item].direction


class Mouse(Actor):
    """
    Represents a mouse in the game.

    Attributes:
        Inherits attributes from Actor.
    """

    def __init__(self, position: List[int]):
        """
        Initialize a Mouse object.

        Args:
            position (List[int]): The initial position of the mouse.
        """
        super().__init__(position, color=mouse_color)


class Devil(Actor):
    """
    Represents a devil in the game.

    Attributes:
        Inherits attributes from Actor.
    """

    def __init__(self, position: List[int]):
        """
        Initialize a Devil object.

        Args:
            position (List[int]): The initial position of the devil.
        """
        super().__init__(position, color=devil_color)
