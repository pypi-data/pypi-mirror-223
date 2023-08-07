from typing import TypedDict, Dict, NotRequired, Optional

from tablate.type.primitives import TextString, FrameDivider, ColumnWidth, TextStyle, TextAlign, Background, \
    ColumnPadding, TextColor, ColumnDivider, HtmlDividerWeight, HtmlColumnDividerStyle, HtmlColumnPadding, \
    HtmlTextStyle, HtmlTextAlign, HtmlTextColor, HtmlBackground, BackgroundPadding, HtmlTextSize, MaxLines, \
    Multiline, TruncValue, HtmlFrameDivider, HtmlOuterBorder, HtmlOuterPadding, HtmlOuterWidth, HtmlDividerColor


class HtmlOuterStylesInput(TypedDict):  # HtmlOuterBase
    html_outer_border_weight: NotRequired[HtmlDividerWeight]
    html_outer_border_style: NotRequired[HtmlOuterBorder]
    html_outer_border_color: NotRequired[HtmlDividerColor]
    html_outer_padding: NotRequired[HtmlOuterPadding]
    html_outer_width: NotRequired[HtmlOuterWidth]


########################################################################################################################

class FrameStylesInput(TypedDict):  # FrameBase
    frame_divider: NotRequired[FrameDivider]
    max_lines: NotRequired[MaxLines]
    multiline: NotRequired[Multiline]
    background: NotRequired[Background]
    trunc_value: NotRequired[TruncValue]


class HtmlFrameStylesInput(TypedDict):  # HtmlFrameBase
    html_frame_divider_style: NotRequired[HtmlFrameDivider]
    html_frame_divider_weight: NotRequired[HtmlDividerWeight]
    html_frame_divider_color: NotRequired[HtmlDividerColor]
    html_max_lines: NotRequired[MaxLines]
    html_multiline: NotRequired[Multiline]
    html_background: NotRequired[HtmlBackground]


########################################################################################################################

class ColumnStylesInput(TypedDict):  # ColumnBase
    column_divider: NotRequired[ColumnDivider]
    padding: NotRequired[ColumnPadding]
    background_padding: NotRequired[BackgroundPadding]


class TextStylesInput(TypedDict):  # TextBase
    text_style: NotRequired[TextStyle]
    text_align: NotRequired[TextAlign]
    text_color: NotRequired[TextColor]


class HtmlColumnStylesInput(TypedDict):  # HtmlColumnBase
    html_column_divider_style: NotRequired[HtmlColumnDividerStyle]
    html_column_divider_weight: NotRequired[HtmlDividerWeight]
    html_column_divider_color: NotRequired[HtmlDividerColor]
    html_padding: NotRequired[HtmlColumnPadding]


class HtmlTextStylesInput(TypedDict):  # HtmlTextBase
    html_text_style: NotRequired[HtmlTextStyle]
    html_text_align: NotRequired[HtmlTextAlign]
    html_text_color: NotRequired[HtmlTextColor]
    html_text_size: NotRequired[HtmlTextSize]
    
    
class RowsStylesInput(TypedDict):  # TableRowsBase
    row_line_divider: NotRequired[FrameDivider]
    odds_background: NotRequired[Background]
    evens_background: NotRequired[Background]
    
    
class HtmlRowsStylesInput(TypedDict):  # HtmlTableRowsBase
    html_row_line_divider_weight: NotRequired[HtmlDividerWeight]
    html_row_line_divider_style: NotRequired[HtmlFrameDivider]
    html_row_line_divider_color: NotRequired[HtmlDividerColor]
    html_odds_background: NotRequired[HtmlBackground]
    html_evens_background: NotRequired[HtmlBackground]


########################################################################################################################
########################################################################################################################
########################################################################################################################

class HtmlColumnInput(TypedDict):
    padding: NotRequired[HtmlColumnPadding]
    divider_style: NotRequired[HtmlColumnDividerStyle]
    divider_weight: NotRequired[HtmlDividerWeight]
    divider_color: NotRequired[HtmlDividerColor]
    text_style: NotRequired[HtmlTextStyle]
    text_align: NotRequired[HtmlTextAlign]
    text_color: NotRequired[HtmlTextColor]
    background: NotRequired[HtmlBackground]


class BaseColumnInput(TypedDict):
    string: TextString
    width: NotRequired[ColumnWidth]
    padding: NotRequired[ColumnPadding]
    divider: NotRequired[ColumnDivider]
    text_style: NotRequired[TextStyle]
    text_align: NotRequired[TextAlign]
    text_color: NotRequired[TextColor]
    background: NotRequired[Background]
    html_styles: NotRequired[Optional[HtmlColumnInput]]


class GridColumnInput(BaseColumnInput):
    pass


class TableColumnInput(BaseColumnInput):
    key: str


TableRowsInput = Dict[str, TextString]


########################################################################################################################
########################################################################################################################
########################################################################################################################


class BaseStylesInput(TypedDict):
    frame_styles: NotRequired[FrameStylesInput]
    column_styles: NotRequired[ColumnStylesInput]
    text_styles: NotRequired[TextStylesInput]
#
#
# GridStylesInput = BaseStylesInput
#
#
TableHeaderFrameStylesInput = BaseStylesInput


class TableBodyFrameStylesInput(BaseStylesInput):
    row_styles: NotRequired[RowsStylesInput]


########################################################################################################################


class HtmlStylesInput(TypedDict):
    html_frame_styles: NotRequired[HtmlFrameStylesInput]
    html_column_styles: NotRequired[HtmlColumnStylesInput]
    html_text_styles: NotRequired[HtmlTextStylesInput]


class HtmlTextFrameStylesInput(TypedDict):
    html_frame_styles: NotRequired[HtmlFrameStylesInput]
    html_text_styles: NotRequired[HtmlTextStylesInput]


HtmlGridStylesInput = HtmlStylesInput


class HtmlTableStylesInput(HtmlStylesInput):
    html_row_styles: NotRequired[HtmlRowsStylesInput]


HtmlTableHeaderStylesInput = HtmlStylesInput

HtmlTableBodyStylesInput = HtmlTableStylesInput

########################################################################################################################
########################################################################################################################
########################################################################################################################

