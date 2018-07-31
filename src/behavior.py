from enum import Enum

class Status(Enum):
    INVALID     = 0
    SUCCESS     = 1
    FAILURE     = 2
    RUNNING     = 3
    ABORTED     = 4

class Behavior:
    _status = Status.INVALID

    # abstract update
    def update(self) -> Status:
        return Status.INVALID

    def onInitialize(self):
        pass

    def onTerminate(self, status: Status):
        pass
    
    def tick(self) -> Status:
        if self._status != Status.RUNNING:
            self.onInitialize()
        self._status = self.update()
        if self._status != Status.RUNNING:
            self.onTerminate(self._status)
        return self._status

    def reset(self):
        self._status = Status.INVALID

    def abort(self):
        self._status = Status.ABORTED
        self.onTerminate(Status.ABORTED)

    def isTerminated(self) -> bool:
        return self._status == Status.SUCCESS | self._status == Status.FAILURE
    
    def isRunning(self) -> bool:
        return self._status == Status.RUNNING

    def getStatus(self) -> Status:
        return self._status
