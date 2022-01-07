from ui.tui.components.window import Window


class TitleBar(Window):
    def __init__(self, height: int, width: int, y: int = 0, x: int = 0):
        super().__init__(height, width, y, x)

    def initial_render(self):
        self.window.clear()
        self.add_centered_str(0, "Föli CLI")
        self.window.refresh()
