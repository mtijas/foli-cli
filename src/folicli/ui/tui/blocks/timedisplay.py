from ui.tui.components.textwindow import TextWindow
from observable import Observable, Observer


class TimeDisplay(TextWindow, Observer):
    def __init__(
        self,
        y: int = 0,
        x: int = 0,
        observable: Observable = None,
    ):
        """Construct a new TimeDisplay"""
        TextWindow.__init__(self, 1, 6, y, x)
        Observer.__init__(self, observable)
        self.observable.register_observer("formatted-time-update", self)

    def initial_render(self):
        self.window.clear()
        self.add_str(0, 0, "--:--")
        self.window.refresh()

    def notify(self, event: str, data):
        if event == "formatted-time-update":
            _, max_x = self.window.getmaxyx()
            self.add_str(0, 0, data)
            self.refresh()
