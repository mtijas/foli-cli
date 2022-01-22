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
        self.polling_interval = None
        TextWindow.__init__(self, height, width, y, x)
        Observer.__init__(self, observable)
        self.observable.register_observer("polling-interval-update", self)

    def static_render(self):
        self.add_str(0, 0, "Polling: ")

    def dynamic_render(self):
        self.window.move(0, 9)
        self.window.clrtoeol()
        if self.polling_interval is not None:
            self.add_str(0, 9, f"every {self.polling_interval} seconds")
        else:
            self.add_str(0, 9, f"OFF")

    def notify(self, event: str, data):
        if event == "polling-interval-update":
            if data > 0:
                self.polling_interval = data
            else:
                self.polling_interval = None
        self.dynamic_render()
