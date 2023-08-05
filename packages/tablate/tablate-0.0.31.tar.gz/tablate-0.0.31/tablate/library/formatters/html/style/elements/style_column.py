from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.library.checkers.is_last_element import is_last_element
from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.library.formatters.html.style.attributes.color import background_color_attr
from tablate.library.formatters.html.style.attributes.divider import divider_attr
from tablate.library.formatters.html.style.attributes.padding import padding_attr
from tablate.library.formatters.html.style.elements.style_text import style_text
from tablate.type.defaults import html_padding_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_base import HtmlColumnBase, HtmlTextBase
from tablate.type.type_input import BaseColumnStyles
from tablate.type.type_store import BaseFrameStore, BaseColumnStore, FrameStoreUnion


def style_column(column_store: HtmlColumnBase,
                 column_styler: ElementStyler,
                 html_px_multiplier: HtmlPxMultiplier) -> None:
    column_padding = column_store.html_padding
    column_padding_css = ""
    column_divider_weight = column_store.html_divider_weight
    column_divider_style = column_store.html_divider_style

    padding_string = padding_attr(column_padding=column_padding,
                                  html_px_multiplier=html_px_multiplier)

    column_styler.add_style_attribute("padding", padding_string)
    if column_divider_style is not None or column_divider_weight is not None:
        column_styler.add_style_attribute(attribute="border-right",
                                          value=divider_attr(divider_style=column_divider_style,
                                                             divider_weight=column_divider_weight),
                                          sub_selector=":not(:last-child)")


def style_column_dict(column_dict: BaseColumnStyles, column_styler: ElementStyler, html_px_multiplier: HtmlPxMultiplier) -> None:
    if "html_styles" in column_dict and column_dict["html_styles"] is not None:
        column_padding = set_key_resolver(instance=column_dict["html_styles"], key="padding", default=html_padding_default)
        divider_style = set_key_resolver(instance=column_dict["html_styles"], key="divider_style", default=None)
        divider_weight = set_key_resolver(instance=column_dict["html_styles"], key="divider_weight", default=None)
        column_background = set_key_resolver(instance=column_dict["html_styles"], key="background", default=None)

        style_column(column_store=HtmlColumnBase(html_padding=column_padding,
                                                 html_divider_style=divider_style,
                                                 html_divider_weight=divider_weight),
                     column_styler=column_styler,
                     html_px_multiplier=html_px_multiplier)

        if column_background is not None:
            column_styler.add_style_attribute("background-color", background_color_attr(column_background))

        text_align = set_key_resolver(instance=column_dict["html_styles"], key="text_align", default=None)
        text_size = set_key_resolver(instance=column_dict["html_styles"], key="text_size", default=None)
        text_style = set_key_resolver(instance=column_dict["html_styles"], key="text_style", default=None)
        text_color = set_key_resolver(instance=column_dict["html_styles"], key="text_color", default=None)

        text_styler = column_styler.text
        style_text(text_store=HtmlTextBase(html_text_align=text_align,
                                           html_text_size=text_size,
                                           html_text_style=text_style,
                                           html_text_color=text_color),
                   text_styler=text_styler,
                   html_px_multiplier=html_px_multiplier)
