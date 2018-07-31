from behavior import Status, Behavior
from typing import List

class Composite(Behavior):
    _children: List[Behavior] = []

    def add_child(self, child: Behavior):
        self._children.append(child)

    def remove_child(self, child: Behavior):
        self._children.remove(child)

    def clear(self):
        self._children.clear()

class Sequence(Composite):
    _currentChild: int

    def onInitialize(self):
        self._currentChild = 0

    def update(self) -> Status:
        while True:
            childStatus: Status = self._children[self._currentChild].tick()
            # if a child failed, we failed
            if childStatus != Status.SUCCESS: return childStatus
            self._currentChild += 1
            # if we reached the end, we're done
            if self._currentChild == len(self._children): return Status.SUCCESS

class Selector(Composite):
    _currentChild: int

    def onInitialize(self):
        self._currentChild = 0

    def update(self) -> Status:
        while True:
            childStatus: Status = self._children[self._currentChild].tick()
            # if a child didn't fail, we're done
            if childStatus != Status.FAILURE: return childStatus
            self._currentChild += 1
            # if we reached the end without any completion, fail
            if self._currentChild == len(self._children): return Status.FAILURE

# TODO: Parallel Composite
# TODO: Monitor Composite

class ActiveSelector(Selector):
    def update(self) -> Status:
        previous: int = self._currentChild # store the current child
        super().onInitialize() # reset current to beginning
        result: Status = super().update() # run all nodes to possibly get a new current child
        # if previous isn't the end, and our new current differs from previous, terminate the previous
        if previous != len(self._children) - 1 and self._currentChild != previous: self._children[previous].onTerminate(Status.ABORTED)
        return result
