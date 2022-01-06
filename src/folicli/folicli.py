#!/usr/bin/python3

import multiprocessing as mp
from time import sleep

from ui.textui import TextUI
from messagebroker import MessageBroker
from fetcher.foli import FoliFetcher

if __name__ == '__main__':
    stop_event = mp.Event()

    broker = MessageBroker(stop_event)

    tui_publish_queue = broker.get_publisher_queue()
    tui_subscribe_queue = broker.get_subscriber_queue()
    ui = TextUI(stop_event, tui_publish_queue, tui_subscribe_queue)

    fetcher_publish_queue = broker.get_publisher_queue()
    fetcher_subscribe_queue = broker.get_subscriber_queue()
    fetcher = FoliFetcher(stop_event, fetcher_publish_queue, fetcher_subscribe_queue)

    broker_process = mp.Process(target=broker.start)
    ui_process = mp.Process(target=ui.start)
    fetcher_process = mp.Process(target=fetcher.start)

    broker_process.start()
    ui_process.start()
    fetcher_process.start()

    try:
        while not stop_event.is_set():
            sleep(0.1)
            if not ui_process.is_alive() or not fetcher_process.is_alive() \
              or not broker_process.is_alive():
                stop_event.set()

    except KeyboardInterrupt:
        stop_event.set()

    print('Stopping...')

    ui_process.join()
    fetcher_process.join()
    broker_process.join()

    ui_process.close()
    fetcher_process.close()
    broker_process.close()
