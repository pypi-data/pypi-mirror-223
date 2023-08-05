from typing import Union, Callable, Tuple

from tablate.classes.bases.TablateApiBase import TablateApiBase


class TablateApiItem(TablateApiBase):

    def name(self):
        for frame_key, frame_item in self._frame_list.items():
            print(frame_key)

    def rename(self, new_name: str):
        if new_name is not None:
            for frame_key, frame_item in self._frame_list.items():
                frame_item["name"] = new_name
                self._frame_list[new_name] = frame_item
                del self._frame_list[frame_key]
                break


    def to_dict(self):
        for frame_key, frame_item in self._frame_list.items():
            if frame_item["type"] == "text":
                return {
                    "text": [frame_item["options"]["text"]]
                }
            if frame_item["type"] == "grid":
                return_dict = {}
                for column_index, column_item in enumerate(frame_item["options"]["columns"]):
                    return_dict[column_index] = [column_item["string"]]
                return return_dict
            if frame_item["type"] == "table":
                return_dict = {}
                for column_item in frame_item["options"]["columns"]:
                    return_dict[column_item["key"]] = []
                    for row_item in frame_item["options"]["rows"]:
                        return_dict[column_item["key"]].append(row_item[column_item["key"]])
                return return_dict
