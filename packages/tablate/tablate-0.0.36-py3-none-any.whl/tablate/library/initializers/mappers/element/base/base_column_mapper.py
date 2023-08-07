from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import column_divider_default, column_padding_default
from tablate.type.type_style import ColumnStyles


def base_column_mapper(columns_input: ColumnStyles = None,
                       column_defaults: ColumnStyles = None) -> ColumnStyles:
    ####################################################################################################################

    columns_input = columns_input if columns_input is not None else ColumnStyles()
    column_defaults = column_defaults if column_defaults is not None else ColumnStyles()

    ####################################################################################################################

    columns_return = ColumnStyles(column_divider=set_attr_resolver(instance=columns_input,
                                                                   attr="divider",
                                                                   default=set_attr_resolver(instance=column_defaults,
                                                                                      attr="divider",
                                                                                      default=column_divider_default)),
                                  padding=set_attr_resolver(instance=columns_input,
                                                            attr="padding",
                                                            default=set_attr_resolver(instance=column_defaults,
                                                                                      attr="padding",
                                                                                      default=column_padding_default)),
                                  background_padding=set_attr_resolver(instance=columns_input,
                                                                       attr="background_padding",
                                                                       default=set_attr_resolver(
                                                                           instance=column_defaults,
                                                                           attr="background_padding",
                                                                           default=column_padding_default))
                                  )

    return columns_return
