from multiprocessing import current_process
from time import sleep

from observable import Observer

class TextUI(Observer):
  def __init__(self, stop_event, broker):
    self.stop_event = stop_event
    self.broker = broker

  def start(self):
    '''Start TextUI'''
    self.broker.register_observer('fetch_completed', self)

    i = 1
    name = current_process().name

    try:
      while not self.stop_event.is_set():
        print(f'TextUI is running as {name}, lap {i}')
        sleep(1)
        i += 1
    except KeyboardInterrupt:
      self.stop_event.set()

  def notify(self, event, data):
    print(f'TextUI got event {event} with {data}')
