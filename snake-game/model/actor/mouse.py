from typing import List

from config import mouse_color
from model.actor.actor import Actor


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
