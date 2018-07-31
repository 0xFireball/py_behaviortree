from behavior import Status, Behavior

class Decorator(Behavior):
    _child: Behavior = None

    def __init__(self, child: Behavior):
        self._child = child

class Repeat(Decorator):
    _limit = 0
    _counter = 0

    def onInitialize(self):
        self._counter = 0

    def update(self) -> Status:
        while True:
            _child.tick()
            if _child.getStatus() == Status.RUNNING break
            if _child.getStatus() == Status.FAILURE return Status.FAILURE
            self._counter += 1
            if self._counter == self._limit return Status.SUCCESS
            _child.reset()
        return Status.INVALID

    def setCount(self, count: int):
        self._limit = count
