import curses
from .window import Window


class CompositeComponent(Window):
    """Curses-based composite block for building Text UI"""

    def __init__(self, height: int, width: int, y: int = 0, x: int = 0):
        super().__init__(height, width, y, x)
        self.children = {}

    def initial_render(self):
        """Initial render of child window.

        Clears child window and calls static and dynamic renders.
        """
        for child in self.children.values():
            child.window.clear()
            child.static_render()
            child.dynamic_render()

    def static_render(self):
        """Render of static Window contents."""
        for child in self.children.values():
            child.static_render()

    def dynamic_render(self):
        """Render of dynamic Window contents."""
        for child in self.children.values():
            child.dynamic_render()

    def add_child(self, name: str, child):
        """Add a child Window component.

        Arguments:
        name -- Name of the window for easier usage
        child -- a Window object to be added as a child
        """
        if name in self.children:
            return

        self.children[name] = child

    def remove_child(self, name: str):
        """Remove a child Window component.

        Arguments:
        name -- name of the window to be removed
        """
        del self.children[name]

    def set_background_color(self, color_pair_id: int):
        """Set background color of every child

        Arguments:
        color_pair_id -- Number/id of curses.color_pair for background color.
        """
        for child in self.children.values():
            child.set_background_color(color_pair_id)

    def refresh(self):
        """Refresh internal window of every child"""
        for child in self.children.values():
            child.window.refresh()
