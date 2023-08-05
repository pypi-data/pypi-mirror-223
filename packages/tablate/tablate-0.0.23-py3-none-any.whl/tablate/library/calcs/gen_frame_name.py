def gen_frame_name(name: str, type: str, frame_dict: dict, ensure_unique: bool = False):
    if name is not None:
        if ensure_unique is False:
            return name
        else:
            if name in frame_dict:
                append_index = 0
                while True:
                    unique_string = f"{name}{append_index}"
                    if unique_string not in frame_dict:
                        return unique_string
                    else:
                        append_index += 1
            else:
                return name
    else:
        untitled_frame_name = f"Untited{type.capitalize()}Frame0"
        for frame_index, (frame_key, _) in enumerate(frame_dict.items()):
            untitled_frame_name = f"Untited{type.capitalize()}Frame{frame_index}"
            if untitled_frame_name in frame_dict:
                continue
            else:
                return untitled_frame_name
        return untitled_frame_name