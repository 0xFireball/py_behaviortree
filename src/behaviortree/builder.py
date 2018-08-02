from behaviortree.behavior import Behavior
from behaviortree.composite import Composite, Selector, Sequence, Parallel, ParallelSelector, ActiveSelector
from behaviortree.decorator import Repeat
from typing import List

class BehaviorTreeBuilder:
    def __init__(self):
        self._stack = []
        self._decorators = []

    def action(self, action: Behavior):
        self._stack[-1].add_child(action)

    def selector(self, name: str):
        self._stack.append(Selector(name))

    def sequence(self, name: str):
        self._stack.append(Sequence(name))

    def parallel(self, name: str, policy: int):
        self._stack.append(Parallel(name, policy))

    def parallelSelector(self, name: str):
        self._stack.append(ParallelSelector(name))

    def activeSelector(self, name: str):
        self._stack.append(ActiveSelector(name))

    def composite(self, composite: Composite):
        self._stack.append(composite)

    def decorator(self, type, name: str, *args):
        self._decorators.append((type, name, args))

    def decorate(self):
        (dec, name, args) = self._decorators.pop()
        child = self._stack.pop()
        self._stack.append(dec(name, child, *args))

    def endComposite(self):
        child = self._stack.pop()
        # peek the next item in the stack and add the child to it
        self._stack[-1].add_child(child)

    def build(self) -> Behavior:
        return self._stack.pop()
