from enum import Enum

class Status(Enum):
    INVALID     = 0
    SUCCESS     = 1
    FAILURE     = 2
    RUNNING     = 3
    ABORTED     = 4

class Behavior:
    def __init__(self, name: str):
        if (name == None):
            name = self.__class__.__name__
        self._status = Status.INVALID
        self._name: str = name
        self._parent = None
        self._blackboards = {}
        # tracing
        self._call_chain = None

    def set_blackboard(self, data, name: str = ''):
        self._blackboards[name] = data

    def get_blackboard(self, name: str = ''):
        if name in self._blackboards: return self._blackboards[name]
        return self._parent.get_blackboard(name)

    # enable tracing for this node (and below)
    def set_trace(self, trace: bool):
        if trace:
            self._call_chain = []
        else:
            self._call_chain = None
    
    def begin_trace(self): # reset the call chain
        if self._call_chain != None:
            self._call_chain = []


    def trace(self): # add the current node to the call chain list
        chain = self._get_call_chain()
        if chain != None:
            chain.append(self)

    # bubble up to get the call chain at the closest parent with tracing enabled
    def _get_call_chain(self):
        if self._call_chain != None: return self._call_chain
        return self._parent._get_call_chain()

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
        self.trace() # for tracing the execution
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
