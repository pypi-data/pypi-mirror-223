from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.library.formatters.html.style.attributes.color import background_color_attr
from tablate.type.defaults import background_default, row_line_divider_default, html_divider_weight_default, \
    html_divider_color_default
from tablate.type.type_style import HtmlTableRowsStyles, TableRowsStyles


def html_rows_mapper(html_rows_input: HtmlTableRowsStyles = None,
                     html_rows_defaults: HtmlTableRowsStyles = None,
                     base_rows_defaults: TableRowsStyles = None) -> HtmlTableRowsStyles:
    html_row_line_divider_weight = set_attr_resolver(
        instance=html_rows_input,
        attr="html_row_line_divider_weight",
        default=set_attr_resolver(
            instance=html_rows_defaults,
            attr="html_row_line_divider_weight",
            default=html_divider_weight_default))
    html_row_line_divider_style = set_attr_resolver(
        instance=html_rows_input,
        attr="html_row_line_divider_style",
        default=set_attr_resolver(
            instance=html_rows_defaults,
            attr="html_row_line_divider_style",
            default=set_attr_resolver(
                instance=base_rows_defaults,
                attr="row_line_divider",
                default=row_line_divider_default)))
    html_row_line_divider_color = set_attr_resolver(
        instance=html_rows_input,
        attr="html_row_line_divider_color",
        default=set_attr_resolver(
            instance=html_rows_defaults,
            attr="html_row_line_divider_color",
            default=html_divider_color_default))
    html_odds_background = set_attr_resolver(
        instance=html_rows_input,
        attr="html_odds_background",
        default=set_attr_resolver(
            instance=html_rows_defaults,
            attr="html_odds_background",
            default=background_color_attr(set_attr_resolver(
                instance=base_rows_defaults,
                attr="odds_background",
                default=background_default))))
    html_evens_background = set_attr_resolver(
        instance=html_rows_input,
        attr="html_evens_background",
        default=set_attr_resolver(
            instance=html_rows_defaults,
            attr="html_evens_background",
            default=background_color_attr(set_attr_resolver(
                instance=base_rows_defaults,
                attr="evens_background",
                default=background_default))))

    rows_return = HtmlTableRowsStyles(html_row_line_divider_weight=html_row_line_divider_weight,
                                      html_row_line_divider_style=html_row_line_divider_style,
                                      html_row_line_divider_color=html_row_line_divider_color,
                                      html_odds_background=html_odds_background,
                                      html_evens_background=html_evens_background)

    return rows_return
