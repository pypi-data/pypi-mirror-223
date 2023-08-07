from dataclasses import dataclass, field
from typing import List, Optional

from tablate.classes.options.html.style.CssStyler import CssStyler
from tablate.type.primitives import CssStyleBlock, PxInteger
from tablate.type.type_style import FrameStyles, ColumnStyles, TextStyles, HtmlFrameStyles, \
    HtmlColumnStyles, HtmlTextStyles, OuterStyles, HtmlOuterStyles


@dataclass
class ConsoleGlobals:
    outer_styles: OuterStyles = field(default_factory=OuterStyles)
    frame_styles: FrameStyles = field(default_factory=FrameStyles)
    column_styles: ColumnStyles = field(default_factory=ColumnStyles)
    text_styles: TextStyles = field(default_factory=TextStyles)


@dataclass
class HtmlGlobals:
    html_outer_styles: HtmlOuterStyles = field(default_factory=HtmlOuterStyles)
    html_frame_styles: HtmlFrameStyles = field(default_factory=HtmlFrameStyles)
    html_column_styles: HtmlColumnStyles = field(default_factory=HtmlColumnStyles)
    html_text_styles: HtmlTextStyles = field(default_factory=HtmlTextStyles)
    css_injection: CssStyleBlock = ""
    styler: Optional[CssStyler] = field(default_factory=CssStyler)
    column_baselines: List[PxInteger] = field(default_factory=list[6])


@dataclass
class Globals:
    console: ConsoleGlobals = field(default_factory=ConsoleGlobals)
    html: HtmlGlobals = field(default_factory=HtmlGlobals)

@dataclass
class GlobalsStore:
    args: dict
    store: Globals