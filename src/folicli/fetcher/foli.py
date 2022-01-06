from multiprocessing import current_process
from time import sleep

from messagebroker import Subscriber, Publisher

class FoliFetcher(Subscriber, Publisher):
    def __init__(self, stop_event, pub_queue, sub_queue):
        self.stop_event = stop_event
        Publisher.__init__(self, pub_queue)
        Subscriber.__init__(self, sub_queue)

    def start(self):
        '''Start FoliFetcher'''

        i = 1
        name = current_process().name

        try:
            while not self.stop_event.is_set():
                sleep(0.1)
                i += 1

                if i == 20:
                    self.publish_message('FoliFetcher fetched something')

        except KeyboardInterrupt:
            self.stop_event.set()

