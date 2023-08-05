from typing import overload, TypeVar, Type

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import column_divider_default, column_padding_default, text_style_default, \
    text_align_default, text_color_default, background_default, html_padding_default, html_divider_weight_default, \
    html_px_multiplier_default
from tablate.type.primitives import ColumnDivider, ColumnPadding, TextStyle, TextAlign, TextColor, Background, \
    HtmlPxMultiplier, BackgroundPadding
from tablate.type.type_base import ColumnBase, TextBase, FrameBase
from tablate.type.type_input import BaseColumnInput, GridColumnInput, HtmlColumnInput, \
    TableColumnInput
from tablate.type.type_store import BaseColumnStore


@overload
def column_attr(column_dict: BaseColumnInput,
                frame_styles: FrameBase,
                column_styles: ColumnBase,
                text_styles: TextBase,
                background_padding: BackgroundPadding,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> BaseColumnInput:
    ...


@overload
def column_attr(column_dict: GridColumnInput,
                frame_styles: FrameBase,
                column_styles: ColumnBase,
                text_styles: TextBase,
                background_padding: BackgroundPadding,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> GridColumnInput:
    ...


@overload
def column_attr(column_dict: TableColumnInput,
                frame_styles: FrameBase,
                column_styles: ColumnBase,
                text_styles: TextBase,
                background_padding: BackgroundPadding,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> TableColumnInput:
    ...


T = TypeVar("T", BaseColumnInput, GridColumnInput, TableColumnInput)


def column_attr(column_dict: Type[T],
                frame_styles: FrameBase,
                column_styles: ColumnBase,
                text_styles: TextBase,
                background_padding: BackgroundPadding,
                html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> T:
    divider = set_attr_resolver(instance=column_styles, attr="divider", default=column_divider_default)
    padding = set_attr_resolver(instance=column_styles, attr="padding", default=column_padding_default)
    text_style = set_attr_resolver(instance=text_styles, attr="text_style", default=text_style_default)
    text_align = set_attr_resolver(instance=text_styles, attr="text_align", default=text_align_default)
    text_color = set_attr_resolver(instance=text_styles, attr="text_color", default=text_color_default)
    background = set_attr_resolver(instance=frame_styles, attr="background", default=background_default)
    html_styles = set_attr_resolver(instance=frame_styles, attr="html_styles", default={})

    if "divider" in column_dict and column_dict["divider"] is not None:
        divider = column_dict["divider"]
        html_styles["divider_style"] = column_dict["divider"]
        html_styles["divider_weight"] = html_divider_weight_default * html_px_multiplier
    if "padding" in column_dict and column_dict["padding"] is not None:
        padding = column_dict["padding"]
        html_styles["padding"] = column_dict["padding"] * html_padding_default
    if "text_style" in column_dict and column_dict["text_style"] is not None:
        text_style = column_dict["text_style"]
        html_styles["text_style"] = column_dict["text_style"]
    if "text_align" in column_dict and column_dict["text_align"] is not None:
        text_align = column_dict["text_align"]
        html_styles["text_align"] = column_dict["text_align"]
    if "text_color" in column_dict and column_dict["text_color"] is not None:
        text_color = column_dict["text_color"]
        html_styles["text_color"] = column_dict["text_color"]
    if "background" in column_dict and column_dict["background"] is not None:
        background = column_dict["background"]
        html_styles["background"] = column_dict["background"]

    if "html_styles" in column_dict or ("html_styles" in column_dict and column_dict["html_styles"] is None):
        html_styles = None

    column_dict: BaseColumnStore = {
        "width": column_dict["width"],
        "string": column_dict["string"],
        "divider": divider,
        "padding": padding,
        "text_style": text_style,
        "text_align": text_align,
        "text_color": text_color,
        "background": background,
        "html_styles": html_styles if html_styles is not None else column_dict["html_styles"],
        "background_padding": background_padding,
        **column_dict
    }
    return_dict = BaseColumnStore(**column_dict)

    return return_dict


# todo: can use TypeVar + Type[T] (hopefully) to do away with the overloads... or not...

# todo: fix this!
