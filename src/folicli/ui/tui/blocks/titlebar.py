from ui.tui.components.window import Window
from observable import Observable, Observer


class TitleBar(Window, Observer):
    def __init__(
        self,
        height: int,
        width: int,
        y: int = 0,
        x: int = 0,
        observable: Observable = None,
    ):
        Window.__init__(self, height, width, y, x)
        Observer.__init__(self, observable)
        self.observable.register_observer("formatted-time-update", self)

    def initial_render(self):
        self.window.clear()
        self.add_centered_str(0, "Föli CLI")
        self.window.refresh()

    def notify(self, event: str, data):
        if event == "formatted-time-update":
            _, max_x = self.window.getmaxyx()
            self.add_str(0, max_x - 6, data)
            self.refresh()
