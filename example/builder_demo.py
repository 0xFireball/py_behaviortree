import common
from basic_tree import SleepAction, ChopAction, HaulAction

from behaviortree.behavior import Status, Behavior
from behaviortree.composite import Sequence, Selector, ActiveSelector
from behaviortree.decorator import Repeat
from behaviortree.builder import BehaviorTreeBuilder
from behaviortree.trace import dump_tree

def build_tree() -> Behavior:
    builder = BehaviorTreeBuilder()
    builder.activeSelector("BasicTree") # level 0
    if 1:
        builder.action(SleepAction(8))
        builder.decorator(Repeat, 'Work', -1)
        builder.sequence("Lumberjack") # level 1
        if 1:
            builder.action(ChopAction(4))
            builder.action(HaulAction())
        builder.decorate()
    builder.endComposite() # level 0

    return builder.build()

tree = build_tree()
dump_tree(tree)
