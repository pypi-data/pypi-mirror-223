from typing import overload, TypeVar, Type

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.library.formatters.html.style.attributes.color import text_color_attr, background_color_attr
from tablate.type.defaults import column_divider_default, column_padding_default, text_style_default, \
    text_align_default, text_color_default, background_default, html_padding_default, html_divider_weight_default, \
    html_px_multiplier_default, html_divider_color_default, html_column_padding_default, html_text_style_default, \
    html_text_align_default, html_text_color_default, html_background_default, html_column_divider_style_default
from tablate.type.primitives import HtmlPxMultiplier, BackgroundPadding
from tablate.type.type_style import ColumnStyles, TextStyles, FrameStyles, HtmlFrameStyles, HtmlColumnStyles, \
    HtmlTextStyles
from tablate.type.type_input import BaseColumnInput, GridColumnInput, TableColumnInput


T = TypeVar("T", BaseColumnInput, GridColumnInput, TableColumnInput)


@overload
def column_attr(column_dict: BaseColumnInput,
                base_frame_styles: FrameStyles,
                base_column_styles: ColumnStyles,
                base_text_styles: TextStyles,
                html_frame_styles: HtmlFrameStyles,
                html_column_styles: HtmlColumnStyles,
                html_text_styles: HtmlTextStyles,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> BaseColumnInput:
    ...


@overload
def column_attr(column_dict: GridColumnInput,
                base_frame_styles: FrameStyles,
                base_column_styles: ColumnStyles,
                base_text_styles: TextStyles,
                html_frame_styles: HtmlFrameStyles,
                html_column_styles: HtmlColumnStyles,
                html_text_styles: HtmlTextStyles,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> BaseColumnInput:
    ...


@overload
def column_attr(column_dict: TableColumnInput,
                base_frame_styles: FrameStyles,
                base_column_styles: ColumnStyles,
                base_text_styles: TextStyles,
                html_frame_styles: HtmlFrameStyles,
                html_column_styles: HtmlColumnStyles,
                html_text_styles: HtmlTextStyles,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> BaseColumnInput:
    ...


def column_attr(column_dict: Type[T],
                base_frame_styles: FrameStyles,
                base_column_styles: ColumnStyles,
                base_text_styles: TextStyles,
                html_frame_styles: HtmlFrameStyles,
                html_column_styles: HtmlColumnStyles,
                html_text_styles: HtmlTextStyles,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> BaseColumnInput:
    base_divider = set_attr_resolver(instance=base_column_styles, attr="column_divider", default=column_divider_default)
    base_padding = set_attr_resolver(instance=base_column_styles, attr="padding", default=column_padding_default)
    base_text_style = set_attr_resolver(instance=base_text_styles, attr="text_style", default=text_style_default)
    base_text_align = set_attr_resolver(instance=base_text_styles, attr="text_align", default=text_align_default)
    base_text_color = set_attr_resolver(instance=base_text_styles, attr="text_color", default=text_color_default)
    base_background = set_attr_resolver(instance=base_frame_styles, attr="background", default=background_default)

    html_divider_style = set_attr_resolver(instance=html_column_styles, attr="html_column_divider_style", default=html_column_divider_style_default)
    html_divider_weight = set_attr_resolver(instance=html_column_styles, attr="html_column_divider_weight", default=html_divider_weight_default)
    html_divider_color = set_attr_resolver(instance=html_column_styles, attr="html_column_divider_color", default=html_divider_color_default)
    html_padding = set_attr_resolver(instance=html_column_styles, attr="html_padding", default=html_column_padding_default)
    html_text_style = set_attr_resolver(instance=html_text_styles, attr="html_text_style", default=html_text_style_default)
    html_text_align = set_attr_resolver(instance=html_text_styles, attr="html_text_align", default=html_text_align_default)
    html_text_color = set_attr_resolver(instance=html_text_styles, attr="html_text_color", default=html_text_color_default)
    html_background = set_attr_resolver(instance=html_frame_styles, attr="html_background", default=html_background_default)

    html_styles = {}

    if "divider" in column_dict and column_dict["divider"] is not None:
        base_divider = column_dict["divider"]
        html_styles["divider_style"] = column_dict["divider"]
        html_styles["divider_weight"] = html_divider_weight * html_px_multiplier
        html_styles["divider_color"] = html_divider_color
    if "padding" in column_dict and column_dict["padding"] is not None:
        base_padding = column_dict["padding"]
        html_styles["padding"] = column_dict["padding"] * html_padding_default
    if "text_style" in column_dict and column_dict["text_style"] is not None:
        base_text_style = column_dict["text_style"]
        html_styles["text_style"] = column_dict["text_style"]
    if "text_align" in column_dict and column_dict["text_align"] is not None:
        base_text_align = column_dict["text_align"]
        html_styles["text_align"] = column_dict["text_align"]
    if "text_color" in column_dict and column_dict["text_color"] is not None:
        base_text_color = column_dict["text_color"]
        html_styles["text_color"] = text_color_attr(column_dict["text_color"])
    if "background" in column_dict and column_dict["background"] is not None:
        base_background = column_dict["background"]
        html_styles["background"] = background_color_attr(column_dict["background"])

    if "html_styles" in column_dict or ("html_styles" in column_dict and column_dict["html_styles"] is None):
        html_styles = None

    column_dict: BaseColumnInput = {
        "width": column_dict["width"],
        "string": column_dict["string"],
        "divider": base_divider,
        "padding": base_padding,
        "text_style": base_text_style,
        "text_align": base_text_align,
        "text_color": base_text_color,
        "background": base_background,
        "html_styles": html_styles if html_styles is not None else column_dict["html_styles"],
        **column_dict
    }

    return column_dict


# todo: can use TypeVar + Type[T] (hopefully) to do away with the overloads... or not...

# todo: fix this!
