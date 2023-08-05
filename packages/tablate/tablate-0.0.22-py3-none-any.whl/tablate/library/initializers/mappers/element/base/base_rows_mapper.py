from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import row_line_divider_default, background_default
from tablate.type.type_base import TableRowsBase
from tablate.type.type_store import TableRowsStore


def base_rows_mapper(rows_input: Optional[TableRowsBase] = None,
                     rows_defaults: Optional[TableRowsBase] = None) -> TableRowsStore:

    ####################################################################################################################

    rows_input = rows_input if rows_input is not None else TableRowsBase()
    rows_defaults = rows_defaults if rows_defaults is not None else TableRowsBase()

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

    rows_return = TableRowsStore(row_line_divider=row_line_divider,
                                 odds_background=odds_background,
                                 evens_background=evens_background)

    return rows_return
