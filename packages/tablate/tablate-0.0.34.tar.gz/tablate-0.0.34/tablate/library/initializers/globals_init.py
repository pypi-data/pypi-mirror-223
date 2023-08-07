from tablate.library.initializers.mappers.element.base.base_column_mapper import base_column_mapper
from tablate.library.initializers.mappers.element.base.base_frame_mapper import base_frame_mapper
from tablate.library.initializers.mappers.element.base.base_text_mapper import base_text_mapper
from tablate.library.initializers.mappers.element.html.html_column_mapper import html_column_mapper
from tablate.library.initializers.mappers.element.html.html_frame_mapper import html_frame_mapper
from tablate.library.initializers.mappers.element.html.html_outer_mapper import html_outer_mapper
from tablate.library.initializers.mappers.element.html.html_text_mapper import html_text_mapper
from tablate.library.initializers.mappers.object.element.html_column_input_to_style import html_column_input_to_style
from tablate.library.initializers.mappers.object.element.html_frame_input_to_style import html_frame_input_to_style
from tablate.library.initializers.mappers.object.element.html_outer_input_style import html_outer_input_to_style
from tablate.library.initializers.mappers.object.element.html_text_input_to_style import html_text_input_to_style
from tablate.type.defaults import outer_border_default, outer_padding_default, outer_width_default, \
    background_padding_default, html_px_multiplier_default
from tablate.type.primitives import OuterBorder, OuterPadding, OuterWidth, FrameDivider, Background, BackgroundPadding, \
    HtmlPxMultiplier, HtmlDefaultColors
from tablate.type.type_style import FrameStyles, OuterStyles
from tablate.type.type_global import ConsoleGlobals, HtmlGlobals, Globals
from tablate.type.type_input import HtmlOuterStylesInput, ColumnStylesInput, TextStylesInput, HtmlFrameStylesInput, \
    HtmlColumnStylesInput, HtmlTextStylesInput


def globals_init(outer_border: OuterBorder = None,
                 outer_padding: OuterPadding = None,
                 outer_width: OuterWidth = None,

                 html_default_colors: HtmlDefaultColors = None,

                 frame_divider: FrameDivider = None,
                 background: Background = None,
                 background_padding: BackgroundPadding = None,

                 html_px_multiplier: HtmlPxMultiplier = None,
                 html_outer_styles: HtmlOuterStylesInput = None,

                 column_styles: ColumnStylesInput = None,
                 text_styles: TextStylesInput = None,

                 html_frame_styles: HtmlFrameStylesInput = None,

                 html_column_styles: HtmlColumnStylesInput = None,
                 html_text_styles: HtmlTextStylesInput = None) -> Globals:

    html_outer_styles = html_outer_input_to_style(html_outer_styles)
    html_frame_styles = html_frame_input_to_style(html_frame_styles)
    html_column_styles = html_column_input_to_style(html_column_styles)
    html_text_styles = html_text_input_to_style(html_text_styles)

    default_outer_styles = OuterStyles(outer_border=outer_border if outer_border else outer_border_default,
                                       outer_padding=outer_padding if outer_padding else outer_padding_default,
                                       outer_width=outer_width if outer_width else outer_width_default,
                                       background_padding=background_padding if background_padding else background_padding_default)

    default_frame_styles = base_frame_mapper(frame_input=FrameStyles(frame_divider=frame_divider,
                                                                     background=background))

    default_column_styles = base_column_mapper(columns_input=column_styles)

    default_text_styles = base_text_mapper(text_input=text_styles)

    console_globals = ConsoleGlobals(outer_styles=default_outer_styles,
                                     frame_styles=default_frame_styles,
                                     column_styles=default_column_styles,
                                     text_styles=default_text_styles)

    if html_px_multiplier is None:
        html_px_multiplier = html_px_multiplier_default

    default_html_outer = html_outer_mapper(html_outer_input=html_outer_styles,
                                           base_outer_defaults=default_outer_styles,
                                           html_px_multiplier=html_px_multiplier,
                                           html_default_colors=html_default_colors)
    default_html_frame = html_frame_mapper(html_frame_input=html_frame_styles,
                                           base_frame_defaults=default_frame_styles)
    default_html_column = html_column_mapper(html_columns_input=html_column_styles,
                                             base_column_defaults=default_column_styles)
    default_html_text = html_text_mapper(html_text_input=html_text_styles,
                                         base_text_defaults=default_text_styles,
                                         html_px_multiplier=html_px_multiplier)

    html_globals = HtmlGlobals(html_outer_styles=default_html_outer,
                               html_frame_styles=default_html_frame,
                               html_column_styles=default_html_column,
                               html_text_styles=default_html_text,
                               css_injection="",
                               column_baselines=[],
                               styler=None)

    return Globals(console=console_globals, html=html_globals)
