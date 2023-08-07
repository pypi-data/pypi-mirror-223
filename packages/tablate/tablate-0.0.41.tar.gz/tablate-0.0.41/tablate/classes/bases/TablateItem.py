from tablate.classes.bases.TablateApiItem import TablateApiItem
from tablate.library.initializers.processors.process_frame import process_frame_args
from tablate.type.primitives import OuterBorder, OuterPadding, OuterWidth, FrameDivider, Background, BackgroundPadding, \
    HtmlPxMultiplier, HtmlDefaultColors
from tablate.type.type_input import HtmlOuterStylesInput, ColumnStylesInput, TextStylesInput, HtmlFrameStylesInput, \
    HtmlColumnStylesInput, HtmlTextStylesInput
from tablate.type.type_store import FrameDict


class TablateItem(TablateApiItem):

    def __init__(self,
                 frame_item: FrameDict,
                 outer_border: OuterBorder = None,
                 outer_padding: OuterPadding = None,
                 outer_width: OuterWidth = None,

                 frame_divider: FrameDivider = None,
                 background: Background = None,
                 background_padding: BackgroundPadding = None,

                 html_px_multiplier: HtmlPxMultiplier = None,
                 html_outer_styles: HtmlOuterStylesInput = None,

                 html_default_colors: HtmlDefaultColors = None,

                 column_styles: ColumnStylesInput = None,
                 text_styles: TextStylesInput = None,

                 html_frame_styles: HtmlFrameStylesInput = None,

                 html_column_styles: HtmlColumnStylesInput = None,
                 html_text_styles: HtmlTextStylesInput = None):
        super().__init__(outer_border=outer_border,
                         outer_padding=outer_padding,
                         outer_width=outer_width,
                         frame_divider=frame_divider,
                         html_default_colors=html_default_colors,
                         background=background,
                         background_padding=background_padding,
                         html_px_multiplier=html_px_multiplier,
                         html_outer_styles=html_outer_styles,
                         column_styles=column_styles,
                         text_styles=text_styles,
                         html_frame_styles=html_frame_styles,
                         html_column_styles=html_column_styles,
                         html_text_styles=html_text_styles)

        self._frame_list = {frame_item.name: FrameDict(name=frame_item.name,
                                                       type=frame_item.type,
                                                       args=frame_item.args,
                                                       store=process_frame_args(frame_args=frame_item.args,
                                                                                frame_type=frame_item.type,
                                                                                global_options=self._globals_store.store))}
