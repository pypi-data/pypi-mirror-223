from tablate.classes.options.html.style.utilities.base_values import base_class
from tablate.classes.options.html.style.utilities.style_types import SelectorDictUnion


class ClassNameMixin:

    _selector_dict: SelectorDictUnion

    def generate_class_names(self) -> str:
        return_string_array = [base_class]
        for key, value in self._selector_dict.items():
            # return_string_array.append(key)
            if type(value) == str:
                return_string_array.append(value)
        return " ".join(return_string_array)

