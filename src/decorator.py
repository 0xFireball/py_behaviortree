from behavior import Status, Behavior

class Decorator(Behavior):
    def __init__(self, child: Behavior, name: str):
        super().__init__(name)
        self._child: Behavior = child

class Repeat(Decorator):
    def __init__(self,  name: str):
        self._limit = 0
        self._counter = 0

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
