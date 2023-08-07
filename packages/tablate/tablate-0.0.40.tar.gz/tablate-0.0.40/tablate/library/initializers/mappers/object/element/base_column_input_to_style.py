from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import ColumnStylesInput
from tablate.type.type_style import ColumnStyles


def base_column_input_to_style(column_styles_input: ColumnStylesInput) -> ColumnStyles:

    column_styles_input = column_styles_input if column_styles_input is not None else {}

    column_divider = set_key_resolver(instance=column_styles_input, key="column_divider", default=None)
    padding = set_key_resolver(instance=column_styles_input, key="padding", default=None)
    background_padding = set_key_resolver(instance=column_styles_input, key="background_padding", default=None)

    return ColumnStyles(
        column_divider=column_divider,
        padding=padding,
        background_padding=background_padding
    )
