#!/usr/bin/python3

import multiprocessing as mp
from time import sleep

from ui.textui import TextUI
from observable import Observable
from fetcher.foli import FoliFetcher

if __name__ == '__main__':
  stop_event = mp.Event()

  broker = Observable()
  ui = TextUI(stop_event, broker)
  fetcher = FoliFetcher(stop_event, broker)

  ui_process = mp.Process(target=ui.start)
  fetcher_process = mp.Process(target=fetcher.start)

  ui_process.start()
  fetcher_process.start()

  i = 0

  try:
    while not stop_event.is_set():
      sleep(0.1)
      if not ui_process.is_alive() or not fetcher_process.is_alive():
        stop_event.set()

      i += 1
      if i % 40 == 0:
        broker.notify_observers('line_selection_update')

  except KeyboardInterrupt:
    stop_event.set()

  print('Stopping...')

  ui_process.join()
  fetcher_process.join()

  ui_process.close()
  fetcher_process.close()
