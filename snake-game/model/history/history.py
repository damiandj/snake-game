import pickle
from dataclasses import dataclass
from datetime import datetime

from config import save_dir
from model.arena import Arena


@dataclass(frozen=True)
class HistoryItem:
    """Represents an item in the game history."""

    arena: Arena
    score: int


class GameHistory(list):
    """Represents the history of a game."""

    def add_to_history(self, game_stage: HistoryItem):
        self.append(game_stage)

    def save(self):
        """Save the game history to a file."""
        filename = save_dir / f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.pkl"
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(filename: str):
        """Load a game history from a file."""
        with open(filename, "rb") as file:
            return pickle.load(file)

    @classmethod
    def from_file(cls, filename: str):
        """Create a GameHistory object from a file."""
        return cls.load(filename)
