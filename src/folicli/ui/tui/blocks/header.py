from ui.tui.components.compositecomponent import CompositeComponent
from ui.tui.blocks.titlebar import TitleBar
from ui.tui.blocks.timedisplay import TimeDisplay
from observable import Observable

import curses


class Header(CompositeComponent):
    def __init__(
        self,
        width: int,
        y: int = 0,
        x: int = 0,
        observable: Observable = None,
    ):
        """Construct a new Header"""
        super().__init__(1, width, y, x)
        titlebar = TitleBar(1, width, y, x)
        timedisplay = TimeDisplay(y, width - 7, observable=observable)
        self.add_child(titlebar)
        self.add_child(timedisplay)

        if curses.has_colors:
            self.set_background_color(13)
            timedisplay.set_background_color(12)
