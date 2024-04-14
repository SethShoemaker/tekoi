import inspect

def get_constructor_params(dependent_class: type) -> dict[str, type]:
    signature = inspect.signature(dependent_class.__init__)
    params = {name: parameter.annotation for name, parameter in signature.parameters.items() if parameter.name != "self"}
    return params
