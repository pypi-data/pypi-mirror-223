from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import column_divider_default, background_default, column_padding_default, \
    html_px_multiplier_default, html_padding_default, html_divider_weight_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_base import HtmlColumnBase, ColumnBase
from tablate.type.type_store import HtmlColumnStore


def html_column_mapper(html_columns_input: Optional[HtmlColumnBase] = None,
                       html_column_defaults: Optional[HtmlColumnBase] = None,
                       base_column_defaults: Optional[ColumnBase] = None) -> HtmlColumnStore:
    if html_columns_input is None:
        html_columns_input = HtmlColumnBase()

    html_divider_weight = set_attr_resolver(
        instance=html_columns_input,
        attr="html_divider_weight",
        default=set_attr_resolver(
            instance=html_column_defaults,
            attr="html_divider_weight",
            default=html_divider_weight_default))
    html_divider_style = set_attr_resolver(
        instance=html_columns_input,
        attr="html_divider_style",
        default=set_attr_resolver(
            instance=html_column_defaults,
            attr="html_divider_style",
            default=set_attr_resolver(
                instance=base_column_defaults,
                attr="divider",
                default=column_divider_default)))
    html_padding = set_attr_resolver(
        instance=html_columns_input,
        attr="html_padding",
        default=set_attr_resolver(
            instance=html_column_defaults,
            attr="html_padding",
            default=(set_attr_resolver(
                instance=base_column_defaults,
                attr="padding",
                default=html_padding_default) * html_padding_default)))

    columns_return = HtmlColumnStore(html_divider_weight=html_divider_weight,
                                     html_divider_style=html_divider_style,
                                     html_padding=html_padding)

    return columns_return

# todo: figure out a better way of doing this. (at the moment the inner checks are being performed before the base checks
