from typing import Iterable

from typing_extensions import Protocol


class OutputDriverProtocol(Protocol):
    def writelines(self, lines: Iterable[str]) -> None:
        """Iterates and write lines

        Args:
            lines (Iterable[str]): The iterable of lines to save
        """
