import common

from enum import Enum
from behaviortree.behavior import Status, Behavior
from behaviortree.composite import Sequence, Selector, ActiveSelector
from behaviortree.decorator import Repeat
from behaviortree.trace import dump_tree

# demonstrate a basic tree
"""
- BasicTree[ActiveSelector]
    |> Sleep
    |@ Work[Repeat]
        |- ChopCycle[Sequence]
            |> Chop
            |> Haul
"""

class SleepAction(Behavior):
    def __init__(self, requiredSleep: int):        
        super().__init__(None)
        self._requiredSleep: int = requiredSleep

    def on_initialize(self):
        self._slept = 0

    def update(self) -> Status:
        bb = self.get_blackboard()
        if bb["energy"] > 4: return Status.FAILURE # only sleep if tired
        self._slept += 1
        if self._slept >= self._requiredSleep: # if we slept our required hours, we're done
            bb["energy"] = 16 # we're well rested
            return Status.SUCCESS
        return Status.RUNNING

class ChopAction(Behavior):
    def __init__(self, capacity: int):
        super().__init__(None)
        self._capacity = capacity

    def update(self) -> Status:
        bb = self.get_blackboard()
        if bb["energy"] <= 0: return Status.FAILURE # we're too tired
        bb["energy"] -= 1 # chopping wood is boring and tiring
        bb["wood"] += 1 # grab another piece of wood
        if bb["wood"] >= self._capacity: # if we're at capacity, we're done
            return Status.SUCCESS
        return Status.RUNNING

class HaulAction(Behavior):
    def __init__(self):
        super().__init__(None)

    def update(self) -> Status:
        bb = self.get_blackboard()
        bb["money"] += bb["wood"] # each wood gives one money unit
        bb["wood"] = 0 # deposit the wood
        return Status.SUCCESS

def build_tree() -> Behavior:
    # blackboard
    blackboard = {
        "energy": 16,
        "wood": 0,
        "money": 0
    }

    # root
    tree_root = ActiveSelector("Root")
    tree_root.set_blackboard(blackboard)

    # sleep
    leaf_sleep = SleepAction(8)

    # work
    leaf_chop = ChopAction(4)
    leaf_haul = HaulAction()
    tree_work = Sequence("ChopCycle")
    tree_work.add_child(leaf_chop)
    tree_work.add_child(leaf_haul)
    tree_work_repeat = Repeat(tree_work, -1, "Work")

    # finish root
    tree_root.add_child(leaf_sleep)
    tree_root.add_child(tree_work_repeat)

    return tree_root

# execute the tree
tree = build_tree()
dump_tree(tree)
tree.set_trace(True) # enable call chain tracing
tick_count = 0
while not tree.is_terminated():
    tree.begin_trace() # clear the call chain list before we tick
    result = tree.tick()
    tick_count += 1
    # condense the call chain in to a list of node names (n -> n.name)
    chain = list(map(lambda n: n._name, tree._call_chain))
    # log the executing leaf node and status
    print(f"tick[{tick_count}] {chain[-1]}: {result}")
    print(f"    CallChain {chain}")
    print()

print(tree.get_blackboard())