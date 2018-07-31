
# BehaviorTree - Basics

## Defining a custom Behavior

To create additional composites or leaf nodes such as actions, you need to subclass `Behavior`.
The necessary parts to override are:
    - `on_initialize`: should reset the state of the behavior
    - `update`: should return status of the behavior
