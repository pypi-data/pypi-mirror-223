from dataclasses import dataclass, field
from typing import TypedDict, Dict, List, NotRequired, Optional, Literal

from tablate.type.primitives import TextString, FrameDivider, ColumnWidth, TextStyle, TextAlign, Background, \
    ColumnPadding, TextColor, ColumnDivider, HtmlDividerWeight, HtmlColumnDividerStyle, HtmlColumnPadding, \
    HtmlTextStyle, HtmlTextAlign, HtmlTextColor, HtmlBackground, FrameName
from tablate.type.type_base import ColumnBase, TextBase, HtmlTextBase, TableRowsBase, \
    HtmlColumnBase, HtmlTableRowsBase, HtmlOuterBase, HtmlFrameBase, FrameBase

HtmlOuterStylesInput = HtmlOuterBase

FrameStylesInput = FrameBase

HtmlFrameStylesInput = HtmlFrameBase


class HtmlColumnInput(TypedDict):
    padding: NotRequired[HtmlColumnPadding]
    divider_style: NotRequired[HtmlColumnDividerStyle]
    divider_weight: NotRequired[HtmlDividerWeight]
    text_style: NotRequired[HtmlTextStyle]
    text_align: NotRequired[HtmlTextAlign]
    text_color: NotRequired[HtmlTextColor]
    background: NotRequired[HtmlBackground]


class BaseColumnStyles(TypedDict):
    width: NotRequired[ColumnWidth]
    padding: NotRequired[ColumnPadding]
    divider: NotRequired[ColumnDivider]
    text_style: NotRequired[TextStyle]
    text_align: NotRequired[TextAlign]
    text_color: NotRequired[TextColor]
    background: NotRequired[Background]
    html_styles: NotRequired[Optional[HtmlColumnInput]]


class BaseColumnInput(BaseColumnStyles):
    string: TextString


########################################################################################################################

GridColumnInput = BaseColumnInput


class TableColumnInput(BaseColumnInput):
    key: str


TableRowsDataInputDict = Dict[str, TextString]


########################################################################################################################

ColumnStylesInput = ColumnBase
TextStylesInput = TextBase

HtmlColumnStylesInput = HtmlColumnBase
HtmlTextStylesInput = HtmlTextBase

########################################################################################################################
########################################################################################################################
########################################################################################################################


@dataclass
class BaseStylesInput:
    frame_styles: Optional[FrameBase] = None
    column_styles: Optional[ColumnBase] = None
    text_styles: Optional[TextBase] = None


TableHeaderFrameStylesInput = BaseStylesInput


@dataclass
class TableBodyFrameStylesInput(BaseStylesInput):
    row_styles: Optional[TableRowsBase] = None


########################################################################################################################
########################################################################################################################
########################################################################################################################

@dataclass
class HtmlStylesInput:
    html_frame_styles: Optional[HtmlFrameBase] = None
    html_column_styles: Optional[HtmlColumnBase] = None
    html_text_styles: Optional[HtmlTextBase] = None


########################################################################################################################

@dataclass
class HtmlTextFrameStylesInput:
    html_frame_styles: Optional[HtmlFrameBase] = None
    html_text_styles: Optional[HtmlTextBase] = None


HtmlGridFrameStylesInput = HtmlStylesInput


@dataclass
class HtmlTableFrameStylesInput(HtmlStylesInput):
    html_row_styles: Optional[HtmlTableRowsBase] = None


HtmlTableBodyFrameStylesInput = HtmlTableFrameStylesInput
HtmlTableHeaderFrameStylesInput = HtmlStylesInput

########################################################################################################################
########################################################################################################################
########################################################################################################################

class FrameDict(TypedDict):
    name: FrameName
    type: Literal["text", "grid", "table"]
    options: dict


FrameDictList = Dict[str, FrameDict]