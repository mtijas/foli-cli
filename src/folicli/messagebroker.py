from abc import ABC, abstractmethod
from multiprocessing import Queue
import queue
from time import sleep

class Subscriber():
    def __init__(self, queue):
        self.receive_queue = queue

    def fetch_message(self):
        '''Tries to get data from the Queue

        Returns data if able, None otherwise
        '''
        if self.receive_queue.empty():
            return None

        try:
            return self.receive_queue.get_nowait()
        except queue.Empty:
            return None # Empty queue is OK


class Publisher():
    def __init__(self, queue):
        self.publish_queue = queue

    def publish_message(self, data):
        '''Forwards data blob to every the queue'''
        self.publish_queue.put_nowait(data)


class MessageBroker():
    '''Message Broker for interprocess communication

    A broker for passing messages from publish queues to every subscriber queue.

    Methods:
    attach_publisher -- Attach a Queue for publishing messages to broker.
    detach_publisher -- Detach a publishing Queue from the broker.
    attach_subscriber -- Attach a subscriber Queue to which we propagate messages.
    detach_subscriber -- Detach a subscriber Queue from the broker.
    run -- Starts the broker (the primary listening-forwarding loop).
    '''
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.subscribers = []
        self.publishers = []

    def attach_publisher(self, publisher: Queue):
        '''Attach a publisher queue to broker'''
        if publisher not in self.publishers:
            self.publishers.append(publisher)

    def detach_publisher(self, publisher: Queue):
        '''Detach a publisher queue from broker'''
        if publisher in self.publishers:
            self.publishers.remove(publisher)

    def attach_subscriber(self, subscriber: Queue):
        '''Attach a subscriber queue to broker'''
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def detach_subscriber(self, subscriber: Queue):
        '''Detach a subscriber queue from broker'''
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def get_publisher_queue(self) -> Queue:
        '''Creates a new publisher queue, attachs it and returns it'''
        queue = Queue()
        self.attach_publisher(queue)
        return queue

    def get_subscriber_queue(self) -> Queue:
        '''Creates a new subscriber queue, attachs it and returns it'''
        queue = Queue()
        self.attach_subscriber(queue)
        return queue

    def start(self):
        '''Start the publish-subscribe message transfer loop'''
        try:
            while not self.stop_event.is_set():
                for publisher in self.publishers:
                    data = self._get_data(publisher)
                    if data is not None:
                        self._forward_data(data)
                sleep(0.1)
        except KeyboardInterrupt:
            self.stop_event.set()

    def _get_data(self, publisher: Queue):
        '''Tries to get data from a publisher Queue

        Returns data if able, None otherwise
        '''
        if publisher.empty():
            return None

        try:
            return publisher.get_nowait()
        except queue.Empty:
            return None # Empty queue is OK

    def _forward_data(self, data):
        '''Forwards data blob to every subscriber queue'''
        for subscriber in self.subscribers:
            subscriber.put_nowait(data)
