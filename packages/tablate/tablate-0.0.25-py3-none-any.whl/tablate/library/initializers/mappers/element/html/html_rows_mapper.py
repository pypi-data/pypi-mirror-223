from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import background_default, row_line_divider_default, html_divider_weight_default
from tablate.type.type_base import HtmlTableRowsBase, TableRowsBase
from tablate.type.type_store import HtmlTableRowsStore


def html_rows_mapper(html_rows_input: Optional[HtmlTableRowsBase] = None,
                     html_rows_defaults: Optional[HtmlTableRowsBase] = None,
                     base_rows_defaults: Optional[TableRowsBase] = None) -> HtmlTableRowsStore:
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
    html_odds_background = set_attr_resolver(
        instance=html_rows_input,
        attr="html_odds_background",
        default=set_attr_resolver(
            instance=html_rows_defaults,
            attr="html_odds_background",
            default=set_attr_resolver(
                instance=base_rows_defaults,
                attr="odds_background",
                default=background_default)))
    html_evens_background = set_attr_resolver(
        instance=html_rows_input,
        attr="html_evens_background",
        default=set_attr_resolver(
            instance=html_rows_defaults,
            attr="html_evens_background",
            default=set_attr_resolver(
                instance=base_rows_defaults,
                attr="evens_background",
                default=background_default)))

    rows_return = HtmlTableRowsStore(html_row_line_divider_weight=html_row_line_divider_weight,
                                     html_row_line_divider_style=html_row_line_divider_style,
                                     html_odds_background=html_odds_background,
                                     html_evens_background=html_evens_background)

    return rows_return
