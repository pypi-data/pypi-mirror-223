from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import html_outer_width_default, html_px_multiplier_default, outer_border_default, \
    outer_padding_default, outer_width_default, html_divider_weight_default, html_padding_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_base import HtmlOuterBase, OuterBase
from tablate.type.type_store import HtmlOuterStore


def html_outer_mapper(html_outer_input: Optional[HtmlOuterBase] = None,
                      html_outer_defaults: Optional[HtmlOuterBase] = None,
                      base_outer_defaults: OuterBase = None,
                      html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> HtmlOuterStore:
    if html_outer_input is None:
        html_outer_input = HtmlOuterBase()

    # html_outer_padding_default = outer_defaults.outer_padding * html_px_multiplier_default

    html_outer_border_weight = set_attr_resolver(
        instance=html_outer_input,
        attr="html_outer_border_weight",
        default=set_attr_resolver(
            instance=html_outer_defaults,
            attr="html_outer_border_weight",
            default=html_divider_weight_default))
    html_outer_border_style = set_attr_resolver(
        instance=html_outer_input,
        attr="html_outer_border_style",
        default=set_attr_resolver(
            instance=html_outer_defaults,
            attr="html_outer_border_style",
            default=set_attr_resolver(
                instance=base_outer_defaults,
                attr="outer_border",
                default=outer_border_default)))
    html_outer_padding = set_attr_resolver(
        instance=html_outer_input,
        attr="html_outer_padding",
        default=set_attr_resolver(
            instance=html_outer_defaults,
            attr="html_outer_padding",
            default=set_attr_resolver(
                instance=base_outer_defaults,
                attr="outer_padding",
                default=outer_padding_default)*html_padding_default))
    html_outer_width = set_attr_resolver(
        instance=html_outer_input,
        attr="html_outer_width",
        default=set_attr_resolver(
            instance=html_outer_defaults,
            attr="html_outer_width",
            default=html_outer_width_default))

    html_outer_return = HtmlOuterStore(html_outer_border_weight=html_outer_border_weight,
                                       html_outer_border_style=html_outer_border_style,
                                       html_outer_padding=html_outer_padding,
                                       html_outer_width=html_outer_width,
                                       html_px_multiplier=html_px_multiplier)

    return html_outer_return
