from multiprocessing import current_process
from time import sleep

from observable import Observer

class FoliFetcher(Observer):
  def __init__(self, stop_event, broker):
    self.stop_event = stop_event
    self.broker = broker

  def start(self):
    '''Start FoliFetcher'''
    self.broker.register_observer('line_selection_update', self)

    i = 1
    name = current_process().name

    try:
      while not self.stop_event.is_set():
        print(f'FoliFetcher is running as {name}, lap {i}')
        sleep(2.5)
        i += 1
        self.broker.notify_observers('fetch_completed')
    except KeyboardInterrupt:
      self.stop_event.set()

  def notify(self, event, data):
    print(f'FoliFetcher got event {event} with {data}')
