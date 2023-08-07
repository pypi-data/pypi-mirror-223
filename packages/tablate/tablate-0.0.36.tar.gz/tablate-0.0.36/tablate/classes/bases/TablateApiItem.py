from tablate.classes.bases.TablateApiBase import TablateApiBase


class TablateApiItem(TablateApiBase):

    @property
    def name(self):
        for frame_key in list(self._frame_list.items())[0]:
            return frame_key

    def rename(self, new_name: str):
        if new_name is not None:
            frame_key, frame_item = list(self._frame_list.items())[0]
            frame_item.name = new_name
            self._frame_list[new_name] = frame_item
            del self._frame_list[frame_key]


    def to_dict(self):
        frame_key, frame_item = list(self._frame_list.items())[0]
        if frame_item.type == "text":
            return {
                "text": [frame_item.args["text"]]
            }
        if frame_item.type == "grid":
            return_dict = {}
            for column_index, column_item in enumerate(frame_item.args["columns"]):
                return_dict[column_index] = [column_item["string"]]
            return return_dict
        if frame_item.type == "table":
            return_dict = {}
            for column_item in frame_item.args["columns"]:
                return_dict[column_item["key"]] = []
                for row_item in frame_item.args["rows"]:
                    return_dict[column_item["key"]].append(row_item[column_item["key"]])
            return return_dict
