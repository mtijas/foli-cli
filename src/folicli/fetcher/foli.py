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
                print(f'FoliFetcher is running as {name}, lap {i}')
                sleep(1.1)
                i += 1

                if i == 2:
                    self.publish_message('FoliFetcher fetched something')

                message = self.fetch_message()
                if message is not None:
                    print(f'FoliFetcher got {message}')

        except KeyboardInterrupt:
            self.stop_event.set()

