import random
from typing import List

from snake_game.config import devil_color
from snake_game.model.actor.actor import Actor


class Devil(Actor):
    """
    Represents a devil in the game.

    Attributes:
        Inherits attributes from Actor.
    """

    def __init__(self, position: List[int], arena_sizes: List[int]):
        """
        Initialize a Devil object.

        Args:
            position (List[int]): The initial position of the devil.
        """
        super().__init__(position, arena_sizes, color=devil_color)
        self.speed = 2
        self.direction = random.choice([[-1, 0], [1, 0], [0, 1], [0, -1]])
        self.dist = 0
        self.max_dist = 5

    def next_position(self) -> List[int]:
        if self.dist < self.max_dist:
            position = [
                (self.position[0] + self.direction[0]) % self.arena_sizes[0],
                (self.position[1] + self.direction[1]) % self.arena_sizes[1],
            ]
            self.dist += 1
        else:
            self.dist = 0
            self.turn_left()
            position = self.next_position()
        return position
