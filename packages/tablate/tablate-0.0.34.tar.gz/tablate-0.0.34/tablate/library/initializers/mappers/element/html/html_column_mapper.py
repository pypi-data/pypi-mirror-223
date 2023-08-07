from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import column_divider_default, html_padding_default, html_divider_weight_default, \
    html_divider_color_default
from tablate.type.type_style import HtmlColumnStyles, ColumnStyles


def html_column_mapper(html_columns_input: HtmlColumnStyles = None,
                       html_column_defaults: HtmlColumnStyles = None,
                       base_column_defaults: ColumnStyles = None) -> HtmlColumnStyles:
    if html_columns_input is None:
        html_columns_input = HtmlColumnStyles()

    html_divider_weight = set_attr_resolver(
        instance=html_columns_input,
        attr="html_column_divider_weight",
        default=set_attr_resolver(
            instance=html_column_defaults,
            attr="html_column_divider_weight",
            default=html_divider_weight_default))
    html_divider_style = set_attr_resolver(
        instance=html_columns_input,
        attr="html_column_divider_style",
        default=set_attr_resolver(
            instance=html_column_defaults,
            attr="html_column_divider_style",
            default=set_attr_resolver(
                instance=base_column_defaults,
                attr="divider",
                default=column_divider_default)))
    html_divider_color = set_attr_resolver(
        instance=html_columns_input,
        attr="html_column_divider_color",
        default=set_attr_resolver(
            instance=html_column_defaults,
            attr="html_column_divider_color",
            default=html_divider_color_default))
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

    columns_return = HtmlColumnStyles(html_column_divider_weight=html_divider_weight,
                                      html_column_divider_style=html_divider_style,
                                      html_column_divider_color=html_divider_color,
                                      html_padding=html_padding)

    return columns_return

# todo: figure out a better way of doing this. (at the moment the inner checks are being performed before the base checks
