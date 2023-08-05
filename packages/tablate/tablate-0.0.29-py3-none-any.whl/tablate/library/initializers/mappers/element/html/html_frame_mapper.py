from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.type.defaults import multiline_default, max_lines_default, background_default, frame_divider_default, \
    html_px_multiplier_default, html_divider_weight_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_base import HtmlFrameBase, FrameBase
from tablate.type.type_store import HtmlFrameStore


def html_frame_mapper(html_frame_input: Optional[HtmlFrameBase] = None,
                      html_frame_defaults: Optional[HtmlFrameBase] = None,
                      base_frame_defaults: Optional[FrameBase] = None,
                      html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> HtmlFrameStore:

    html_frame_divider_weight = set_attr_resolver(
        instance=html_frame_input,
        attr="html_frame_divider_weight",
        default=set_attr_resolver(
            instance=html_frame_defaults,
            attr="html_frame_divider_weight",
            default=html_divider_weight_default))
    html_frame_divider_style = set_attr_resolver(
        instance=html_frame_input,
        attr="html_frame_divider_style",
        default=set_attr_resolver(
            instance=html_frame_defaults,
            attr="html_frame_divider_style",
            default=set_attr_resolver(
                instance=base_frame_defaults,
                attr="divider",
                default=frame_divider_default)))
    html_max_lines = set_attr_resolver(
        instance=html_frame_input,
        attr="html_max_lines",
        default=set_attr_resolver(
            instance=html_frame_defaults,
            attr="html_max_lines",
            default=set_attr_resolver(
                instance=base_frame_defaults,
                attr="max_linnes",
                default=max_lines_default)))
    html_multiline = set_attr_resolver(
        instance=html_frame_input,
        attr="html_multiline",
        default=set_attr_resolver(
            instance=html_frame_defaults,
            attr="html_multiline",
            default=set_attr_resolver(
                instance=base_frame_defaults,
                attr="multiline",
                default=max_lines_default)))
    html_background = set_attr_resolver(
        instance=html_frame_input,
        attr="html_background",
        default=set_attr_resolver(
            instance=html_frame_defaults,
            attr="html_background",
            default=set_attr_resolver(
                instance=base_frame_defaults,
                attr="background",
                default=background_default)))

    html_frame_return = HtmlFrameStore(html_frame_divider_weight=html_frame_divider_weight,
                                       html_frame_divider_style=html_frame_divider_style,
                                       html_max_lines=html_max_lines,
                                       html_multiline=html_multiline,
                                       html_background=html_background,
                                       html_px_multiplier=html_px_multiplier)

    return html_frame_return
