import curses
import logging
from abc import ABC, abstractmethod


class Window(ABC):
    """Curses-based window for building Text UI"""

    def __init__(self, height: int, width: int, y: int = 0, x: int = 0):
        """Constructor

        Arguments:
        height -- Window height in lines.
        width -- Window width in characters.
        y -- Position of top left corner, y axis. In lines.
        x -- Position of top left corner, x axis. In characters.
        """
        self._logger = logging.getLogger("foli-cli.ui.tui.components.Window")
        self.height = height if height > 0 else 1
        self.width = width if width > 0 else 1
        self.y = y if y >= 0 else 0
        self.x = x if x >= 0 else 0
        self.window = curses.newwin(self.height, self.width, self.y, self.x)
        self.window.keypad(True)
        self.window.nodelay(True)

    def add_child(self, name: str, child):
        """Add a child Window component.

        Arguments:
        name -- Name of the window for easier usage
        child -- a Window object to be added as a child

        Raises RuntimeWarning in case current object should not have children
        """
        raise RuntimeWarning("This component should not have children")

    def remove_child(self, name: str):
        """Remove a child Window component.

        Arguments:
        name -- name of the window to be removed

        Raises RuntimeWarning in case current object should not have children
        """
        raise RuntimeWarning("This component should not have children")

    def initial_render(self):
        """Initial render of window.

        Clears window and calls static and dynamic renders.
        """
        self.window.erase()
        if curses.has_colors():
            self.set_background_color(0)
        self.static_render()
        self.dynamic_render()

    @abstractmethod
    def static_render(self):
        """Render of static Window contents.

        Gives ability to render static parts of the window.
        """
        pass

    @abstractmethod
    def dynamic_render(self):
        """Render of dynamic Window contents.

        Gives ability to render dynamic parts of the window.
        """
        pass

    def set_background_color(self, color_pair_id: int):
        """Set background color of the window

        Arguments:
        color_pair_id -- Number/id of curses.color_pair for background color.
        """
        self.window.bkgd(" ", curses.color_pair(color_pair_id))

    def refresh(self):
        """Refresh internal window"""
        if self.window.is_wintouched():
            self.window.refresh()

    def getch(self):
        """Get ch from internal window

        Returns int of char (basically what Python Curses getch() returns
        """
        return self.window.getch()

    def get_max_yx(self):
        """Gets rightmost column and last line numbers for internal window

        Returns tuple of (bottom line, rightmost column)
        """
        max_y, max_x = self.window.getmaxyx()
        return (max_y - 1, max_x - 1)

    def move(self, new_y: int = 0, new_x: int = 0):
        """Move window to a new location

        Arguments:
        new_y -- New Y location
        new_x -- New X location
        """
        self._logger.debug(f"Moving window to y:{new_y} x:{new_x}")
        self.y = new_y
        self.x = new_x
        self.window.mvwin(new_y, new_x)
        self.window.touchwin()

    def resize(self, height: int, width: int):
        """Resize window

        Arguments:
        height -- Height of the window
        width -- Width of the window
        """
        self._logger.debug(f"Resizing window to h:{height} w:{width}")
        self.height = height
        self.width = width
        self.window.resize(height, width)
        self.initial_render()
