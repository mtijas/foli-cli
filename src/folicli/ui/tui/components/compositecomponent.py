import curses


class CompositeComponent:
    """Curses-based composite block for building Text UI"""

    def __init__(self):
        self.children = []

    def initial_render(self):
        """Initial render of Window contents.

        Gives ability to render static parts of the window initially.
        """
        for child in self.children:
            child.initial_render()

    def add_child(self, child):
        """Add a child Window component.

        Arguments:
        child -- a Window object to be added as a child

        Raises RuntimeWarning in case current object should not have children
        """
        if child in self.children:
            return

        self.children.append(child)

    def remove_child(self, child):
        """Remove a child Window component.

        Arguments:
        child -- a Window object to be removed

        Raises RuntimeWarning in case current object should not have children
        """
        self.children.remove(child)

    def set_background_color(self, color_pair_id: int):
        """Set background color of every child

        Arguments:
        color_pair_id -- Number/id of curses.color_pair for background color.
        """
        for child in self.children:
            child.set_background_color(color_pair_id)

    def refresh(self):
        """Refresh internal window of every child"""
        for child in self.children:
            child.refresh()
