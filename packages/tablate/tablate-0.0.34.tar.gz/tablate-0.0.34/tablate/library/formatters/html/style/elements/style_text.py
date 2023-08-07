from tablate.classes.options.html.style.subclasses.TextStyler import TextStyler
from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import html_text_size_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_style import HtmlTextStyles


def style_text(text_store: HtmlTextStyles, text_styler: TextStyler, html_px_multiplier: HtmlPxMultiplier) -> None:
    text_align = text_store.html_text_align
    text_size = set_attr_resolver(instance=text_store, attr="html_text_size", default=html_text_size_default)
    text_style = text_store.html_text_style
    text_color = text_store.html_text_color

    text_styler.add_style_attribute("font-size", f"{text_size * html_px_multiplier}px")

    if text_align is not None:
        text_styler.add_style_attribute("text-align", text_align)
    if text_style is not None:
        if text_style == "bold" or text_style == "bold_underlined":
            text_styler.add_style_attribute("font-weight", "bold")
        if text_style == "underlined" or text_style == "bold_underlined":
            text_styler.add_style_attribute("text-decoration", "underline")
    if text_color is not None:
        text_styler.add_style_attribute("color", text_color)


