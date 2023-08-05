from dataclasses import dataclass, field
from typing import List, Optional

from tablate.classes.options.html.style.CssStyler import CssStyler
from tablate.type.primitives import CssStyleBlock, PxInteger
from tablate.type.type_base import HtmlOuterBase, FrameBase, ColumnBase, TextBase, OuterBase, HtmlFrameBase, \
    HtmlColumnBase, HtmlTextBase
from tablate.type.type_store import HtmlOuterStore, OuterStore


@dataclass
class ConsoleGlobals:
    outer_styles: OuterStore = field(default_factory=OuterStore)
    frame_styles: FrameBase = field(default_factory=FrameBase)
    column_styles: ColumnBase = field(default_factory=ColumnBase)
    text_styles: TextBase = field(default_factory=TextBase)


@dataclass
class HtmlGlobals:
    html_outer_styles: HtmlOuterStore = field(default_factory=HtmlOuterStore)
    html_frame_styles: HtmlFrameBase = field(default_factory=HtmlFrameBase)
    html_column_styles: HtmlColumnBase = field(default_factory=HtmlColumnBase)
    html_text_styles: HtmlTextBase = field(default_factory=HtmlTextBase)
    css_injection: CssStyleBlock = ""
    styler: Optional[CssStyler] = field(default_factory=CssStyler)
    column_baselines: List[PxInteger] = field(default_factory=list[6])


@dataclass
class Globals:
    console: ConsoleGlobals = field(default_factory=ConsoleGlobals)
    html: HtmlGlobals = field(default_factory=HtmlGlobals)
