from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import text_style_default, text_align_default, text_color_default, html_text_size_default, \
    html_px_multiplier_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_base import HtmlTextBase, TextBase
from tablate.type.type_store import HtmlTextStore


def html_text_mapper(html_text_input: Optional[HtmlTextBase] = None,
                     html_text_defaults: Optional[HtmlTextBase] = None,
                     base_text_defaults: Optional[TextBase] = None,
                     html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> HtmlTextStore:
    if html_text_input is None:
        html_text_input = HtmlTextBase()

    html_text_style = set_attr_resolver(
        instance=html_text_input,
        attr="html_text_style",
        default=set_attr_resolver(
            instance=html_text_defaults,
            attr="html_text_style",
            default=set_attr_resolver(
                instance=base_text_defaults,
                attr="text_style",
                default=text_style_default)))
    html_text_align = set_attr_resolver(
        instance=html_text_input,
        attr="html_text_align",
        default=set_attr_resolver(
            instance=html_text_defaults,
            attr="html_text_align",
            default=set_attr_resolver(
                instance=base_text_defaults,
                attr="text_align",
                default=text_align_default)))
    html_text_color = set_attr_resolver(
        instance=html_text_input,
        attr="html_text_color",
        default=set_attr_resolver(
            instance=html_text_defaults,
            attr="html_text_color",
            default=set_attr_resolver(
                instance=base_text_defaults,
                attr="text_color",
                default=text_color_default)))
    html_text_size = set_attr_resolver(
        instance=html_text_input,
        attr="html_text_size",
        default=set_attr_resolver(
            instance=html_text_defaults,
            attr="html_text_size",
            default=html_text_size_default))

    text_return = HtmlTextStore(html_text_style=html_text_style,
                                html_text_align=html_text_align,
                                html_text_color=html_text_color,
                                html_text_size=html_text_size)

    return text_return
