from typing import List, Tuple


class Actor:
    """
    Base class for game actors.

    Attributes:
        position (Tuple[int]): The initial position of the actor [x, y].
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

        self._turning_blocked = False

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
            self._turning_blocked = False
            self.make_step()

    def _reset_steps_to_move(self):
        """Reset the steps needed for the actor to move."""
        self.step_to_move = 11 - self.speed

    def turn_north(self):
        """Turn the actor to the north."""
        if self._turning_blocked:
            return
        if self.direction[1] != 0:
            return
        self.direction = [0, -1]
        self._turning_blocked = True

    def turn_south(self):
        """Turn the actor to the south."""
        if self._turning_blocked:
            return
        if self.direction[1] != 0:
            return
        self.direction = [0, 1]
        self._turning_blocked = True

    def turn_west(self):
        """Turn the actor to the west."""
        if self.direction[0] != 0:
            return
        self.direction = [-1, 0]

    def turn_east(self):
        """Turn the actor to the east."""
        if self._turning_blocked:
            return
        if self.direction[0] != 0:
            return
        self.direction = [1, 0]
        self._turning_blocked = True

    def turn_back(self):
        """Turn back the actor."""
        self.direction = list(map(lambda x: -1 * x, self.direction))

    def make_step(self):
        """Make a step in the game."""
        pass
