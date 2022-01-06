import multiprocessing
import unittest
from unittest.mock import Mock
from time import sleep

from src.folicli.observable import Observable, Observer

class DummyObserver(Observer):
  def __init__(self, stop_event, broker):
    self.stop_event = stop_event
    self.broker = broker
    self.notify_called = False

  def start(self):
    self.broker.register_observer('event', self)
    print(self.broker.observers)

    try:
      while not self.stop_event.is_set():
        sleep(1)
    except KeyboardInterrupt:
      self.stop_event.set()

  def notify(self, event, data):
    self.notify_called = True


class TestObservableIntegration(unittest.TestCase):
  def test_register_from_threads(self):
    '''All processes should be able to register to single Observable'''
    stop_event = multiprocessing.Event()
    observable = Observable()
    observer1 = DummyObserver(stop_event, observable)
    observer2 = DummyObserver(stop_event, observable)

    o1_process = multiprocessing.Process(target=observer1.start)
    o2_process = multiprocessing.Process(target=observer2.start)

    o1_process.start()
    o2_process.start()

    sleep(0.1)

    registered_observers = observable.observers
    print(observable.observers)

    stop_event.set()

    o1_process.join()
    o2_process.join()

    o1_process.close()
    o2_process.close()

    self.assertIn('event', registered_observers)
    if 'event' in registered_observers:
      self.assertIn(observer1, registered_observers)
      self.assertIn(observer2, registered_observers)
