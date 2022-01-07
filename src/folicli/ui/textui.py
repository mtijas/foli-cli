from multiprocessing import current_process
from time import sleep
import curses
from datetime import datetime

from messagebroker import Subscriber, Publisher
from ui.tui.blocks.titlebar import TitleBar
from ui.tui.blocks.statusbar import StatusBar
from observable import Observable


class TextUI(Subscriber, Publisher):
    def __init__(self, stop_event, pub_queue, sub_queue):
        self.stop_event = stop_event
        self.events = Observable()

        Publisher.__init__(self, pub_queue)
        Subscriber.__init__(self, sub_queue)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        if curses.has_colors:
            curses.start_color()
            curses.use_default_colors()
            self.init_color_pairs()
        curses.setsyx(-1, -1)

    def start(self):
        """Start TextUI"""
        screen_height, screen_width = self.get_screen_size()
        titlebar = TitleBar(1, screen_width, events=self.events)
        statusbar = StatusBar(1, screen_width, screen_height - 1, 0, self.events)
        if curses.has_colors:
            titlebar.set_background_color(13)
        titlebar.initial_render()
        statusbar.initial_render()
        try:
            while not self.stop_event.is_set():
                message = self.fetch_message()
                if message is not None:
                    if "event" in message and "data" in message:
                        self.events.notify_observers(message["event"], message["data"])
                    else:
                        self.events.notify_observers("generic", message)
                self.emit_time()
                sleep(0.05)

        except KeyboardInterrupt:
            pass  # It's OK since we would only set stop_event flag here anyway
        finally:
            self.stop()

    def stop(self):
        self.stop_event.set()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def get_screen_size(self):
        """Get screen size"""
        curses.update_lines_cols()
        return curses.LINES, curses.COLS

    def emit_time(self):
        """Emits current time to observers"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        self.events.notify_observers("formatted-time-update", current_time)

    def init_color_pairs(self):
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(14, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(15, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(16, curses.COLOR_BLACK, curses.COLOR_CYAN)
