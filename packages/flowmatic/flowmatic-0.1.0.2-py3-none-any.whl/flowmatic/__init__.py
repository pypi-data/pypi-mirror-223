from .gui.screens import *
from .gui.screens.screen import *
from .gui.elements import *
from .flows.flow import Flow
from .server import Server
from .util import Settings
from .flowmatic import App


server = Server()


def run(app: App):
    """Start app.
    Args:
        screen (type[Screen]): Screen to start with."""
    server.app = app
    server.app.start()


def show_screen(screen: Screen):
    """Show screen.
    Args:
        screen (type[Screen]): Screen to show."""
    server.app.show_screen(screen)


def start_flow(flow: Flow):
    """Start flow.
    Args:
        flow (Flow): Flow to start."""
    server.app.start_flow(flow)


def get_settings() -> Settings:
    """Get settings.
    Returns:
        Settings: Settings."""
    return server.app.settings


def set_settings(settings: dict[str, str]) -> None:
    """Set settings.
    Args:
        settings (dict[str, str]): Settings."""
    server.app.settings.set(settings)
    server.app.settings.save()


def update_gui():
    server.app.gui.update()


def quit_app():
    server.app.quit()
