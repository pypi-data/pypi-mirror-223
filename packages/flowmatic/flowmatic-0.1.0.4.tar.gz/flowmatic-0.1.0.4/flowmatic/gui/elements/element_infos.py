from typing import Callable, NamedTuple


class Button(NamedTuple):
    text: str
    command: Callable[[], None]
