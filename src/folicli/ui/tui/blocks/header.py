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
        timedisplay = TimeDisplay(y, width - 8, observable=observable)
        self.add_child("titlebar", titlebar)
        self.add_child("timedisplay", timedisplay)

    def resize(self, height: int, width: int):
        """Resize child windows

        Arguments:
        height -- Height of the window
        width -- Width of the window
        """
        self.width = width
        self.children["timedisplay"].move(0, width - 8)
        self.children["titlebar"].resize(1, width)
