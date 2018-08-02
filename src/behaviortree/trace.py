from behaviortree.behavior import Behavior
from behaviortree.composite import Composite

def dump_tree(tree: Composite, n: int = 1):
    print(" - " * n + tree._name + f"[{tree.__class__.__name__}]")
    # dump children
    if hasattr(tree, "_children"):
        for child in tree._children:
            dump_tree(child, n + 1)
    if hasattr(tree, "_child"):
        dump_tree(tree._child, n + 1)