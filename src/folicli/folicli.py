#!/usr/bin/python3

import logging
import logging.handlers
import multiprocessing as mp
from logging.handlers import SysLogHandler
from time import sleep

from fetcher.foli import FoliFetcher
from messagebroker import MessageBroker
from ui.textui import TextUI


def main():
    logger = setup_logging()
    logger.info("Starting Föli-CLI")

    stop_event = mp.Event()

    broker = MessageBroker(stop_event)
    pub_queue = broker.get_publish_queue()

    ui = TextUI(stop_event, pub_queue, broker.get_new_subscriber_queue())
    fetcher = FoliFetcher(stop_event, pub_queue, broker.get_new_subscriber_queue())

    started = start_processes(broker, ui, fetcher)

    try:
        logger.debug("Starting main loop")
        while not stop_event.is_set():
            sleep(0.1)
            if check_for_dead(started):
                stop_event.set()
        logger.debug("Stopping main loop")

    except KeyboardInterrupt:
        logger.debug("Got KeyboardInterrupt")
        stop_event.set()
    finally:
        logger.info("Stopping Föli-CLI")
        for process in started:
            process.join()
            process.close()


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


def setup_logging():
    """Setup global logging

    Returns logger instance
    """
    logger = logging.getLogger("foli-cli")
    logger.setLevel(logging.DEBUG)

    syslog_formatter = logging.Formatter("%(name)s [%(levelname)s]: %(message)s")
    syslog_handler = logging.handlers.SysLogHandler(
        facility=SysLogHandler.LOG_LOCAL0, address="/dev/log"
    )
    syslog_handler.setLevel(logging.DEBUG)
    syslog_handler.setFormatter(syslog_formatter)

    logger.addHandler(syslog_handler)

    return logger


if __name__ == "__main__":
    main()
