from copy import copy, deepcopy
from functools import cached_property
from typing import Callable, Tuple

from IPython.core.display import HTML
from IPython.core.display_functions import display

from tablate.classes.bases.TablateBase import TablateBase
from tablate.library.renderers.console.render_console import render_console
from tablate.library.renderers.html.render_html import render_html

from tablate.type.primitives import OuterBorder, FrameDivider, OuterWidth, OuterPadding, Background, HtmlPxMultiplier, \
    BackgroundPadding
from tablate.type.type_input import HtmlOuterStylesInput, ColumnStylesInput, TextStylesInput, \
    HtmlFrameStylesInput, HtmlColumnStylesInput, HtmlTextStylesInput


class TablateApiBase(TablateBase):

    def __init__(self,
                 outer_border: OuterBorder = None,
                 outer_padding: OuterPadding = None,
                 outer_width: OuterWidth = None,

                 frame_divider: FrameDivider = None,
                 background: Background = None,
                 background_padding: BackgroundPadding = None,

                 html_px_multiplier: HtmlPxMultiplier = None,
                 html_styles: HtmlOuterStylesInput = None,

                 column_styles: ColumnStylesInput = None,
                 text_styles: TextStylesInput = None,

                 html_frame_styles: HtmlFrameStylesInput = None,

                 html_column_styles: HtmlColumnStylesInput = None,
                 html_text_styles: HtmlTextStylesInput = None) -> None:

        args = copy(locals())
        del args["self"]

        self._globals_dict = args
        self._css_injection = []
        self._frame_list = {}

    # def __is_ipython(self):
    #     return hasattr(__builtins__, "__IPYTHON__")

    # def list_frames(self):
    #     print_frame_list(self._frame_list)

    def apply(self, function: Callable[[dict, dict],Tuple[dict, dict]]):
        frame_list_copy = deepcopy(self._frame_list)
        global_options_copy = deepcopy((self._globals_dict))
        try:
            frame_dict, global_dict = function(frame_list_copy, global_options_copy)
            if frame_dict is not None:
                self._frame_list = frame_dict
            if global_options_copy is not None:
                self._globals_dict = global_dict
        except:
            self._frame_list = frame_list_copy
            self._globals_dict = global_options_copy

    def apply_style(self, selector: str, css: str, sub_selector: str = None):
        self._css_injection.append({"selector": selector, "css": css, "sub_selector": sub_selector})

    def to_string(self) -> str:
        return render_console(frame_list=self._frame_list, global_options=self._globals_dict)

    def print(self) -> None:
        print(self.to_string())

    def __repr__(self) -> str:
        return self.to_string()

    def to_html(self) -> str:
        return render_html(frame_list=self._frame_list, globals_dict=self._globals_dict, css_injection=self._css_injection)

    @cached_property
    def _repr_html_(self) -> str:
        return self.to_html()
