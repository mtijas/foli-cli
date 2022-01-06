from multiprocessing import current_process
from time import sleep

from messagebroker import Subscriber, Publisher

class TextUI(Subscriber, Publisher):
    def __init__(self, stop_event, pub_queue, sub_queue):
        self.stop_event = stop_event
        Publisher.__init__(self, pub_queue)
        Subscriber.__init__(self, sub_queue)

    def start(self):
        '''Start TextUI'''
        i = 1
        name = current_process().name

        try:
            while not self.stop_event.is_set():
                print(f'TextUI is running as {name}, lap {i}')
                sleep(1)

                message = self.fetch_message()
                if message is not None:
                    print(f'TextUI got {message}')

                i += 1
                if i > 30:
                    self.stop_event.set()
        except KeyboardInterrupt:
            self.stop_event.set()

    def notify(self, event, data):
        print(f'TextUI got event {event} with {data}')
