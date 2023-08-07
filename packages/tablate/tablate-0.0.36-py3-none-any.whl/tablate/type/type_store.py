from dataclasses import dataclass, field
from typing import Literal, Union, List, Dict, Tuple, Optional

from tablate.type.defaults import frame_name_default
from tablate.type.primitives import TextString, TableRowKey, FrameName, HideHeader
from tablate.type.type_input import GridColumnInput, TableColumnInput
from tablate.type.type_style import ColumnStyles, TextStyles, HtmlTextStyles, FrameStyles, HtmlColumnStyles, \
    HtmlFrameStyles, HtmlTableRowsStyles, TableRowsStyles


########################################################################################################################
# FrameDicts ###########################################################################################################
########################################################################################################################

@dataclass
class BaseFrameStore:
    frame_styles: FrameStyles = field(default_factory=FrameStyles)
    column_styles: ColumnStyles = field(default_factory=ColumnStyles)
    text_styles: TextStyles = field(default_factory=TextStyles)


@dataclass
class BaseTableFrameStore(BaseFrameStore):
    row_styles: TableRowsStyles = field(default_factory=TableRowsStyles)


@dataclass
class HtmlFrameStore:
    html_frame_styles: HtmlFrameStyles = field(default_factory=HtmlFrameStyles)
    html_column_styles: HtmlColumnStyles = field(default_factory=HtmlColumnStyles)
    html_text_styles: HtmlTextStyles = field(default_factory=HtmlTextStyles)


@dataclass
class HtmlTableFrameStore(HtmlFrameStore):
    html_row_styles: HtmlTableRowsStyles = field(default_factory=HtmlTableRowsStyles)


@dataclass
class FrameStore(BaseFrameStore, HtmlFrameStore):
    pass


@dataclass
class TableFrameStore(BaseTableFrameStore, HtmlTableFrameStore):
    pass

# Grid FrameDict #######################################################################################################




@dataclass()
class GridFrameStore(FrameStore):
    type: Union[Literal["grid"], Literal["text"]] = "text"
    name: FrameName = frame_name_default
    column_list: List[GridColumnInput] = field(default_factory=list)


# Table FrameDict ######################################################################################################

@dataclass()
class TableHeaderFrameStore(FrameStore):
    type: Literal["table_header"] = "table_header"
    name: FrameName = frame_name_default
    column_list: List[TableColumnInput] = field(default_factory=list)


@dataclass()
class TableBodyFrameStore(FrameStore):
    type: Literal["table_body"] = "table_body"
    name: FrameName = frame_name_default
    hide_header: HideHeader = False
    column_list: List[TableColumnInput] = field(default_factory=list)
    row_list: List[Dict[TableRowKey, TextString]] = field(default_factory=list)
    row_styles: TableRowsStyles = field(default_factory=TableRowsStyles)
    html_row_styles: HtmlTableRowsStyles = field(default_factory=HtmlTableRowsStyles)


# FrameDict List #######################################################################################################

FrameStoreUnion = Union[GridFrameStore, TableHeaderFrameStore, TableBodyFrameStore]
FrameStoreList = List[FrameStoreUnion]

@dataclass()
class FrameDict:
    name: FrameName
    type: Literal["text", "grid", "table"]
    args: dict
    store: Optional[Union[GridFrameStore, Tuple[Union[TableHeaderFrameStore, None], TableBodyFrameStore]]]


FrameDictList = Dict[str, FrameDict]
