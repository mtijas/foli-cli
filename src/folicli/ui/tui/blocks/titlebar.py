import curses

from ui.tui.components.textwindow import TextWindow


class TitleBar(TextWindow):
    def __init__(
        self,
        height: int,
        width: int,
        y: int = 0,
        x: int = 0,
    ):
        """Construct a new TitleBar"""
        TextWindow.__init__(self, height, width, y, x)

    def static_render(self):
        if curses.has_colors:
            self.set_background_color(13)
        self.add_centered_str(0, "Foli CLI")
