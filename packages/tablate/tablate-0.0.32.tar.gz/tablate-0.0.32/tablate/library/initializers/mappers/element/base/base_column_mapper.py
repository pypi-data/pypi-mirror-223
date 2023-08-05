from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import column_divider_default, background_default, column_padding_default
from tablate.type.type_base import ColumnBase
from tablate.type.type_store import ColumnStore


def base_column_mapper(columns_input: Optional[ColumnBase] = None,
                       column_defaults: Optional[ColumnBase] = None) -> ColumnStore:

    ####################################################################################################################

    columns_input = columns_input if columns_input is not None else ColumnBase()
    column_defaults = column_defaults if column_defaults is not None else ColumnBase()

    ####################################################################################################################

    columns_return = ColumnStore(divider=set_attr_resolver(instance=columns_input,
                                                           attr="divider",
                                                           default=set_attr_resolver(instance=column_defaults,
                                                                                     attr="divider",
                                                                                     default=column_divider_default)),
                                 padding=set_attr_resolver(instance=columns_input,
                                                           attr="padding",
                                                           default=set_attr_resolver(instance=column_defaults,
                                                                                     attr="padding",
                                                                                     default=column_padding_default)))

    return columns_return
