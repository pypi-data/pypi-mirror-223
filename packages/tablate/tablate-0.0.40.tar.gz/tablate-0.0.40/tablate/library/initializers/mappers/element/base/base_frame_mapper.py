from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import background_default, max_lines_default, \
    multiline_default, trunc_value_default, frame_divider_default
from tablate.type.type_style import FrameStyles
from tablate.type.type_store import FrameStore


def base_frame_mapper(frame_input: FrameStyles = None,
                      frame_defaults: FrameStyles = None) -> FrameStyles:
    ####################################################################################################################

    frame_input = frame_input if frame_input is not None else FrameStyles()
    frame_defaults = frame_defaults if frame_defaults is not None else FrameStyles()

    ####################################################################################################################

    frame_return = FrameStyles(frame_divider=set_attr_resolver(instance=frame_input,
                                                               attr="frame_divider",
                                                               default=set_attr_resolver(instance=frame_defaults,
                                                                                         attr="frame_divider",
                                                                                         default=frame_divider_default)),
                               max_lines=set_attr_resolver(instance=frame_input,
                                                           attr="max_lines",
                                                           default=set_attr_resolver(instance=frame_defaults,
                                                                                     attr="max_lines",
                                                                                     default=max_lines_default)),
                               multiline=set_attr_resolver(instance=frame_input,
                                                           attr="multiline",
                                                           default=set_attr_resolver(instance=frame_defaults,
                                                                                     attr="multiline",
                                                                                     default=multiline_default)),
                               background=set_attr_resolver(instance=frame_input,
                                                            attr="background",
                                                            default=set_attr_resolver(instance=frame_defaults,
                                                                                      attr="background",
                                                                                      default=background_default)),
                               trunc_value=set_attr_resolver(instance=frame_input,
                                                             attr="trunc_value",
                                                             default=set_attr_resolver(instance=frame_defaults,
                                                                                       attr="trunc_value",
                                                                                       default=trunc_value_default)))

    return frame_return
