from dataclasses import dataclass, field
from typing import Optional

from tablate.type.defaults import frame_divider_default, max_lines_default, multiline_default, background_default, \
    trunc_value_default, column_divider_default, column_padding_default, text_style_default, text_align_default, \
    text_color_default, row_line_divider_default, html_divider_weight_default, outer_border_default, \
    outer_padding_default, outer_width_default, html_outer_width_default, html_text_size_default, \
    html_background_default, html_max_lines_default, html_multiline_default, html_frame_divider_default, \
    html_outer_border_default, html_outer_padding_default, html_text_style_default, html_text_color_default, \
    html_text_align_default, html_row_line_divider_style_default, background_padding_default, \
    html_px_multiplier_default, html_default_colors_default, html_divider_color_default
from tablate.type.primitives import FrameDivider, OuterBorder, TextStyle, TextAlign, ColumnWidth, \
    ColumnPadding, MaxLines, Multiline, OuterWidth, OuterPadding, HtmlTextStyle, HtmlTextColor, HtmlTextSize, \
    HtmlColumnDividerStyle, HtmlColumnPadding, HtmlBackground, HtmlFrameDivider, \
    HtmlPxMultiplier, HtmlOuterBorder, HtmlOuterPadding, HtmlOuterWidth, HtmlTextAlign, Background, TextColor, \
    TruncValue, TextString, TableRowKey, ColumnDivider, HtmlDividerWeight, BackgroundPadding, HtmlDefaultColors, \
    HtmlDividerColor


@dataclass
class OuterStyles:
    outer_border: Optional[OuterBorder] = outer_border_default
    outer_padding: Optional[OuterPadding] = outer_padding_default
    outer_width: Optional[OuterWidth] = outer_width_default
    background_padding: BackgroundPadding = background_padding_default


###################################

@dataclass
class FrameStyles:
    frame_divider: Optional[FrameDivider] = frame_divider_default
    max_lines: Optional[MaxLines] = max_lines_default
    multiline: Optional[Multiline] = multiline_default
    background: Optional[Background] = background_default
    trunc_value: Optional[TruncValue] = trunc_value_default


@dataclass
class ColumnStyles:
    column_divider: Optional[ColumnDivider] = column_divider_default
    padding: Optional[ColumnPadding] = column_padding_default
    background_padding: Optional[BackgroundPadding] = background_default


@dataclass
class TextStyles:
    text_style: Optional[TextStyle] = text_style_default
    text_align: Optional[TextAlign] = text_align_default
    text_color: Optional[TextColor] = text_color_default


###################################
###################################
###################################

@dataclass
class TableRowsStyles:
    row_line_divider: Optional[FrameDivider] = row_line_divider_default
    odds_background: Optional[Background] = background_default
    evens_background: Optional[Background] = background_default


########################################################################################################################
########################################################################################################################
########################################################################################################################

@dataclass
class HtmlOuterStyles:
    html_outer_border_weight: Optional[HtmlDividerWeight] = html_divider_weight_default
    html_outer_border_style: Optional[HtmlOuterBorder] = html_outer_border_default
    html_outer_border_color: Optional[HtmlDividerColor] = html_divider_color_default
    html_outer_padding: Optional[HtmlOuterPadding] = field(default_factory=lambda: [html_outer_padding_default])
    html_outer_width: Optional[HtmlOuterWidth] = html_outer_width_default
    html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default
    html_default_colors: HtmlDefaultColors = html_default_colors_default

@dataclass
class HtmlFrameStyles:
    html_frame_divider_style: Optional[HtmlFrameDivider] = html_frame_divider_default
    html_frame_divider_weight: Optional[HtmlDividerWeight] = html_divider_weight_default
    html_frame_divider_color: Optional[HtmlDividerColor] = html_divider_color_default
    html_max_lines: Optional[MaxLines] = html_max_lines_default
    html_multiline: Optional[Multiline] = html_multiline_default
    html_background: Optional[HtmlBackground] = html_background_default
    html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default


@dataclass
class HtmlColumnStyles:
    html_column_divider_style: Optional[HtmlColumnDividerStyle] = column_divider_default
    html_column_divider_weight: Optional[HtmlDividerWeight] = html_divider_weight_default
    html_column_divider_color: Optional[HtmlDividerColor] = html_divider_color_default
    html_padding: Optional[HtmlColumnPadding] = column_padding_default


@dataclass
class HtmlTextStyles:
    html_text_style: Optional[HtmlTextStyle] = html_text_style_default
    html_text_align: Optional[HtmlTextAlign] = html_text_align_default
    html_text_color: Optional[HtmlTextColor] = html_text_color_default
    html_text_size: Optional[HtmlTextSize] = html_text_size_default


###################################
###################################
###################################


@dataclass
class HtmlTableRowsStyles:
    html_row_line_divider_weight: Optional[HtmlDividerWeight] = html_divider_weight_default
    html_row_line_divider_style: Optional[HtmlFrameDivider] = html_row_line_divider_style_default
    html_row_line_divider_color: Optional[HtmlDividerColor] = html_divider_color_default
    html_odds_background: Optional[HtmlBackground] = html_background_default
    html_evens_background: Optional[HtmlBackground] = html_background_default



