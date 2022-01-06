from multiprocessing import Queue, Event
import unittest
from unittest.mock import Mock
import unittest.mock as mock

from src.folicli.messagebroker import MessageBroker, Publisher, Subscriber


class TestMessageBroker(unittest.TestCase):
    @mock.patch('multiprocessing.Event')
    def setUp(self, mock_event):
        self.subscriber_count = 10
        self.publisher_count = 10
        self.stop_event = mock_event
        # Stop message broker after fifth round
        self.stop_event.is_set.side_effect = [False, False, False, False, True]
        self.broker = MessageBroker(self.stop_event)

        self.subscriber_queues = []
        for i in range(self.subscriber_count):
            self.subscriber_queues.append(Mock())

        self.publisher_queues = []
        for i in range(self.publisher_count):
            q = Mock()
            q.get_nowait.side_effect = [{1}, {2}, {3}]
            q.empty.side_effect = [False, False, False, True]
            self.publisher_queues.append(q)

    def test_attach_publisher_queues(self):
        '''Publisher queues should be able to be attached'''
        for q in self.publisher_queues:
            self.broker.attach_publisher(q)

        for q in self.publisher_queues:
            self.assertIn(q, self.broker.publishers)

    def test_detach_publisher_queues(self):
        '''Publisher queues should be able to be detached'''
        for q in self.publisher_queues:
            self.broker.attach_publisher(q)

        self.broker.detach_publisher(self.publisher_queues[0])

        self.assertNotIn(self.publisher_queues[0], self.broker.publishers)

    def test_attach_subscriber_queues(self):
        '''Subscriber queues should be able to be attached'''
        for q in self.subscriber_queues:
            self.broker.attach_subscriber(q)

        for q in self.subscriber_queues:
            self.assertIn(q, self.broker.subscribers)

    def test_detach_subscriber_queues(self):
        '''Subscriber queues should be able to be detached'''
        for q in self.subscriber_queues:
            self.broker.attach_subscriber(q)

        self.broker.detach_subscriber(self.subscriber_queues[0])

        self.assertNotIn(self.subscriber_queues[0], self.broker.subscribers)

    def test_message_passing(self):
        '''Test message passing from publish queue to subscribe queues'''
        for q in self.subscriber_queues:
            self.broker.attach_subscriber(q)
        for q in self.publisher_queues:
            self.broker.attach_publisher(q)

        self.broker.start()

        for q in self.subscriber_queues:
            self.assertEqual(30, q.put_nowait.call_count)

    def test_getting_publisher_queue(self):
        '''Publisher queue should be added and returned'''
        result = self.broker.get_publisher_queue()

        self.assertIn(result, self.broker.publishers)
        self.assertNotIn(result, self.broker.subscribers)

    def test_getting_subscriber_queue(self):
        '''Subscriber queue should be added and returned'''
        result = self.broker.get_subscriber_queue()

        self.assertNotIn(result, self.broker.publishers)
        self.assertIn(result, self.broker.subscribers)
