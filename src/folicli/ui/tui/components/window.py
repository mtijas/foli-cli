import curses
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
        self.height = height if height > 0 else 1
        self.width = width if width > 0 else 1
        self.y = y if y >= 0 else 0
        self.x = x if x >= 0 else 0
        self.window = curses.newwin(self.height, self.width, self.y, self.x)
        self.window.keypad(True)
        self.window.nodelay(True)

    def add_child(self, child):
        """Add a child Window component.

        Arguments:
        child -- a Window object to be added as a child

        Raises RuntimeWarning in case current object should not have children
        """
        raise RuntimeWarning("This component should not have children")

    def remove_child(self, child):
        """Remove a child Window component.

        Arguments:
        child -- a Window object to be removed

        Raises RuntimeWarning in case current object should not have children
        """
        raise RuntimeWarning("This component should not have children")

    @abstractmethod
    def initial_render(self):
        """Initial render of Window contents.

        Gives ability to render static parts of the window initially.
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
