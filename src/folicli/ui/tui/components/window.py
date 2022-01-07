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

    def add_str(self, y: int, x: int, text: str, color: int = None):
        """Add string to current window

        Cuts text at right border of the window.
        Limits start column and line to window bounds.

        Arguments:
        y -- Line in which to add text
        x -- Position of first character in x axis
        text -- Text to be added
        color -- Color pair id if color is desired to be changed
        """
        max_y, max_x = self.window.getmaxyx()

        y = self._limit_between(y, 0, max_y - 1)
        x = self._limit_between(x, 0, max_x - 1)

        max_len = max_x - x
        if color is not None:
            self.window.addnstr(y, x, text, max_len, curses.color_pair(color))
        else:
            self.window.addnstr(y, x, text, max_len)

    def add_centered_str(self, y: int, text: str, color: int = None):
        """Add centered string to current window

        Cuts text at right border of the window.
        Limits line length to window width.

        Arguments:
        y -- Line in which to add the text
        text -- Text to be added
        color -- Color pair id if color is desired to be changed
        """
        _, max_x = self.window.getmaxyx()
        x = max_x // 2 - len(text) // 2
        if x < 0:
            x = 0
        self.add_str(y, x, text, color)

    def _limit_between(self, value, lower_boundary, upper_boundary):
        """Limit value between min and max

        Arguments:
        value -- Value to be limited
        lower_boundary -- Lower boundary
        upper_boundary -- Upper boundary

        Returns bounded value
        """
        if value < lower_boundary:
            return lower_boundary
        elif value > upper_boundary:
            return upper_boundary
        else:
            return value
