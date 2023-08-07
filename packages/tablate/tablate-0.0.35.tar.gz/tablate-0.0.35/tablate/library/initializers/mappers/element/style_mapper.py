from typing import Optional

from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.library.initializers.mappers.element.base.base_column_mapper import base_column_mapper
from tablate.library.initializers.mappers.element.base.base_frame_mapper import base_frame_mapper
from tablate.library.initializers.mappers.element.base.base_text_mapper import base_text_mapper
from tablate.library.initializers.mappers.element.html.html_column_mapper import html_column_mapper
from tablate.library.initializers.mappers.element.html.html_frame_mapper import html_frame_mapper
from tablate.library.initializers.mappers.element.html.html_text_mapper import html_text_mapper
from tablate.type.defaults import html_px_multiplier_default
from tablate.type.primitives import HtmlPxMultiplier
from tablate.type.type_style import FrameStyles, TextStyles, ColumnStyles, HtmlFrameStyles, HtmlColumnStyles, HtmlTextStyles
from tablate.type.type_global import Globals
from tablate.type.type_store import BaseFrameStore, FrameStore, HtmlFrameStore


def style_mapper(base_input: Optional[BaseFrameStore],
                 html_input: Optional[HtmlFrameStore],
                 base_defaults: Optional[BaseFrameStore],
                 html_defaults: Optional[HtmlFrameStore],
                 html_px_multiplier: HtmlPxMultiplier,
                 global_options: Globals) -> FrameStore:
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    if html_px_multiplier is None:
        html_px_multiplier = html_px_multiplier_default

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    frame_styles_default = base_frame_mapper(frame_input=global_options.console.frame_styles,
                                             frame_defaults=FrameStyles())
    column_styles_default = base_column_mapper(columns_input=global_options.console.column_styles,
                                               column_defaults=ColumnStyles())
    text_styles_default = base_text_mapper(text_input=global_options.console.text_styles,
                                           text_defaults=TextStyles())

    frame_styles_default = set_attr_resolver(instance=base_defaults,
                                             attr="frame_styles",
                                             default=frame_styles_default)
    column_styles_default = set_attr_resolver(instance=base_defaults,
                                              attr="column_styles",
                                              default=column_styles_default)
    text_styles_default = set_attr_resolver(instance=base_defaults,
                                            attr="text_styles",
                                            default=text_styles_default)

    ####################################################################################################################

    frame_styles = set_attr_resolver(instance=base_input,
                                     attr="frame_styles",
                                     default=frame_styles_default)
    column_styles = set_attr_resolver(instance=base_input,
                                      attr="column_styles",
                                      default=column_styles_default)
    text_styles = set_attr_resolver(instance=base_input,
                                    attr="text_styles",
                                    default=text_styles_default)

    frame_styles = base_frame_mapper(frame_input=frame_styles,
                                     frame_defaults=frame_styles_default)
    column_styles = base_column_mapper(columns_input=column_styles,
                                       column_defaults=column_styles_default)
    text_styles = base_text_mapper(text_input=text_styles,
                                   text_defaults=text_styles_default)

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    html_frame_styles_default = html_frame_mapper(html_frame_input=global_options.html.html_frame_styles,
                                                  html_frame_defaults=HtmlFrameStyles(),
                                                  html_px_multiplier=html_px_multiplier)
    html_column_styles_default = html_column_mapper(html_columns_input=global_options.html.html_column_styles,
                                                    html_column_defaults=HtmlColumnStyles())
    html_text_styles_default = html_text_mapper(html_text_input=global_options.html.html_text_styles,
                                                html_text_defaults=HtmlTextStyles(),
                                                html_px_multiplier=html_px_multiplier)

    html_frame_styles_default = set_attr_resolver(instance=html_defaults,
                                                  attr="html_frame_styles",
                                                  default=html_frame_styles_default)
    html_column_styles_default = set_attr_resolver(instance=html_defaults,
                                                   attr="html_column_styles",
                                                   default=html_column_styles_default)
    html_text_styles_default = set_attr_resolver(instance=html_defaults,
                                                 attr="html_text_styles",
                                                 default=html_text_styles_default)

    ####################################################################################################################

    html_frame_styles = set_attr_resolver(instance=html_input,
                                          attr="html_frame_styles",
                                          default=None)
    html_column_styles = set_attr_resolver(instance=html_input,
                                           attr="html_column_styles",
                                           default=None)
    html_text_styles = set_attr_resolver(instance=html_input,
                                         attr="html_text_styles",
                                         default=None)

    ####################################################################################################################

    html_frame_styles = html_frame_mapper(html_frame_input=html_frame_styles,
                                          html_frame_defaults=html_frame_styles_default,
                                          base_frame_defaults=frame_styles,
                                          html_px_multiplier=html_px_multiplier)
    html_column_styles = html_column_mapper(html_columns_input=html_column_styles,
                                            html_column_defaults=html_column_styles_default,
                                            base_column_defaults=column_styles)
    html_text_styles = html_text_mapper(html_text_input=html_text_styles,
                                        html_text_defaults=html_text_styles_default,
                                        base_text_defaults=text_styles,
                                        html_px_multiplier=html_px_multiplier)

    # html_frame_styles = html_frame_mapper(html_frame_input=html_frame_styles,
    #                                       html_frame_defaults=html_frame_styles_default,
    #                                       html_px_multiplier=html_px_multiplier)
    # html_column_styles = html_column_mapper(html_columns_input=html_column_styles,
    #                                         html_column_defaults=html_column_styles_default)
    # html_text_styles = html_text_mapper(html_text_input=html_text_styles,
    #                                     html_text_defaults=html_text_styles_default,
    #                                     html_px_multiplier=html_px_multiplier)

    test = HtmlFrameStyles()

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    return FrameStore(frame_styles=frame_styles,
                      column_styles=column_styles,
                      text_styles=text_styles,
                      html_frame_styles=html_frame_styles,
                      html_column_styles=html_column_styles,
                      html_text_styles=html_text_styles)
