#!/usr/bin/python3

import multiprocessing as mp
from time import sleep

from ui.textui import TextUI
from messagebroker import MessageBroker
from fetcher.foli import FoliFetcher


def main():
    print("Starting Föli-CLI...")

    stop_event = mp.Event()

    broker = MessageBroker(stop_event)
    pub_queue = broker.get_publish_queue()

    ui = TextUI(stop_event, pub_queue, broker.get_new_subscriber_queue())
    fetcher = FoliFetcher(stop_event, pub_queue, broker.get_new_subscriber_queue())

    started = start_processes(broker, ui, fetcher)

    try:
        while not stop_event.is_set():
            sleep(0.1)
            if check_for_dead(started):
                stop_event.set()

    except KeyboardInterrupt:
        stop_event.set()
    finally:
        for process in started:
            process.join()
            process.close()
        print("Good bye!")


def start_processes(*args):
    """Start arguments as multiprocessing Processes"""
    started = []
    for target in args:
        process = mp.Process(target=target.start)
        process.start()
        started.append(process)
    return started


def check_for_dead(processes):
    """Checks if any process has died

    Arguments:
    processes -- List of multiprocessing.Processes to check
    """
    for process in processes:
        if not process.is_alive():
            return True
    return False


if __name__ == "__main__":
    main()
