from typing import Tuple
from screeninfo import get_monitors

class MonitorInfo:
    def __init__(self) -> None:
        self.width = None
        self.height = None

    def getMonitorDimensions(self) -> Tuple[int, int]:
        for monitor in get_monitors():
            if monitor.is_primary:
                self.width = monitor.width
                self.height = monitor.height
        return self.width, self.height