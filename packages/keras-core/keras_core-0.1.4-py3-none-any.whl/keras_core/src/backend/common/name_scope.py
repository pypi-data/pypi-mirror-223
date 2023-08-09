from keras_core.src.backend.common import global_state


class NameScope:
    def __init__(self, name):
        if not isinstance(name, str) or not name.isalnum():
            raise ValueError(
                "Argument `name` must be an alphanumeric string. "
                f"Received: name={name}"
            )
        self.name = name

    def __enter__(self):
        name_scope_stack = global_state.get_global_attribute(
            "name_scope_stack", default=[], set_to_default=True
        )
        name_scope_stack.append(self.name)
        return self

    def __exit__(self, *args, **kwargs):
        name_scope_stack = global_state.get_global_attribute("name_scope_stack")
        name_scope_stack.pop()


def current_path():
    name_scope_stack = global_state.get_global_attribute("name_scope_stack")
    if name_scope_stack is None:
        return ""
    return "/".join(name_scope_stack)

