
# Builder

`BehaviorTreeBuilder` provides an intuitive interface for constructing a behavior tree in forward form.

## Example

```py
def build_tree() -> Behavior:
    builder = BehaviorTreeBuilder()
    
    builder.activeSelector("BasicTree")
    if 1:
        builder.action(SleepAction(8))
        builder.decorator(Repeat, 'Work', -1)
        builder.sequence("Lumberjack")
        if 1:
            builder.action(ChopAction(4))
            builder.action(HaulAction())
        builder.decorate()
    builder.endComposite()

    return builder.build()
```

This builds a tree to look like this:
```
  |- BasicTree[ActiveSelector]
    |> SleepAction[]
    |@ Work[Repeat]
      |- Lumberjack[Sequence]
        |> ChopAction[]
        |> HaulAction[]
```

Use `dump_tree` from `behaviortree.trace` to automatically pretty-print trees like above.

## Guide

### The `if 1:` thing
This is a stupid solution to allow indenting to show tree structure, since Python cares about whitespace (why?)

### Composites

Begin a composite by calling one of the composite methods (`selector`, `sequence`, `parallel`, `parallelSelector`, `activeSelector`) and specifying a `"name"` or `None`.
Alternatively, use `composite` to add a custom composite.
Use `endComposite` to signal that the composite is complete; the current composite will be popped and attached to the next item on the stack.

### Actions (leaf nodes)

Add an action (leaf behavior) using `action`.

### Decorators

Queue a decorator by calling `decorator` with a decorator type (not an instance), followed by the name and additional parameters.
When `decorate` is called, the most recent composite is popped and the decorator is attached, then the wrapped composite is pushed back.
Decorators cannot currently be attached directly to leaf nodes. Instead, use a single-child composite and decorate that.

### Generating a Tree

Calling `build` returns a completed behavior tree.
