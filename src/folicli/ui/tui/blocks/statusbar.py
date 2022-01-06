from ui.tui.components.window import Window
from ui.observable import Observable, Observer


class StatusBar(Window, Observer):
    def __init__(self, height:int, width:int, y:int=0, x:int=0, events:Observable=None):
        super().__init__(height, width, y, x)
        self.events = events
        self.events.register_observer('status-update', self)

    def initial_render(self):
        self.notify('initial', 'Nothing yet...')

    def notify(self, event:str, data):
        self.window.clear()
        self.add_str(0, 1, data)
        self.window.refresh()


