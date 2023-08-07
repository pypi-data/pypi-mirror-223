from __future__ import annotations

from importlib.metadata import version

from tablate.api.Tablate import Tablate
from tablate.api.modules.Grid import Grid
from tablate.api.modules.Table import Table
from tablate.api.modules.Text import Text

from tablate.api.functions.concat import concat

# from tablate.type.type_input import HtmlOuterStylesInput, FrameStylesInput, HtmlFrameStylesInput, ColumnStylesInput, \
#     TextStylesInput, HtmlColumnStylesInput, HtmlTextStylesInput, RowsStylesInput, HtmlRowsStylesInput, \
#     HtmlColumnInput, BaseColumnInput, GridColumnInput, TableColumnInput, TableRowsInput, BaseStylesInput, \
#     TableHeaderFrameStylesInput, TableBodyFrameStylesInput, HtmlStylesInput, HtmlTextFrameStylesInput, \
#     HtmlGridStylesInput, HtmlTableStylesInput, HtmlTableHeaderStylesInput, HtmlTableBodyStylesInput

########################################################################################################################
########################################################################################################################
########################################################################################################################


try:
    __version__ = version('tablate')
except ModuleNotFoundError:
    pass
