from behavior import Status, Behavior

class Decorator(Behavior):
    _child: Behavior = None

    def __init__(self, child: Behavior):
        self._child = child

class Repeat(Decorator):
    _limit = 0
    _counter = 0

    def on_initialize(self):
        self._counter = 0

    def update(self) -> Status:
        while True:
            self._child.tick()
            if self._child.getStatus() == Status.RUNNING: break
            if self._child.getStatus() == Status.FAILURE: return Status.FAILURE
            self._counter += 1
            if self._counter == self._limit: return Status.SUCCESS
            self._child.reset()
        return Status.INVALID

    def set_count(self, count: int):
        self._limit = count
