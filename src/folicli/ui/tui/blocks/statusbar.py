from ui.tui.components.textwindow import TextWindow
from observable import Observable, Observer


class StatusBar(TextWindow, Observer):
    def __init__(
        self,
        height: int,
        width: int,
        y: int = 0,
        x: int = 0,
        observable: Observable = None,
    ):
        TextWindow.__init__(self, height, width, y, x)
        Observer.__init__(self, observable)
        self.observable.register_observer("polling-interval-update", self)

    def initial_render(self):
        self.window.clear()
        self.add_str(0, 0, "Polling: OFF")
        self.refresh()

    def notify(self, event: str, data):
        self.window.clear()
        if event == "polling-interval-update":
            if data > 0:
                self.add_str(
                    0,
                    0,
                    f"Polling: every {data} seconds",
                )
            else:
                self.add_str(0, 0, "Polling: OFF")
        self.refresh()
