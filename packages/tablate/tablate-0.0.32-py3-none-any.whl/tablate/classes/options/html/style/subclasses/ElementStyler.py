from copy import copy
from typing import Callable, Union, List, Tuple, Optional

from tablate.classes.options.html.style.mixins.AddStyleMixin import AddStyleMixin
from tablate.classes.options.html.style.mixins.ClassNameMixin import ClassNameMixin
from tablate.classes.options.html.style.subclasses.TextStyler import TextStyler
from tablate.classes.options.html.style.utilities.selectors import column_selector, row_selector
from tablate.classes.options.html.style.utilities.style_types import ElementSelectorDict, SelectorDictUnion, \
    ElementSelectorDictKeys, StyleItem


class ElementStyler(ClassNameMixin, AddStyleMixin):

    def __init__(self,
                 selector: ElementSelectorDict,
                 create_style: Callable[[SelectorDictUnion, StyleItem], None]) -> None:
        self._selector_dict = selector
        self._create_style = create_style

    def column(self, column_index: int = None):
        selector = self.__create_selector_dict(column=True, column_index=column_index)
        return ElementStyler(selector=selector, create_style=self._create_style)

    def row(self, row_index: int = None):
        selector = self.__create_selector_dict(row=True, row_index=row_index)
        return ElementStyler(selector=selector, create_style=self._create_style)

    @property
    def text(self):
        selector = self.__create_selector_dict(text_cell=True)
        return TextStyler(selector=selector, create_style=self._create_style)

    def __create_selector_dict(self,
                               column: bool = False,
                               column_index: int = None,
                               row: bool = None,
                               row_index: int = None,
                               text_cell: bool = False) -> ElementSelectorDict:
        new_selector_dict: ElementSelectorDict = copy(self._selector_dict)
        if column:
            # base_type: ElementSelectorDictKeys = "tablate_column"
            new_selector_dict["element_type"]: ElementSelectorDictKeys = "tablate_column"
            new_selector_dict["tablate_column"] = column_selector(index=column_index)
        if row:
            # base_type: ElementSelectorDictKeys = "tablate_row"
            new_selector_dict["element_type"]: ElementSelectorDictKeys = "tablate_row"
            new_selector_dict["tablate_row"] = row_selector(index=row_index)
        if text_cell:
            # base_type: ElementSelectorDictKeys = "tablate_text"
            new_selector_dict["element_type"]: ElementSelectorDictKeys = "tablate_text"
        return new_selector_dict
