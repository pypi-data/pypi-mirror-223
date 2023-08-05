from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import text_style_default, text_align_default, text_color_default
from tablate.type.type_base import TextBase
from tablate.type.type_store import TextStore


def base_text_mapper(text_input: Optional[TextBase] = None,
                     text_defaults: Optional[TextBase] = None) -> TextStore:

    ####################################################################################################################

    text_input = text_input if text_input is not None else TextBase()
    text_defaults = text_defaults if text_defaults is not None else TextBase()

    ####################################################################################################################

    text_return = TextStore(text_style=set_attr_resolver(instance=text_input,
                                                         attr="text_style",
                                                         default=set_attr_resolver(instance=text_defaults,
                                                                                   attr="text_style",
                                                                                   default=text_style_default)),
                            text_align=set_attr_resolver(instance=text_input,
                                                         attr="text_align",
                                                         default=set_attr_resolver(instance=text_defaults,
                                                                                   attr="text_align",
                                                                                   default=text_align_default)),
                            text_color=set_attr_resolver(instance=text_input,
                                                         attr="text_color",
                                                         default=set_attr_resolver(instance=text_defaults,
                                                                                   attr="text_color",
                                                                                   default=text_color_default)))

    return text_return
