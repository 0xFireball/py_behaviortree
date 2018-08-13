from behaviortree.behavior import Behavior
from behaviortree.composite import Composite

def dump_tree(tree: Composite, n: int = 1):
    is_composite = hasattr(tree, "_children")
    is_decorator = hasattr(tree, "_child")
    symbol = ">"
    if is_composite: symbol = "-"
    if is_decorator: symbol = "@"
    item_name = tree._name
    item_type = tree.__class__.__name__
    if item_name == item_type: item_type = ""
    display = f"|{symbol} {item_name}[{item_type}]"
    print("  " * n + display)
    # dump children
    if is_composite:
        for child in tree._children:
            dump_tree(child, n + 1)
    if is_decorator:
        dump_tree(tree._child, n + 1)