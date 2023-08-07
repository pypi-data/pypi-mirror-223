from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import row_line_divider_default, background_default
from tablate.type.type_style import TableRowsStyles


def base_rows_mapper(rows_input: TableRowsStyles = None,
                     rows_defaults: TableRowsStyles = None) -> TableRowsStyles:
    ####################################################################################################################

    rows_input = rows_input if rows_input is not None else TableRowsStyles()
    rows_defaults = rows_defaults if rows_defaults is not None else TableRowsStyles()

    ####################################################################################################################

    row_line_divider = set_attr_resolver(instance=rows_input,
                                         attr="row_line_divider",
                                         default=set_attr_resolver(instance=rows_defaults,
                                                                   attr="row_line_divider",
                                                                   default=row_line_divider_default))
    odds_background = set_attr_resolver(instance=rows_input,
                                        attr="odds_background",
                                        default=set_attr_resolver(instance=rows_defaults,
                                                                  attr="odds_background",
                                                                  default=background_default))
    evens_background = set_attr_resolver(instance=rows_input,
                                         attr="evens_background",
                                         default=set_attr_resolver(instance=rows_defaults,
                                                                   attr="odds_background",
                                                                   default=background_default))

    rows_return = TableRowsStyles(row_line_divider=row_line_divider,
                                  odds_background=odds_background,
                                  evens_background=evens_background)

    return rows_return
