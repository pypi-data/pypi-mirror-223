from tablate.classes.options.html.style.utilities.base_values import base_class, tablate_instance_key, \
    element_type_key
from tablate.classes.options.html.style.utilities.style_types import ElementSelectorDictKeys


def element_append(string: str) -> str:
    return f"{string}_element"


def base_selector_dict(base_selector: str, key: str, value: str, element_type: ElementSelectorDictKeys):
    # element_type = element_append(element_type)
    return {tablate_instance_key: base_selector, key: value, element_type_key: element_type}


def instance_selector(uid: str):
    return f"{base_class}_{uid}"


def container_selector() -> str:
    return f"{base_class}_wrapper"


def table_selector() -> str:
    return f"{base_class}_table"


def frame_selector(index: int) -> str:
    return f"{base_class}_frame_{index}"


def column_selector(index: int) -> str:
    specifier = ""
    if index is not None:
        specifier = f"_{index}"
    return f"{base_class}_column{specifier}"


def row_selector(index: int) -> str:
    specifier = ""
    if index is not None:
        specifier = f"_{index}"
    return f"{base_class}_row{specifier}"


def text_selector() -> str:
    return f"{base_class}_text"
