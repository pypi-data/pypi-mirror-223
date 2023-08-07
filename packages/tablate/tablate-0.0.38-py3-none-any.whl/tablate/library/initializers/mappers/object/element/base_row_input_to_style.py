from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import RowsStylesInput
from tablate.type.type_style import TableRowsStyles


def base_row_input_to_style(row_styles_input: RowsStylesInput) -> TableRowsStyles:

    row_styles_input = row_styles_input if row_styles_input is not None else {}

    row_line_divider = set_key_resolver(instance=row_styles_input, key="row_line_divider", default=None)
    odds_background = set_key_resolver(instance=row_styles_input, key="odds_background", default=None)
    evens_background = set_key_resolver(instance=row_styles_input, key="evens_background", default=None)

    return TableRowsStyles(
        row_line_divider=row_line_divider,
        odds_background=odds_background,
        evens_background=evens_background
    )
