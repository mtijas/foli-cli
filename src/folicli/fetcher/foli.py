import logging
from multiprocessing import current_process
from time import sleep

from messagebroker import Publisher, Subscriber


class FoliFetcher(Subscriber, Publisher):
    def __init__(self, stop_event, pub_queue, sub_queue):
        self.stop_event = stop_event
        Publisher.__init__(self, pub_queue)
        Subscriber.__init__(self, sub_queue)
        self._logger = logging.getLogger("foli-cli.fetcher.foli.FoliFetcher")

    def start(self):
        """Start FoliFetcher"""

        i = 1
        name = current_process().name

        try:
            self._logger.debug("Starting FoliFetcher main loop")
            while not self.stop_event.is_set():
                sleep(0.1)
                i += 1

                if i == 20:
                    self.publish_message(
                        {
                            "event": "polling-interval-update",
                            "data": 3,
                        }
                    )
            self._logger.debug("Stopping FoliFetcher main loop")

        except KeyboardInterrupt:
            self._logger.debug("Got KeyboardInterrupt")
            self.stop_event.set()
