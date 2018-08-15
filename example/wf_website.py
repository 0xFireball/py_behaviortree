import common
from common import parse_executing, crunch_status

from enum import Enum
from random import randint
from behaviortree.behavior import Status, Behavior
from behaviortree.composite import Sequence, Selector, ActiveSelector, Parallel
from behaviortree.decorator import Repeat
from behaviortree.trace import dump_tree
from behaviortree.builder import BehaviorTreeBuilder

class PromptAction(Behavior):
    def __init__(self, text, field):
        super().__init__(None)
        self.text = text
        self.field = field

    def update(self) -> Status:
        bb = self.get_blackboard()
        inputs = bb["inputs"]
        if self.field not in inputs: return Status.RUNNING
        input_value = inputs[self.field]
        if input_value == None: return Status.FAILURE
        # copy to blackboard
        bb[self.field] = input_value
        return Status.SUCCESS

class CompanyNamePrompt(PromptAction):
    def __init__(self):
        super().__init__("What is your company name?", "company_name")

    def update(self) -> Status:
        return super().update()

class DomainNamePrompt(PromptAction):
    def __init__(self):
        super().__init__("What is your domain name?", "domain_name")

    def update(self) -> Status:
        return super().update()

class BuildWebsiteAction(Behavior):
    def __init__(self):
        super().__init__(None)
        self.work_done = 0
        self.work_required = 4

    def update(self) -> Status:
        self.work_done += 1
        if self.work_done >= self.work_required: return Status.SUCCESS
        return Status.RUNNING

def build_tree() -> Behavior:
    # blackboard
    blackboard = {
        "inputs": {}
    }

    builder = BehaviorTreeBuilder()
    builder.sequence("Workflow_Website")
    if 1:
        builder.parallel("InitialInformation", Parallel.REQUIRE_ALL)
        if 1:
            builder.action(CompanyNamePrompt())
            builder.action(DomainNamePrompt())
        builder.endComposite()
        builder.action(BuildWebsiteAction())

    tree = builder.build()
    tree.set_blackboard(blackboard)
    return tree

INPUT_BAG = [
    ("company_name", "Example Widgets"),
    ("domain_name", "example.com"),
    ("useless1", "junk1"),
    ("useless2", "junk2"),
    ("useless3", "junk3"),
]

if __name__ == "__main__":
    # execute the tree
    tree = build_tree()
    dump_tree(tree)
    print()
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

        # randomly fill inputs from the input bag
        if len(INPUT_BAG) > 0:
            (input_name, input_value) = INPUT_BAG.pop(randint(0, len(INPUT_BAG) - 1))
            print(f"filled input {(input_name, input_value)}")
            tree.get_blackboard()["inputs"][input_name] = input_value

    # print(tree.get_blackboard())
