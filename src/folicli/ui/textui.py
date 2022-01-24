import curses
import logging
from datetime import datetime
from multiprocessing import current_process
from time import sleep

from messagebroker import Publisher, Subscriber
from observable import Observable

from ui.tui.blocks.header import Header
from ui.tui.blocks.statusbar import StatusBar


class TextUI(Subscriber, Publisher):
    def __init__(self, stop_event, pub_queue, sub_queue):
        self._logger = logging.getLogger("foli-cli.ui.textui.TextUi")
        self.stop_event = stop_event
        self.events = Observable()
        self.blocks = {}

        Publisher.__init__(self, pub_queue)
        Subscriber.__init__(self, sub_queue)
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        if curses.has_colors:
            curses.start_color()
            curses.use_default_colors()
            self.init_color_pairs()
        curses.setsyx(-1, -1)

    def start(self):
        """Start TextUI"""
        resize_timer = 0
        resize_required = False
        screen_height, screen_width = self.get_screen_size()
        header = Header(screen_width, observable=self.events)
        statusbar = StatusBar(
            1, screen_width, screen_height - 1, 0, observable=self.events
        )

        self.blocks["header"] = header
        self.blocks["statusbar"] = statusbar

        header.getch()  # Quick'n'dirty fix for first getch clearing window

        for block in self.blocks.values():
            block.initial_render()

        try:
            self._logger.debug("Starting TextUI main loop")
            while not self.stop_event.is_set():
                self.pass_messagebroker_events()
                self.emit_time()

                c = header.getch()
                if c == curses.KEY_RESIZE:
                    resize_timer = 0
                    resize_required = True
                elif c == ord("q"):
                    self.stop_event.set()

                for block in self.blocks.values():
                    block.refresh()

                if resize_required:
                    if resize_timer >= 3:
                        self.resize()
                        resize_required = False
                    resize_timer += 1

                sleep(0.1)
            self._logger.debug("Stopping TextUI main loop")

        except KeyboardInterrupt:
            self._logger.debug("Got KeyboardInterrupt")
            pass  # It's OK since we would only set stop_event flag here anyway
        finally:
            self.stop()

    def stop(self):
        """Stop operations reverting terminal"""
        self.stop_event.set()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def get_screen_size(self):
        """Get screen size"""
        curses.update_lines_cols()
        return curses.LINES, curses.COLS

    def resize(self):
        height, width = self.get_screen_size()
        self.stdscr.clear()
        self.stdscr.refresh()
        self.blocks["header"].resize(1, width)
        self.blocks["statusbar"].resize(1, width)
        self.blocks["statusbar"].move(height - 1, 0)

    def pass_messagebroker_events(self):
        """Pass events fetched from MessageBroker queue to event observers"""
        message = self.fetch_message()
        if message is None:
            return
        if "event" in message and "data" in message:
            self.events.notify_observers(message["event"], message["data"])
        else:
            self.events.notify_observers("generic", message)

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
