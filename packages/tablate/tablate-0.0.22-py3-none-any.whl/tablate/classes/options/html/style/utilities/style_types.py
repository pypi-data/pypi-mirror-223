from typing import TypedDict, NotRequired, Literal, Union, Optional

TablateInstanceKey = Literal["tablate_instance"]
ElementTypeKey = Literal["element_type"]

BaseSelectorDictKeys = Literal[TablateInstanceKey, ElementTypeKey]
TableSelectorDictKeys = Literal[BaseSelectorDictKeys, "tablate_container"]
ElementSelectorDictKeys = Literal[BaseSelectorDictKeys, "tablate_frame", "tablate_column", "tablate_row", "tablate_text"]

SelectorDictKeysUnion = Union[TableSelectorDictKeys, ElementSelectorDictKeys]

# NOTE: ( ▲ | ▼ ) Ensure the values of these two types match!!! (until Python allows a KeysOf[TypedDict] type...)

class StyleItem(TypedDict):
    style: str
    pseudo: Optional[str]


class BaseSelectorDict(TypedDict):
    tablate_instance: str
    element_type: str


class TableSelectorDict(BaseSelectorDict):
    tablate_table: str


class ElementSelectorDict(BaseSelectorDict):
    tablate_frame: NotRequired[str]
    tablate_column: NotRequired[str]
    tablate_row: NotRequired[str]
    tablate_text: NotRequired[str]


SelectorDictUnion = Union[TableSelectorDict, ElementSelectorDict]
