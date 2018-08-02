from behaviortree.behavior import Status, Behavior

class Decorator(Behavior):
    def __init__(self, child: Behavior, name: str):
        super().__init__(name)
        child._parent = self
        self._child: Behavior = child

class Repeat(Decorator):
    def __init__(self, child: Behavior, limit: int, name: str):
        super().__init__(child, name)
        self._limit = limit
        self._counter = 0

    def on_initialize(self):
        self._counter = 0

    def update(self) -> Status:
        self._child.tick()
        if self._child.getStatus() == Status.RUNNING: return Status.RUNNING
        if self._child.getStatus() == Status.FAILURE: return Status.FAILURE
        self._counter += 1
        if self._counter == self._limit: return Status.SUCCESS
        self._child.reset()
        return Status.RUNNING

    def set_count(self, count: int):
        self._limit = count
