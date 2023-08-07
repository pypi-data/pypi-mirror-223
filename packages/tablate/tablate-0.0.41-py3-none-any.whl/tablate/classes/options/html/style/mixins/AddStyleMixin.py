from typing import Callable, List, Union, Optional, Tuple

from tablate.classes.options.html.style.utilities.style_types import SelectorDictUnion, StyleItem


class AddStyleMixin:

    # todo: possibly in the future create specific methods for each style type... (ie: text-align / padding / etc)

    _selector_dict: SelectorDictUnion
    _create_style: Callable[[SelectorDictUnion, StyleItem], None]

    def add_style_attribute(self, attribute: str, value: Union[str, int], sub_selector: str = None) -> None:
        self._create_style(self._selector_dict, StyleItem(style=f"{attribute}:{value}", pseudo=sub_selector))


