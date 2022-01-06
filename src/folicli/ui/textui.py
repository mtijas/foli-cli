from multiprocessing import current_process
from time import sleep
import curses

from messagebroker import Subscriber, Publisher
from ui.tui.blocks.titlebar import TitleBar
from ui.tui.blocks.statusbar import StatusBar
from ui.observable import Observable

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
        curses.setsyx(-1, -1)

    def start(self):
        '''Start TextUI'''
        screen_height, screen_width = self.get_screen_size()
        titlebar = TitleBar(1, screen_width)
        statusbar = StatusBar(screen_height-1, 30, 1, screen_width-30, self.events)
        titlebar.initial_render()
        statusbar.initial_render()
        try:
            while not self.stop_event.is_set():

                message = self.fetch_message()
                if message is not None:
                    if 'event' in message and 'data' in message:
                        self.events.notify_observers(message['event'], message['data'])
                    else:
                        self.events.notify_observers('generic', message)

                sleep(0.05)

        except KeyboardInterrupt:
            pass # It's OK since we would only set stop_event flag here anyway
        finally:
            self.stop()

    def stop(self):
        self.stop_event.set()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def get_screen_size(self):
        '''Get screen size'''
        curses.update_lines_cols()
        return curses.LINES, curses.COLS
