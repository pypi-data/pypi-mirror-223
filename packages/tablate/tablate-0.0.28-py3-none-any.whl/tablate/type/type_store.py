from dataclasses import dataclass, field
from typing import Literal, Union, List, Dict

from tablate.type.defaults import background_padding_default, html_px_multiplier_default, frame_name_default
from tablate.type.primitives import TextString, TableRowKey, HtmlPxMultiplier, BackgroundPadding, FrameName, HideHeader
from tablate.type.type_base import ColumnBase, TextBase, HtmlTextBase, FrameBase, HtmlColumnBase, \
    HtmlTableRowsBase, TableRowsBase, HtmlFrameBase, HtmlOuterBase, OuterBase
from tablate.type.type_input import GridColumnInput, TableColumnInput, BaseColumnInput

########################################################################################################################
# FrameDicts ###########################################################################################################
########################################################################################################################


@dataclass
class OuterStore(OuterBase):
    background_padding: BackgroundPadding = background_padding_default


@dataclass
class HtmlOuterStore(HtmlOuterBase):
    html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default


@dataclass
class HtmlFrameStore(HtmlFrameBase):
    html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default


FrameStore = FrameBase
ColumnStore = ColumnBase
TextStore = TextBase

HtmlColumnStore = HtmlColumnBase
HtmlTextStore = HtmlTextBase

TableRowsStore = TableRowsBase
HtmlTableRowsStore = HtmlTableRowsBase


class BaseColumnStore(BaseColumnInput):
    background_padding: BackgroundPadding = background_padding_default


@dataclass
class BaseFrameStore:
    frame_styles: FrameStore = field(default_factory=FrameStore)
    column_styles: ColumnStore = field(default_factory=ColumnStore)
    text_styles: TextStore = field(default_factory=TextStore)
    html_frame_styles: HtmlFrameStore = field(default_factory=HtmlFrameStore)
    html_column_styles: HtmlColumnStore = field(default_factory=HtmlColumnStore)
    html_text_styles: HtmlTextStore = field(default_factory=HtmlTextStore)


# Grid FrameDict #######################################################################################################


GridColumnStore = BaseColumnStore


@dataclass()
class GridFrameStore(BaseFrameStore):
    type: Union[Literal["grid"], Literal["text"]] = "text"
    name: FrameName = frame_name_default
    column_list: List[GridColumnStore] = field(default_factory=list)


# Table FrameDict ######################################################################################################

@dataclass()
class TableHeaderFrameStore(BaseFrameStore):
    type: Literal["table_header"] = "table_header"
    name: FrameName = frame_name_default
    column_list: List[BaseColumnStore] = field(default_factory=list)


@dataclass()
class TableBodyFrameStore(BaseFrameStore):
    type: Literal["table_body"] = "table_body"
    name: FrameName = frame_name_default
    hide_header: HideHeader = False
    column_list: List[TableColumnInput] = field(default_factory=list)
    row_list: List[Dict[TableRowKey, TextString]] = field(default_factory=list)
    row_styles: TableRowsStore = field(default_factory=TableRowsStore)
    html_row_styles: HtmlTableRowsStore = field(default_factory=HtmlTableRowsStore)


# FrameDict List #######################################################################################################

FrameStoreUnion = Union[GridFrameStore, TableHeaderFrameStore, TableBodyFrameStore]
FrameStoreList = List[FrameStoreUnion]
