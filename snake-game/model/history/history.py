import copy
import pickle
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import save_dir
from model.arena import Arena


@dataclass(frozen=True)
class HistoryItem:
    """Represents an item in the game history."""

    arena: Arena
    score: int


class GameHistory(list):
    """
    Represents the history of a game.

    Attributes:
        path (Optional[Path]): The path of the file the history was saved to.
    """

    def __init__(self):
        super().__init__()
        self.path = Optional[Path]

    def add_to_history(self, game_stage: HistoryItem):
        """
        Add a game stage to the game history.

        Args:
            game_stage (HistoryItem): The game stage to add to the history.

        """
        self.append(game_stage)

    def remove_duplicated_beginning(self):
        """Remove duplicated beginning of the game."""
        for i in range(len(self) - 1):
            if self[i] == self[i + 1]:
                self.pop(i)
            else:
                break

    def save(self, cleanup=True):
        """
        Save the game history to a file. The file name is the current date and time.
        The file is saved in the save_dir directory. If cleanup is True, remove duplicated beginning of the game.

        Args:
            cleanup (bool): Whether to remove duplicated beginning of the game.
        """
        filename = save_dir / f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.pkl"
        self.path = filename
        history_cp = copy.deepcopy(self)
        if cleanup:
            history_cp.remove_duplicated_beginning()
        if len(self) < 1:
            return
        with open(filename, "wb") as file:
            pickle.dump(history_cp, file)

    def load(self, filename: Path):
        """
        Load a game history from a file.

        Args:
            filename (Path): The path of the file to load the history from.
        """
        self.path = filename
        with open(filename, "rb") as file:
            self.extend(list(pickle.load(file)))

    @classmethod
    def from_file(cls, filename: Path):
        """
        Create a GameHistory object from a file.

        Args:
            filename (Path): The path of the file to load the history from.
        """
        history = cls()
        history.load(filename)
        return history
