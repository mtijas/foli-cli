from ui.tui.components.window import Window
from observable import Observable, Observer


class StatusBar(Window, Observer):
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
        self.observable.register_observer("status-update", self)

    def initial_render(self):
        self.window.clear()
        self.add_str(0, 0, "Status:")
        self.refresh()

    def notify(self, event: str, data):
        self.add_str(0, 8, data)
        self.refresh()
