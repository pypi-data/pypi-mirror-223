from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.library.formatters.html.style.attributes.color import background_color_attr
from tablate.type.defaults import max_lines_default, background_default, frame_divider_default, \
    html_px_multiplier_default, html_divider_weight_default, html_divider_color_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_style import HtmlFrameStyles, FrameStyles


def html_frame_mapper(html_frame_input: HtmlFrameStyles = None,
                      html_frame_defaults: HtmlFrameStyles = None,
                      base_frame_defaults: FrameStyles = None,
                      html_px_multiplier: HtmlPxMultiplier = html_px_multiplier_default) -> HtmlFrameStyles:
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
    html_frame_divider_color = set_attr_resolver(
        instance=html_frame_input,
        attr="html_frame_divider_color",
        default=set_attr_resolver(
            instance=html_frame_defaults,
            attr="html_frame_divider_color",
            default=html_divider_color_default))
    html_max_lines = set_attr_resolver(
        instance=html_frame_input,
        attr="html_max_lines",
        default=set_attr_resolver(
            instance=html_frame_defaults,
            attr="html_max_lines",
            default=set_attr_resolver(
                instance=base_frame_defaults,
                attr="max_lines",
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
            default=background_color_attr(set_attr_resolver(
                instance=base_frame_defaults,
                attr="background",
                default=background_default))))

    html_frame_return = HtmlFrameStyles(html_frame_divider_weight=html_frame_divider_weight,
                                        html_frame_divider_style=html_frame_divider_style,
                                        html_frame_divider_color=html_frame_divider_color,
                                        html_max_lines=html_max_lines,
                                        html_multiline=html_multiline,
                                        html_background=html_background,
                                        html_px_multiplier=html_px_multiplier)

    return html_frame_return
