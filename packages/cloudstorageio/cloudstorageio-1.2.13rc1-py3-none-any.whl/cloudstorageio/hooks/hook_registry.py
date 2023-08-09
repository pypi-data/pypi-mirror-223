from typing import Callable


class HookRegistry:
    def __init__(self):
        self.hooks = {}

    def register(self, hook_name: str, hook: Callable):
        self.hooks[hook_name] = hook

    def execute(self, hook_name, *args, **kwargs):
        return self.hooks[hook_name](*args, **kwargs)
