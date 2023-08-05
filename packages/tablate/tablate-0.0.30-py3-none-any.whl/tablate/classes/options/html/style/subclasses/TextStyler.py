from typing import Callable, Union, List, Tuple, Optional

from tablate.classes.options.html.style.mixins.AddStyleMixin import AddStyleMixin
from tablate.classes.options.html.style.mixins.ClassNameMixin import ClassNameMixin
from tablate.classes.options.html.style.utilities.style_types import SelectorDictUnion, StyleItem
from tablate.type.primitives import TextAlign


class TextStyler(ClassNameMixin, AddStyleMixin):

    def __init__(self, selector: SelectorDictUnion,
                 create_style: Callable[[SelectorDictUnion, StyleItem], None]) -> None:
        self._selector_dict: SelectorDictUnion = selector
        self._create_style = create_style

    def alignment(self, align=TextAlign):
        pass
