from typing import Callable, Union, List

from tablate.classes.options.html.style.mixins.AddStyleMixin import AddStyleMixin
from tablate.classes.options.html.style.mixins.ClassNameMixin import ClassNameMixin
from tablate.classes.options.html.style.utilities.style_types import TableSelectorDict, SelectorDictUnion, StyleItem


class TableStyler(ClassNameMixin, AddStyleMixin):

    def __init__(self,
                 selector: TableSelectorDict,
                 create_style: Callable[[SelectorDictUnion, StyleItem], None]) -> None:
        self._selector_dict = selector
        self._create_style = create_style
