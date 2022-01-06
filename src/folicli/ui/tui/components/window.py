import curses
from abc import ABC, abstractmethod


class Window(ABC):
    def __init__(self, height:int, width:int, y:int=0, x:int=0):
        self.children = []
        self.height = height if height > 0 else 1
        self.width = width if width > 0 else 1
        self.y = y if y >= 0 else 0
        self.x = x if x >= 0 else 0
        self.window = curses.newwin(self.height, self.width, self.y, self.x)

    @abstractmethod
    def initial_render(self):
        pass

    def refresh(self):
        '''Refresh internal window'''
        self.window.refresh()
        for child in self.children:
            child.refresh()

    def add_child(self, window):
        '''Add a new Window as child'''
        if element not in self.children:
            self.children.append(window)

    def add_str(self, y, x, text, color=None):
        '''Add string to current window'''
        max_y, max_x = self.window.getmaxyx()
        max_len = max_x-x
        if y < max_y and x < max_x and max_len > 0:
            if color is not None:
                self.window.addnstr(y, x, text, max_len, color)
            else:
                self.window.addnstr(y, x, text, max_len)

    def add_centered_str(self, y, text, color=None):
        '''Add centered string to current window'''
        _, x = self.window.getmaxyx()
        x = x // 2 - len(text) // 2
        if x < 0:
            x = 0
        self.add_str(y, x, text, color)
