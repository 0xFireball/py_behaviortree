from enum import Enum

class Status(Enum):
    INVALID     = 0
    SUCCESS     = 1
    FAILURE     = 2
    RUNNING     = 3
    ABORTED     = 4

class Behavior:
    _status: Status = Status.INVALID
    _name: str

    def __init__(self, name=None):
        if (name == None):
            name = self.__class__.__name__
        self._name = name

    # abstract update
    def update(self) -> Status:
        return Status.INVALID

    def on_initialize(self):
        pass

    def on_terminate(self, status: Status):
        pass
    
    def tick(self) -> Status:
        if self._status != Status.RUNNING:
            self.on_initialize()
        self._status = self.update()
        if self._status != Status.RUNNING:
            self.on_terminate(self._status)
        return self._status

    def reset(self):
        self._status = Status.INVALID

    def abort(self):
        self._status = Status.ABORTED
        self.on_terminate(Status.ABORTED)

    def is_terminated(self) -> bool:
        return self._status == Status.SUCCESS or self._status == Status.FAILURE
    
    def is_running(self) -> bool:
        return self._status == Status.RUNNING

    def getStatus(self) -> Status:
        return self._status
