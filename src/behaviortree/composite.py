from behaviortree.behavior import Status, Behavior
from typing import List

class Composite(Behavior):
    def __init__(self,  name: str):
        super().__init__(name)
        self._children: List[Behavior] = []

    def add_child(self, child: Behavior):
        child._parent = self
        self._children.append(child)

    def remove_child(self, child: Behavior):
        child._parent = None
        self._children.remove(child)

    def clear(self):
        for child in self._children:
            self.remove_child(child)

class Sequence(Composite):
    def __init__(self,  name: str):
        super().__init__(name)
        self._currentChild: int

    def on_initialize(self):
        self._currentChild = 0

    def update(self) -> Status:
        childStatus: Status = self._children[self._currentChild].tick()
        # if a child failed, we failed
        if childStatus != Status.SUCCESS: return childStatus
        self._currentChild += 1
        # if we reached the end, we're done
        if self._currentChild == len(self._children): return Status.SUCCESS
        return Status.RUNNING

class Selector(Composite):
    def __init__(self,  name: str):
        super().__init__(name)
        self._currentChild: int

    def on_initialize(self):
        self._currentChild = 0

    def update(self) -> Status:
        childStatus: Status = self._children[self._currentChild].tick()
        # if a child didn't fail, we're done
        if childStatus != Status.FAILURE: return childStatus
        self._currentChild += 1
        # if we reached the end without any completion, fail
        if self._currentChild == len(self._children): return Status.FAILURE
        return Status.RUNNING

class Parallel(Composite):
    REQUIRE_ONE = 0
    REQUIRE_ALL = 1

    def __init__(self,  name: str, policy: int):
        super().__init__(name)
        self._policy = policy

    def on_initialize(self):
        self._currentChild = 0

    def update(self) -> Status:
        successes   = 0
        failures    = 0
        for child in self._children:
            if not child.is_terminated():
                child.tick()
            if child._status == Status.SUCCESS:
                successes += 1
                if self._policy == Parallel.REQUIRE_ONE:
                    return Status.SUCCESS
            if child._status == Status.FAILURE:
                failures += 1
                if self._policy == Parallel.REQUIRE_ALL:
                    return Status.FAILURE

        if self._policy == Parallel.REQUIRE_ALL:
            if successes + failures == len(self._children):
                return Status.FAILURE
            if successes == len(self._children):
                return Status.SUCCESS

        return Status.RUNNING

class ParallelSelector(Composite):
    def __init__(self,  name: str):
        super().__init__(name)
        self._currentChild: int

    def on_initialize(self):
        self._currentChild = 0

    def update(self) -> Status:
        while True:
            childStatus: Status = self._children[self._currentChild].tick()
            # if a child didn't fail, we're done
            if childStatus != Status.FAILURE: return childStatus
            self._currentChild += 1
            # if we reached the end without any completion, fail
            if self._currentChild == len(self._children): return Status.FAILURE

class ActiveSelector(ParallelSelector):
    def __init__(self, name: str):
        super().__init__(name)

    def update(self) -> Status:
        previous: int = self._currentChild # store the current child
        super().on_initialize() # reset current to beginning
        result: Status = super().update() # run all nodes to possibly get a new current child
        # if previous isn't the end, and our new current differs from previous, terminate the previous
        if previous != len(self._children) - 1 and self._currentChild != previous: self._children[previous].abort()
        return result
