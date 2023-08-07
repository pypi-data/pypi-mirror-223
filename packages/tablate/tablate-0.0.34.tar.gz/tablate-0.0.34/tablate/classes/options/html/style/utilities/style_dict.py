from typing import Union, List, Optional, Tuple

from tablate.classes.options.html.style.utilities.base_values import styles_key
from tablate.classes.options.html.style.utilities.style_types import SelectorDictUnion, SelectorDictKeysUnion, StyleItem


def style_dict_key_builder(style_dict: dict, selector_dict: SelectorDictUnion, key: SelectorDictKeysUnion) -> Union[dict, list]:
    if key in selector_dict:
        if selector_dict[key] in style_dict:
            style_dict = style_dict[selector_dict[key]]
        else:
            style_dict[selector_dict[key]] = {}
            style_dict = style_dict[selector_dict[key]]
    return style_dict


def style_dict_css_append(style_dict: dict, css_item: StyleItem):
    if styles_key in style_dict:
        style_dict[styles_key].append(css_item)
    else:
        style_dict[styles_key] = [css_item]
    return style_dict
