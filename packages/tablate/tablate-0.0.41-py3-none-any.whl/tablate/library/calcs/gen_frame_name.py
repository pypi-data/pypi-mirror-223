def gen_frame_name(name: str, type: str, frame_dict: dict, ensure_unique: bool = False):
    if name is not None:
        if ensure_unique is False:
            return name
        else:
            if name in frame_dict:
                append_index = 0
                while True:
                    unique_string = f"{name}{append_index}"
                    if unique_string in frame_dict:
                        append_index += 1
                    else:
                        return unique_string

            else:
                return name
    else:
        append_index = 0
        while True:
            untitled_frame_name = f"Untited{type.capitalize()}Frame{append_index}"
            if untitled_frame_name in frame_dict:
                append_index += 1
            else:
                return untitled_frame_name
