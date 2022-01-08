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

    def initial_render(self):
        self.window.clear()
        self.add_centered_str(0, "Foli CLI")
        self.window.refresh()
