from copy import deepcopy

from tablate.type.type_input import BaseColumnInput
from tablate.type.type_store import TableBodyFrameStore


def row_colors(column_item: BaseColumnInput, row_index: int, table_frame_store: TableBodyFrameStore) -> BaseColumnInput:
    row_column_item = deepcopy(column_item)
    if row_index % 2 == 1 and table_frame_store.row_styles.evens_background is not None:
        row_column_item["background"] = table_frame_store.row_styles.evens_background
    if row_index % 2 == 0 and table_frame_store.row_styles.odds_background is not None:
        row_column_item["background"] = table_frame_store.row_styles.odds_background
    return row_column_item
