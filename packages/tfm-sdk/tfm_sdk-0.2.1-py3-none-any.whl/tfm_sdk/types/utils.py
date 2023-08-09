def underscore_to_camelcase(variable_name):
    components = variable_name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def get_or(kwargs, key, or_key, required=True):
    if key in kwargs:
        return kwargs[key]
    return kwargs[or_key] if required else kwargs.get(or_key)
