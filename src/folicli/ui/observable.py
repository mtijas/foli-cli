from abc import ABC, abstractmethod

class Observer(ABC):
    '''Observer for any Observable'''

    @abstractmethod
    def notify(self, event:str, data):
        pass


class Observable():
    def __init__(self):
        self.observers = dict()

    def register_observer(self, event: str, observer: Observer):
        if event not in self.observers:
            self.observers[event] = []

        if observer not in self.observers[event]:
            self.observers[event].append(observer)

    def deregister_observer(self, event: str, observer: Observer):
        if observer in self.observers[event]:
            self.observers[event].remove(observer)

    def notify_observers(self, event, data=None):
        if event not in self.observers:
            return

        for observer in self.observers[event]:
            observer.notify(event, data)
