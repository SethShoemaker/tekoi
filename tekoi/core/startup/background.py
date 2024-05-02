from abc import ABC as _ABC

class BackgroundService(_ABC):

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass


class BackgroundServiceDefinition(_ABC):
    
    def __init__(self, cls: type[BackgroundService]):
        self.cls = cls
