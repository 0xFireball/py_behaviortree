import common
from common import parse_executing, crunch_status

from enum import Enum
from behaviortree.behavior import Status, Behavior
from behaviortree.composite import Sequence, Selector, ActiveSelector, Parallel
from behaviortree.decorator import Repeat
from behaviortree.trace import dump_tree
from behaviortree.builder import BehaviorTreeBuilder

class VacationAction(Behavior):
    def __init__(self, cost):
        super().__init__(None)
        self.cost = cost

    def update(self) -> Status:
        bb = self.get_blackboard()
        if bb["coins"] < self.cost: return Status.FAILURE
        bb["coins"] -= self.cost
        return Status.SUCCESS

class BuyCarAction(Behavior):
    def __init__(self, cost):
        super().__init__(None)
        self.cost = cost

    def update(self) -> Status:
        bb = self.get_blackboard()
        bb["coins"] -= self.cost
        return Status.SUCCESS

class SaveMoneyAction(Behavior):
    def __init__(self, thresh):
        super().__init__(None)
        self.thresh = thresh

    def update(self) -> Status:
        bb = self.get_blackboard()
        if bb["coins"] > self.thresh: return Status.SUCCESS
        bb["coins"] += 1
        return Status.RUNNING

def build_tree() -> Behavior:
    # blackboard
    blackboard = {
        "coins": 0
    }

    builder = BehaviorTreeBuilder()
    builder.activeSelector("CoinDude")
    if 1:
        builder.parallel("SpendMoney", Parallel.REQUIRE_ALL)
        if 1:
            builder.action(VacationAction(2))
            builder.action(BuyCarAction(4))
        builder.endComposite()
        print(builder._stack)
        builder.action(SaveMoneyAction(8))

    tree = builder.build()
    tree.set_blackboard(blackboard)
    return tree

if __name__ == "__main__":
    # execute the tree
    tree = build_tree()
    dump_tree(tree)
    print()
    tree.set_trace(True) # enable call chain tracing
    tick_count = 0
    while not tree.is_terminated():
        tree.begin_trace() # clear the call chain list before we tick
        result = tree.tick()
        tick_count += 1
        # condense the call chain in to a list of node names (n -> n.name)
        chain = list(map(lambda n: f"{n[0]._name}:{crunch_status(n[1])}", tree._call_chain))
        executing = list(map(lambda n: f"{n[0]._name}:{crunch_status(n[1])}", parse_executing(tree._call_chain)))
        # log the executing leaf node and status
        print(f"tick[{tick_count}] {chain[-1]}: {result}")
        print(f"    CallChain {chain}")
        print(f"    Executing {executing}")
        print()

    print(tree.get_blackboard())
