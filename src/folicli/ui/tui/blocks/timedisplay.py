import curses

from observable import Observable, Observer
from ui.tui.components.textwindow import TextWindow


class TimeDisplay(TextWindow, Observer):
    def __init__(
        self,
        y: int = 0,
        x: int = 0,
        observable: Observable = None,
    ):
        """Construct a new TimeDisplay"""
        TextWindow.__init__(self, 1, 8, y, x)
        Observer.__init__(self, observable)
        self.observable.register_observer("formatted-time-update", self)

    def static_render(self):
        """Render placeholder as static"""
        if curses.has_colors:
            self.set_background_color(12)
        self.add_str(0, 0, " --:-- ")

    def notify(self, event: str, data):
        if event == "formatted-time-update":
            self.add_str(0, 0, f" {data} ")
