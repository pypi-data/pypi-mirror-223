from typing import Protocol, Self
import tkinter as tk

from ...flows.flow import Flow


class Screen(Protocol):
    """Screen protocol.

    Args:
        master (tk.Tk): Master window.

    Methods:
        build: Build screen."""

    master: tk.Tk

    def __init__(self) -> None:
        ...

    def __call__(self, master: tk.Tk) -> Self:
        self.master = master  # pylint: disable=attribute-defined-outside-init
        return self

    def build(self) -> None:  # pylint: disable=missing-function-docstring
        ...


class FlowScreen(Screen):
    flow: Flow

    def __init__(self, flow: Flow) -> None:
        self.flow = flow
        super().__init__()

    def next(self) -> None:
        self.flow.next()

    def previous(self) -> None:
        self.flow.previous()

    def build(self) -> None:
        ...
