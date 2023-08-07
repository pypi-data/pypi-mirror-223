from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.library.formatters.html.style.attributes.divider import divider_attr
from tablate.library.formatters.html.style.attributes.padding import padding_attr
from tablate.library.formatters.html.style.elements.style_text import style_text
from tablate.type.defaults import html_padding_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_input import BaseColumnInput
from tablate.type.type_style import HtmlColumnStyles, HtmlTextStyles


def style_column(column_store: HtmlColumnStyles,
                 column_styler: ElementStyler,
                 html_px_multiplier: HtmlPxMultiplier) -> None:
    column_padding = column_store.html_padding
    column_padding_css = ""
    column_divider_weight = column_store.html_column_divider_weight
    column_divider_style = column_store.html_column_divider_style
    column_divider_color = column_store.html_column_divider_color

    padding_string = padding_attr(column_padding=column_padding,
                                  html_px_multiplier=html_px_multiplier)

    column_styler.add_style_attribute("padding", padding_string, sub_selector=" > div")
    if column_divider_style is not None or column_divider_weight is not None:
        column_styler.add_style_attribute(attribute="border-right",
                                          value=divider_attr(divider_style=column_divider_style,
                                                             divider_weight=column_divider_weight,
                                                             divider_color=column_divider_color),
                                          sub_selector=":not(:last-child) > div")
        column_styler.add_style_attribute(attribute="height",
                                          value="100%",
                                          sub_selector=" > div")
        column_styler.add_style_attribute(attribute="height",
                                          value="100%")


def style_column_dict(column_dict: BaseColumnInput, column_styler: ElementStyler, html_px_multiplier: HtmlPxMultiplier) -> None:
    if "html_styles" in column_dict and column_dict["html_styles"] is not None:
        column_padding = set_key_resolver(instance=column_dict["html_styles"], key="padding", default=html_padding_default)
        divider_style = set_key_resolver(instance=column_dict["html_styles"], key="divider_style", default=None)
        divider_weight = set_key_resolver(instance=column_dict["html_styles"], key="divider_weight", default=None)
        divider_color = set_key_resolver(instance=column_dict["html_styles"], key="divider_color", default=None)
        column_background = set_key_resolver(instance=column_dict["html_styles"], key="background", default=None)

        style_column(column_store=HtmlColumnStyles(html_padding=column_padding,
                                                   html_column_divider_style=divider_style,
                                                   html_column_divider_weight=divider_weight,
                                                   html_column_divider_color=divider_color),
                     column_styler=column_styler,
                     html_px_multiplier=html_px_multiplier)

        if column_background is not None:
            column_styler.add_style_attribute("background-color", column_background)

        text_align = set_key_resolver(instance=column_dict["html_styles"], key="text_align", default=None)
        text_size = set_key_resolver(instance=column_dict["html_styles"], key="text_size", default=None)
        text_style = set_key_resolver(instance=column_dict["html_styles"], key="text_style", default=None)
        text_color = set_key_resolver(instance=column_dict["html_styles"], key="text_color", default=None)

        text_styler = column_styler.text
        style_text(text_store=HtmlTextStyles(html_text_align=text_align,
                                             html_text_size=text_size,
                                             html_text_style=text_style,
                                             html_text_color=text_color),
                   text_styler=text_styler,
                   html_px_multiplier=html_px_multiplier)
