from multiprocessing import current_process
from time import sleep
import curses

from messagebroker import Subscriber, Publisher

class TextUI(Subscriber, Publisher):
    def __init__(self, stop_event, pub_queue, sub_queue):
        self.stop_event = stop_event
        Publisher.__init__(self, pub_queue)
        Subscriber.__init__(self, sub_queue)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def start(self):
        '''Start TextUI'''
        name = current_process().name

        try:
            while not self.stop_event.is_set():
                sleep(0.1)

                message = self.fetch_message()
                if message is not None:
                    self.stdscr.addstr(0, 0, f'TextUI got {message}')

                self.stdscr.refresh()

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
