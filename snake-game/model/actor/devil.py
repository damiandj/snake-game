from typing import List

from config import devil_color
from model.actor.actor import Actor


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
