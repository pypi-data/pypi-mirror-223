import tkinter as tk
import customtkinter as ctk
import tkinterdnd2

from flowmatic.gui.gui import GUI  # pylint: disable=import-error

from .screens.screen import Screen
from ..flows.flow import Flow


class TKGUI(GUI):
    root: tk.Tk
    title: str
    start_screen: Screen
    geometry: str
    light_mode: bool

    def __init__(
        self,
        title: str,
        start_screen: type[Screen],
        geometry: str = "1280x720",
        light_mode: bool = False,
    ) -> None:
        self.root = tkinterdnd2.Tk()
        self.title = title
        self.start_screen = start_screen()
        self.geometry = geometry
        self.light_mode = light_mode

    def start(self) -> None:
        """Start GUI.
        Args:
            screen (type[Screen]): Screen to start with."""
        self.setup()
        self.build_screen(self.start_screen)
        self.root.mainloop()

    def setup(self) -> None:
        ctk.set_appearance_mode("light" if self.light_mode else "dark")
        self.root.geometry(self.geometry)
        self.root.title(self.title)

    def switch_screen(self, screen: Screen) -> None:
        """Switch to a new screen.

        Args:
            screen (type[Screen]): Screen to show."""
        self.clear_screen()
        self.build_screen(screen)

    def start_flow(self, flow: Flow) -> None:
        self.clear_screen()
        self.current_flow = flow
        flow.start()

    def build_screen(self, screen: Screen) -> None:
        """Build screen.

        Args:
            screen (type[Screen]): Screen to build."""
        screen(self.root).build()
        self.current_screen = screen

    def clear_screen(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def update(self) -> None:
        self.root.update()

    def quit(self) -> None:
        self.root.quit()
