import sys
sys.path.append('../src')

from behaviortree.behavior import Status

def parse_executing(call_chain):
    executing = []
    for node in call_chain:
        # check node type
        is_composite = hasattr(node, "_children")
        is_decorator = hasattr(node, "_child")
        if not is_composite and not is_decorator:
            executing.append(node)
    return executing

def crunch_status(status: Status):
    if status == Status.SUCCESS:
        return 'S'
    if status == Status.FAILURE:
        return 'F'
    if status == Status.RUNNING:
        return 'R'
    if status == Status.ABORTED:
        return 'A'
    if status == Status.INVALID:
        return 'I'
    return status